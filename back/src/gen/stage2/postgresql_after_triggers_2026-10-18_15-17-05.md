# PostgreSQL AFTER Trigger Implementation Report

## 1. Synthesis Overview

- **Target Relation(s)**: `public.manufacturers` and `public.products`.
- **Architecture Compliance**: The implementation uses statement-level `AFTER UPDATE` triggers with `REFERENCING OLD TABLE AS old_r NEW TABLE AS new_r`. Each trigger computes rule-scoped deletions and insertions and writes them transactionally to an asynchronous maintenance queue.
- **Scope and deployment contracts**:
  - The supplied information does not specify resolved predicate IRIs, named-graph URIs, or the class IRIs. These are not guessed: `public.ivm_rule_config` stores them and must be populated for all eight rules before updates are processed.
  - The URI templates are implemented as the given prefix followed by the primary-key value cast to text. This is direct placeholder substitution; deployments must confirm that it matches the source mapping’s exact URI-template encoding semantics.
  - The code assumes the source relations are in schema `public` and that the listed columns have the names and nullability described in the rules.
  - These triggers handle `UPDATE` statements, as requested. They do not implement separate `INSERT` or `DELETE` triggers.
  - For `tr-products-5` during a `manufacturers` update, the old-side query joins `old_r` to the current `products` relation. This correctly handles manufacturer updates where referencing product rows remain unchanged. If an update cascades changes to `products.brand_id`, the old product state is not available from the manufacturer trigger’s transition tables; supporting that case requires additional coordination or a separate cascade-aware maintenance design.

## 2. Trigger Execution & Component Computation

- **Snapshot Capture**: Each statement-level trigger receives the updated relation’s pre-update snapshot through `old_r` (`Δ⁻`) and post-update snapshot through `new_r` (`Δ⁺`). The trigger functions read these transition relations as statement snapshots.
- **Affected Deletion Tuples (`A⁻[Ψ](u)`)**:
  - For pivot-relevant rules, the old-side contribution query evaluates the rule against tuples in `old_r`.
  - For `tr-products-5` when `manufacturers` changes, the old-side query identifies affected product pivots by joining `public.products.brand_id` to `old_r.id`, and constructs the brand contribution using the old manufacturer identity.
  - For `tr-products-5` when `products` changes, the old-side query evaluates old product tuples against the unchanged `public.manufacturers` relation.
- **Affected Insertion Tuples (`A⁺[Ψ](u)`)**:
  - For pivot-relevant rules, the new-side contribution query evaluates the rule against tuples in `new_r`.
  - For `tr-products-5` when `manufacturers` changes, the new-side query joins `public.products.brand_id` to `new_r.id`.
  - For `tr-products-5` when `products` changes, the new-side query evaluates new product tuples against `public.manufacturers`. A null `brand_id` produces no brand contribution because the join finds no referenced manufacturer.
- **Post-Update Contributions (`S2[Ψ](u)`)**:
  - The post-update contribution for `tr-products-5` is obtained using the post-update side of the relevant statement and the FK path `products(brand_id) → manufacturers(id)`.
  - Local rules use the changed tuple’s own attributes and require no additional relational-path join.
  - `tr-manufacturers-3` is maintained exactly as supplied: a non-null `homepage` is represented as an IRI object. Its nonconforming OTR status does not change the implemented mapping behavior.
- **Changesets Computation (`Δ⁺(u)` and `Δ⁻(u)`)**:
  - Each function constructs old and new rule-scoped RDF contribution sets.
  - `old_q EXCEPT new_q` yields deletions; `new_q EXCEPT old_q` yields insertions. Set comparison includes the rule identifier, subject, object, term kind, and datatype, so rule provenance is retained and duplicate rows within a contribution set do not create duplicate changes.
  - Queue entries retain the configured predicate and graph URI alongside the RDF terms.

## 3. Asynchronous Maintenance Queue Integration

The implementation defines `public.ivm_maintenance_queue` as the transactional handoff to an asynchronous consumer. Each row contains the operation (`-` or `+`), rule identifier, graph URI, predicate URI, subject, object, object term kind, and optional datatype URI. Queue rows are committed atomically with the source update; a separate consumer can process them asynchronously.

Before enabling updates, populate `public.ivm_rule_config` with one row per rule. `predicate_uri` and `graph_uri` must be the actual resolved IRIs for that rule. For the two CTR rules, `fixed_object_uri` must also contain the actual class IRI. The trigger functions raise an error if a needed rule configuration is absent or incomplete; no guessed namespace or graph URI is emitted.

## 4. Generated PostgreSQL AFTER Trigger Code

```sql
-- Queue infrastructure.
CREATE TABLE IF NOT EXISTS public.ivm_rule_config (
    rule_id          text PRIMARY KEY,
    graph_uri        text NOT NULL CHECK (graph_uri <> ''),
    predicate_uri    text NOT NULL CHECK (predicate_uri <> ''),
    fixed_object_uri text,
    CHECK (fixed_object_uri IS NULL OR fixed_object_uri <> '')
);

CREATE TABLE IF NOT EXISTS public.ivm_maintenance_queue (
    queue_id       bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    transaction_id bigint NOT NULL,
    queued_at      timestamptz NOT NULL DEFAULT clock_timestamp(),
    operation      text NOT NULL CHECK (operation IN ('+', '-')),
    rule_id        text NOT NULL,
    graph_uri      text NOT NULL,
    subject        text NOT NULL,
    predicate      text NOT NULL,
    object         text NOT NULL,
    object_kind    text NOT NULL CHECK (object_kind IN ('IRI', 'LITERAL')),
    datatype_uri   text
);

-- Resolve configured rule terms strictly: missing configuration raises an error.
CREATE OR REPLACE FUNCTION public.ivm_graph_uri(p_rule_id text)
RETURNS text
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_uri text;
BEGIN
    SELECT c.graph_uri
      INTO STRICT v_uri
      FROM public.ivm_rule_config AS c
     WHERE c.rule_id = p_rule_id;

    RETURN v_uri;
END;
$$;

CREATE OR REPLACE FUNCTION public.ivm_predicate_uri(p_rule_id text)
RETURNS text
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_uri text;
BEGIN
    SELECT c.predicate_uri
      INTO STRICT v_uri
      FROM public.ivm_rule_config AS c
     WHERE c.rule_id = p_rule_id;

    RETURN v_uri;
END;
$$;

CREATE OR REPLACE FUNCTION public.ivm_fixed_object_uri(p_rule_id text)
RETURNS text
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_uri text;
BEGIN
    SELECT c.fixed_object_uri
      INTO STRICT v_uri
      FROM public.ivm_rule_config AS c
     WHERE c.rule_id = p_rule_id;

    IF v_uri IS NULL THEN
        RAISE EXCEPTION
            'fixed_object_uri is required for transformation rule %',
            p_rule_id;
    END IF;

    RETURN v_uri;
END;
$$;


-- Manufacturers UPDATE:
--   pivot rules: tr-manufacturers-1, tr-manufacturers-2, tr-manufacturers-3
--   relation rule: tr-products-5
CREATE OR REPLACE FUNCTION public.ivm_maintain_manufacturers_update()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    WITH
    old_q(rule_id, subject, object, object_kind, datatype_uri) AS (
        -- tr-manufacturers-1: schema:Organization
        SELECT
            'tr-manufacturers-1'::text,
            'http://example.com' || r.id::text,
            public.ivm_fixed_object_uri('tr-manufacturers-1'),
            'IRI'::text,
            NULL::text
        FROM old_r AS r

        UNION ALL

        -- tr-manufacturers-2: schema:name, xsd:string
        SELECT
            'tr-manufacturers-2'::text,
            'http://example.com' || r.id::text,
            r.name::text,
            'LITERAL'::text,
            'http://www.w3.org/2001/XMLSchema#string'::text
        FROM old_r AS r
        WHERE r.name IS NOT NULL

        UNION ALL

        -- tr-manufacturers-3: schema:url, RDFIRI(homepage)
        SELECT
            'tr-manufacturers-3'::text,
            'http://example.com' || r.id::text,
            r.homepage::text,
            'IRI'::text,
            NULL::text
        FROM old_r AS r
        WHERE r.homepage IS NOT NULL

        UNION ALL

        -- tr-products-5 old-side contribution for products referencing old ids.
        SELECT
            'tr-products-5'::text,
            'http://example.com' || p.product_id::text,
            'http://example.com' || r.id::text,
            'IRI'::text,
            NULL::text
        FROM old_r AS r
        JOIN public.products AS p
          ON p.brand_id = r.id
    ),
    new_q(rule_id, subject, object, object_kind, datatype_uri) AS (
        -- tr-manufacturers-1: schema:Organization
        SELECT
            'tr-manufacturers-1'::text,
            'http://example.com' || r.id::text,
            public.ivm_fixed_object_uri('tr-manufacturers-1'),
            'IRI'::text,
            NULL::text
        FROM new_r AS r

        UNION ALL

        -- tr-manufacturers-2: schema:name, xsd:string
        SELECT
            'tr-manufacturers-2'::text,
            'http://example.com' || r.id::text,
            r.name::text,
            'LITERAL'::text,
            'http://www.w3.org/2001/XMLSchema#string'::text
        FROM new_r AS r
        WHERE r.name IS NOT NULL

        UNION ALL

        -- tr-manufacturers-3: schema:url, RDFIRI(homepage)
        SELECT
            'tr-manufacturers-3'::text,
            'http://example.com' || r.id::text,
            r.homepage::text,
            'IRI'::text,
            NULL::text
        FROM new_r AS r
        WHERE r.homepage IS NOT NULL

        UNION ALL

        -- tr-products-5 post-update contribution for products referencing new ids.
        SELECT
            'tr-products-5'::text,
            'http://example.com' || p.product_id::text,
            'http://example.com' || r.id::text,
            'IRI'::text,
            NULL::text
        FROM new_r AS r
        JOIN public.products AS p
          ON p.brand_id = r.id
    ),
    delta(rule_id, subject, object, object_kind, datatype_uri, operation) AS (
        (
            SELECT rule_id, subject, object, object_kind, datatype_uri
            FROM old_q
            EXCEPT
            SELECT rule_id, subject, object, object_kind, datatype_uri
            FROM new_q
        )
        SELECT rule_id, subject, object, object_kind, datatype_uri, '-'::text
        FROM (
            SELECT rule_id, subject, object, object_kind, datatype_uri
            FROM old_q
            EXCEPT
            SELECT rule_id, subject, object, object_kind, datatype_uri
            FROM new_q
        ) AS deleted_q

        UNION ALL

        SELECT rule_id, subject, object, object_kind, datatype_uri, '+'::text
        FROM (
            SELECT rule_id, subject, object, object_kind, datatype_uri
            FROM new_q
            EXCEPT
            SELECT rule_id, subject, object, object_kind, datatype_uri
            FROM old_q
        ) AS inserted_q
    )
    INSERT INTO public.ivm_maintenance_queue (
        transaction_id,
        operation,
        rule_id,
        graph_uri,
        subject,
        predicate,
        object,
        object_kind,
        datatype_uri
    )
    SELECT
        txid_current(),
        d.operation,
        d.rule_id,
        public.ivm_graph_uri(d.rule_id),
        d.subject,
        public.ivm_predicate_uri(d.rule_id),
        d.object,
        d.object_kind,
        d.datatype_uri
    FROM delta AS d;

    RETURN NULL;
END;
$$;


-- Products UPDATE:
--   pivot rules: tr-products-1 through tr-products-5
CREATE OR REPLACE FUNCTION public.ivm_maintain_products_update()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    WITH
    old_q(rule_id, subject, object, object_kind, datatype_uri) AS (
        -- tr-products-1: schema:Product
        SELECT
            'tr-products-1'::text,
            'http://example.com' || d.product_id::text,
            public.ivm_fixed_object_uri('tr-products-1'),
            'IRI'::text,
            NULL::text
        FROM old_r AS d

        UNION ALL

        -- tr-products-2: schema:name, xsd:string
        SELECT
            'tr-products-2'::text,
            'http://example.com' || d.product_id::text,
            d.title::text,
            'LITERAL'::text,
            'http://www.w3.org/2001/XMLSchema#string'::text
        FROM old_r AS d
        WHERE d.title IS NOT NULL

        UNION ALL

        -- tr-products-3: schema:sku, xsd:string
        SELECT
            'tr-products-3'::text,
            'http://example.com' || d.product_id::text,
            d.sku::text,
            'LITERAL'::text,
            'http://www.w3.org/2001/XMLSchema#string'::text
        FROM old_r AS d
        WHERE d.sku IS NOT NULL

        UNION ALL

        -- tr-products-4: schema:price, xsd:decimal
        SELECT
            'tr-products-4'::text,
            'http://example.com' || d.product_id::text,
            d.price::text,
            'LITERAL'::text,
            'http://www.w3.org/2001/XMLSchema#decimal'::text
        FROM old_r AS d
        WHERE d.price IS NOT NULL

        UNION ALL

        -- tr-products-5 old-side path contribution.
        SELECT
            'tr-products-5'::text,
            'http://example.com' || d.product_id::text,
            'http://example.com' || t.id::text,
            'IRI'::text,
            NULL::text
        FROM old_r AS d
        JOIN public.manufacturers AS t
          ON t.id = d.brand_id
    ),
    new_q(rule_id, subject, object, object_kind, datatype_uri) AS (
        -- tr-products-1: schema:Product
        SELECT
            'tr-products-1'::text,
            'http://example.com' || d.product_id::text,
            public.ivm_fixed_object_uri('tr-products-1'),
            'IRI'::text,
            NULL::text
        FROM new_r AS d

        UNION ALL

        -- tr-products-2: schema:name, xsd:string
        SELECT
            'tr-products-2'::text,
            'http://example.com' || d.product_id::text,
            d.title::text,
            'LITERAL'::text,
            'http://www.w3.org/2001/XMLSchema#string'::text
        FROM new_r AS d
        WHERE d.title IS NOT NULL

        UNION ALL

        -- tr-products-3: schema:sku, xsd:string
        SELECT
            'tr-products-3'::text,
            'http://example.com' || d.product_id::text,
            d.sku::text,
            'LITERAL'::text,
            'http://www.w3.org/2001/XMLSchema#string'::text
        FROM new_r AS d
        WHERE d.sku IS NOT NULL

        UNION ALL

        -- tr-products-4: schema:price, xsd:decimal
        SELECT
            'tr-products-4'::text,
            'http://example.com' || d.product_id::text,
            d.price::text,
            'LITERAL'::text,
            'http://www.w3.org/2001/XMLSchema#decimal'::text
        FROM new_r AS d
        WHERE d.price IS NOT NULL

        UNION ALL

        -- tr-products-5 post-update path contribution.
        SELECT
            'tr-products-5'::text,
            'http://example.com' || d.product_id::text,
            'http://example.com' || t.id::text,
            'IRI'::text,
            NULL::text
        FROM new_r AS d
        JOIN public.manufacturers AS t
          ON t.id = d.brand_id
    ),
    deleted_q(rule_id, subject, object, object_kind, datatype_uri) AS (
        SELECT rule_id, subject, object, object_kind, datatype_uri
        FROM old_q
        EXCEPT
        SELECT rule_id, subject, object, object_kind, datatype_uri
        FROM new_q
    ),
    inserted_q(rule_id, subject, object, object_kind, datatype_uri) AS (
        SELECT rule_id, subject, object, object_kind, datatype_uri
        FROM new_q
        EXCEPT
        SELECT rule_id, subject, object, object_kind, datatype_uri
        FROM old_q
    ),
    delta(rule_id, subject, object, object_kind, datatype_uri, operation) AS (
        SELECT
            rule_id, subject, object, object_kind, datatype_uri, '-'::text
        FROM deleted_q

        UNION ALL

        SELECT
            rule_id, subject, object, object_kind, datatype_uri, '+'::text
        FROM inserted_q
    )
    INSERT INTO public.ivm_maintenance_queue (
        transaction_id,
        operation,
        rule_id,
        graph_uri,
        subject,
        predicate,
        object,
        object_kind,
        datatype_uri
    )
    SELECT
        txid_current(),
        d.operation,
        d.rule_id,
        public.ivm_graph_uri(d.rule_id),
        d.subject,
        public.ivm_predicate_uri(d.rule_id),
        d.object,
        d.object_kind,
        d.datatype_uri
    FROM delta AS d;

    RETURN NULL;
END;
$$;


-- Statement-level UPDATE triggers with transition relations.
CREATE TRIGGER ivm_manufacturers_after_update
AFTER UPDATE ON public.manufacturers
REFERENCING OLD TABLE AS old_r NEW TABLE AS new_r
FOR EACH STATEMENT
EXECUTE FUNCTION public.ivm_maintain_manufacturers_update();

CREATE TRIGGER ivm_products_after_update
AFTER UPDATE ON public.products
REFERENCING OLD TABLE AS old_r NEW TABLE AS new_r
FOR EACH STATEMENT
EXECUTE FUNCTION public.ivm_maintain_products_update();
```