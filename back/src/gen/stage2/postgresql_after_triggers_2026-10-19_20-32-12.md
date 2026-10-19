# PostgreSQL AFTER Trigger Implementation Report

## 1. Synthesis Overview

- **Target Relation(s)**: `manufacturers` and `products`.
- **Architecture Compliance**: Both triggers are statement-level `AFTER UPDATE` triggers using `REFERENCING OLD TABLE` and `NEW TABLE` transition relations. Each function computes rule-level insertion and deletion contributions and enqueues them; it does not apply RDF changes or perform asynchronous worker operations.

**Interface and specification boundary:** The prompt does not include the schema for the maintenance queue, its prescribed JSON templates, the SQL column types, RDF namespace declarations, or URI-template escaping rules. The SQL below therefore defines an explicit queue adapter contract rather than claiming compatibility with an unspecified existing queue. It preserves the supplied predicate names as CURIE strings and uses the supplied URI template by direct textual substitution: `http://example.com` followed by the key’s text value. Adapt the queue table and term serialization to the actual infrastructure before deployment if those differ.

The update plan is implemented as follows:

| Updated relation | Pivot-relevant rules | Relation-relevant rules |
|---|---|---|
| `manufacturers` | `tr-manufacturers-1`, `tr-manufacturers-2`, `tr-manufacturers-3` | `tr-products-5` |
| `products` | `tr-products-1` through `tr-products-5` | None |

The `schema:url` mapping is included as supplied, although the specification identifies it as nonconforming to the entity-preserving OTR pattern.

## 2. Trigger Execution & Component Computation

- **Snapshot Capture**: `old_manufacturers` / `new_manufacturers` and `old_products` / `new_products` expose the statement’s deleted and inserted row images. They are used as the update snapshots `Δ⁻` and `Δ⁺`; they are not persistent copies of the entire source relations.

- **Affected Deletion Tuples (`A⁻[Ψ](u)`)**:
  - For pivot-relevant rules, old transition-table rows supply the affected pivot tuples.
  - For `tr-products-5` on a manufacturer update, `A⁻` is the set of current product rows whose `brand_id` matches an old manufacturer `id`.

- **Affected Insertion Tuples (`A⁺[Ψ](u)`)**:
  - For pivot-relevant rules, new transition-table rows supply the affected pivot tuples.
  - For `tr-products-5` on a manufacturer update, `A⁺` is the set of current product rows whose `brand_id` matches a new manufacturer `id`.

- **Post-Update Contributions (`S2[Ψ](u)`)**:
  - Manufacturer pivot rules map new manufacturer rows directly.
  - Product pivot rules map new product rows directly; `tr-products-5` additionally joins those rows to the post-update `manufacturers` relation.
  - The manufacturer-trigger path contribution evaluates the post-update product/manufacturer join for products in `A⁺`.

- **Changesets Computation (`Δ⁺(u)` and `Δ⁻(u)`)**: Each rule’s old and new RDF contributions are represented as rows containing its rule identifier, subject term, predicate, and object term. Set difference computes deletions (`old_contributions EXCEPT new_contributions`) and insertions (`new_contributions EXCEPT old_contributions`). Only nonempty changesets are enqueued.

**Operational assumption:** The manufacturer-path implementation relies on manufacturer `id` values being stable during an update, or on referential actions leaving the relevant product rows discoverable by the old/new IDs at trigger execution. A primary-key change with cascading updates can require an explicit old-to-new entity correspondence; the supplied schema and plan do not provide one.

## 3. Asynchronous Maintenance Queue Integration

The code defines `rdf_maintenance_queue` as the adapter interface used by these trigger functions. Each queue row contains the source relation and two JSONB arrays, `delta_plus` and `delta_minus`. Each array element has this shape:

```json
{
  "rule_id": "tr-products-2",
  "subject": {"term_type": "IRI", "value": "http://example.com..."},
  "predicate": "schema:name",
  "object": {
    "term_type": "Literal",
    "value": "example",
    "datatype": "xsd:string"
  }
}
```

Object-property and URL objects use `term_type: "IRI"`; datatype-property objects use `term_type: "Literal"`. The queue stores rule-level contributions, as requested. The report does not assign a named graph because none is specified. The asynchronous worker remains responsible for consuming the queue and applying its own operations.

## 4. Generated PostgreSQL AFTER Trigger Code

```sql
-- Queue adapter contract for this implementation.
-- Replace this definition or the INSERT statements below if the
-- deployment's maintenance-queue infrastructure uses a different schema.
CREATE TABLE IF NOT EXISTS rdf_maintenance_queue (
    queue_id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_relation  text        NOT NULL,
    delta_plus       jsonb       NOT NULL,
    delta_minus      jsonb       NOT NULL,
    enqueued_at      timestamptz NOT NULL DEFAULT clock_timestamp()
);


CREATE OR REPLACE FUNCTION compute_changeset_manufacturers()
RETURNS trigger
LANGUAGE plpgsql
AS $function$
BEGIN
    WITH
    -- A- for the relation-relevant tr-products-5 rule.
    a_minus_products AS (
        SELECT p.product_id, p.brand_id
        FROM products AS p
        JOIN old_manufacturers AS om
          ON p.brand_id = om.id
    ),

    -- A+ for the relation-relevant tr-products-5 rule.
    a_plus_products AS (
        SELECT p.product_id, p.brand_id
        FROM products AS p
        JOIN new_manufacturers AS nm
          ON p.brand_id = nm.id
    ),

    -- S2 for tr-products-5: evaluate the path against post-update state.
    s2_brand AS (
        SELECT
            ap.product_id,
            m.id AS manufacturer_id
        FROM a_plus_products AS ap
        JOIN manufacturers AS m
          ON m.id = ap.brand_id
    ),

    old_contributions AS (
        -- tr-manufacturers-1: schema:Organization
        SELECT
            'tr-manufacturers-1'::text AS rule_id,
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || om.id::text
            ) AS subject,
            'schema:Organization'::text AS predicate,
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'schema:Organization'
            ) AS object_term
        FROM old_manufacturers AS om

        UNION ALL

        -- tr-manufacturers-2: schema:name, xsd:string
        SELECT
            'tr-manufacturers-2',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || om.id::text
            ),
            'schema:name',
            jsonb_build_object(
                'term_type', 'Literal',
                'value', om.name::text,
                'datatype', 'xsd:string'
            )
        FROM old_manufacturers AS om
        WHERE om.name IS NOT NULL

        UNION ALL

        -- tr-manufacturers-3: schema:url, RDFIRI(homepage)
        SELECT
            'tr-manufacturers-3',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || om.id::text
            ),
            'schema:url',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', om.homepage::text
            )
        FROM old_manufacturers AS om
        WHERE om.homepage IS NOT NULL

        UNION ALL

        -- Old tr-products-5 contributions for A- product pivots.
        SELECT
            'tr-products-5',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ),
            'schema:brand',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || om.id::text
            )
        FROM a_minus_products AS ap
        JOIN old_manufacturers AS om
          ON om.id = ap.brand_id
    ),

    new_contributions AS (
        -- tr-manufacturers-1: schema:Organization
        SELECT
            'tr-manufacturers-1'::text AS rule_id,
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || nm.id::text
            ) AS subject,
            'schema:Organization'::text AS predicate,
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'schema:Organization'
            ) AS object_term
        FROM new_manufacturers AS nm

        UNION ALL

        -- tr-manufacturers-2: schema:name, xsd:string
        SELECT
            'tr-manufacturers-2',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || nm.id::text
            ),
            'schema:name',
            jsonb_build_object(
                'term_type', 'Literal',
                'value', nm.name::text,
                'datatype', 'xsd:string'
            )
        FROM new_manufacturers AS nm
        WHERE nm.name IS NOT NULL

        UNION ALL

        -- tr-manufacturers-3: schema:url, RDFIRI(homepage)
        SELECT
            'tr-manufacturers-3',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || nm.id::text
            ),
            'schema:url',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', nm.homepage::text
            )
        FROM new_manufacturers AS nm
        WHERE nm.homepage IS NOT NULL

        UNION ALL

        -- Post-update tr-products-5 contributions for S2.
        SELECT
            'tr-products-5',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || sb.product_id::text
            ),
            'schema:brand',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || sb.manufacturer_id::text
            )
        FROM s2_brand AS sb
    ),

    delta_minus AS (
        SELECT rule_id, subject, predicate, object_term
        FROM old_contributions
        EXCEPT
        SELECT rule_id, subject, predicate, object_term
        FROM new_contributions
    ),

    delta_plus AS (
        SELECT rule_id, subject, predicate, object_term
        FROM new_contributions
        EXCEPT
        SELECT rule_id, subject, predicate, object_term
        FROM old_contributions
    ),

    payload AS (
        SELECT
            COALESCE(
                (
                    SELECT jsonb_agg(
                        jsonb_build_object(
                            'rule_id', d.rule_id,
                            'subject', d.subject,
                            'predicate', d.predicate,
                            'object', d.object_term
                        )
                        ORDER BY d.rule_id, d.subject::text,
                                 d.predicate, d.object_term::text
                    )
                    FROM delta_plus AS d
                ),
                '[]'::jsonb
            ) AS delta_plus_json,
            COALESCE(
                (
                    SELECT jsonb_agg(
                        jsonb_build_object(
                            'rule_id', d.rule_id,
                            'subject', d.subject,
                            'predicate', d.predicate,
                            'object', d.object_term
                        )
                        ORDER BY d.rule_id, d.subject::text,
                                 d.predicate, d.object_term::text
                    )
                    FROM delta_minus AS d
                ),
                '[]'::jsonb
            ) AS delta_minus_json
    )

    INSERT INTO rdf_maintenance_queue (
        source_relation,
        delta_plus,
        delta_minus
    )
    SELECT
        'manufacturers',
        payload.delta_plus_json,
        payload.delta_minus_json
    FROM payload
    WHERE payload.delta_plus_json <> '[]'::jsonb
       OR payload.delta_minus_json <> '[]'::jsonb;

    RETURN NULL;
END;
$function$;


CREATE TRIGGER manufacturers_compute_changeset_after_update
AFTER UPDATE ON manufacturers
REFERENCING
    OLD TABLE AS old_manufacturers
    NEW TABLE AS new_manufacturers
FOR EACH STATEMENT
EXECUTE FUNCTION compute_changeset_manufacturers();


CREATE OR REPLACE FUNCTION compute_changeset_products()
RETURNS trigger
LANGUAGE plpgsql
AS $function$
BEGIN
    WITH
    -- A- and A+ for product-pivot rules.
    a_minus_products AS (
        SELECT op.product_id, op.title, op.sku, op.price, op.brand_id
        FROM old_products AS op
    ),

    a_plus_products AS (
        SELECT np.product_id, np.title, np.sku, np.price, np.brand_id
        FROM new_products AS np
    ),

    -- S2 for tr-products-5: evaluate the post-update FK path.
    s2_brand AS (
        SELECT
            ap.product_id,
            m.id AS manufacturer_id
        FROM a_plus_products AS ap
        JOIN manufacturers AS m
          ON m.id = ap.brand_id
    ),

    old_contributions AS (
        -- tr-products-1: schema:Product
        SELECT
            'tr-products-1'::text AS rule_id,
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ) AS subject,
            'schema:Product'::text AS predicate,
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'schema:Product'
            ) AS object_term
        FROM a_minus_products AS ap

        UNION ALL

        -- tr-products-2: schema:name, xsd:string
        SELECT
            'tr-products-2',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ),
            'schema:name',
            jsonb_build_object(
                'term_type', 'Literal',
                'value', ap.title::text,
                'datatype', 'xsd:string'
            )
        FROM a_minus_products AS ap
        WHERE ap.title IS NOT NULL

        UNION ALL

        -- tr-products-3: schema:sku, xsd:string
        SELECT
            'tr-products-3',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ),
            'schema:sku',
            jsonb_build_object(
                'term_type', 'Literal',
                'value', ap.sku::text,
                'datatype', 'xsd:string'
            )
        FROM a_minus_products AS ap
        WHERE ap.sku IS NOT NULL

        UNION ALL

        -- tr-products-4: schema:price, xsd:decimal
        SELECT
            'tr-products-4',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ),
            'schema:price',
            jsonb_build_object(
                'term_type', 'Literal',
                'value', ap.price::text,
                'datatype', 'xsd:decimal'
            )
        FROM a_minus_products AS ap
        WHERE ap.price IS NOT NULL

        UNION ALL

        -- Old tr-products-5 contribution for the old product pivot.
        SELECT
            'tr-products-5',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ),
            'schema:brand',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || m.id::text
            )
        FROM a_minus_products AS ap
        JOIN manufacturers AS m
          ON m.id = ap.brand_id
    ),

    new_contributions AS (
        -- tr-products-1: schema:Product
        SELECT
            'tr-products-1'::text AS rule_id,
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ) AS subject,
            'schema:Product'::text AS predicate,
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'schema:Product'
            ) AS object_term
        FROM a_plus_products AS ap

        UNION ALL

        -- tr-products-2: schema:name, xsd:string
        SELECT
            'tr-products-2',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ),
            'schema:name',
            jsonb_build_object(
                'term_type', 'Literal',
                'value', ap.title::text,
                'datatype', 'xsd:string'
            )
        FROM a_plus_products AS ap
        WHERE ap.title IS NOT NULL

        UNION ALL

        -- tr-products-3: schema:sku, xsd:string
        SELECT
            'tr-products-3',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ),
            'schema:sku',
            jsonb_build_object(
                'term_type', 'Literal',
                'value', ap.sku::text,
                'datatype', 'xsd:string'
            )
        FROM a_plus_products AS ap
        WHERE ap.sku IS NOT NULL

        UNION ALL

        -- tr-products-4: schema:price, xsd:decimal
        SELECT
            'tr-products-4',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || ap.product_id::text
            ),
            'schema:price',
            jsonb_build_object(
                'term_type', 'Literal',
                'value', ap.price::text,
                'datatype', 'xsd:decimal'
            )
        FROM a_plus_products AS ap
        WHERE ap.price IS NOT NULL

        UNION ALL

        -- Post-update tr-products-5 contribution for S2.
        SELECT
            'tr-products-5',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || sb.product_id::text
            ),
            'schema:brand',
            jsonb_build_object(
                'term_type', 'IRI',
                'value', 'http://example.com' || sb.manufacturer_id::text
            )
        FROM s2_brand AS sb
    ),

    delta_minus AS (
        SELECT rule_id, subject, predicate, object_term
        FROM old_contributions
        EXCEPT
        SELECT rule_id, subject, predicate, object_term
        FROM new_contributions
    ),

    delta_plus AS (
        SELECT rule_id, subject, predicate, object_term
        FROM new_contributions
        EXCEPT
        SELECT rule_id, subject, predicate, object_term
        FROM old_contributions
    ),

    payload AS (
        SELECT
            COALESCE(
                (
                    SELECT jsonb_agg(
                        jsonb_build_object(
                            'rule_id', d.rule_id,
                            'subject', d.subject,
                            'predicate', d.predicate,
                            'object', d.object_term
                        )
                        ORDER BY d.rule_id, d.subject::text,
                                 d.predicate, d.object_term::text
                    )
                    FROM delta_plus AS d
                ),
                '[]'::jsonb
            ) AS delta_plus_json,
            COALESCE(
                (
                    SELECT jsonb_agg(
                        jsonb_build_object(
                            'rule_id', d.rule_id,
                            'subject', d.subject,
                            'predicate', d.predicate,
                            'object', d.object_term
                        )
                        ORDER BY d.rule_id, d.subject::text,
                                 d.predicate, d.object_term::text
                    )
                    FROM delta_minus AS d
                ),
                '[]'::jsonb
            ) AS delta_minus_json
    )

    INSERT INTO rdf_maintenance_queue (
        source_relation,
        delta_plus,
        delta_minus
    )
    SELECT
        'products',
        payload.delta_plus_json,
        payload.delta_minus_json
    FROM payload
    WHERE payload.delta_plus_json <> '[]'::jsonb
       OR payload.delta_minus_json <> '[]'::jsonb;

    RETURN NULL;
END;
$function$;


CREATE TRIGGER products_compute_changeset_after_update
AFTER UPDATE ON products
REFERENCING
    OLD TABLE AS old_products
    NEW TABLE AS new_products
FOR EACH STATEMENT
EXECUTE FUNCTION compute_changeset_products();
```