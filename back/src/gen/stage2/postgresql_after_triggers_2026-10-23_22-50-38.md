# PostgreSQL AFTER Trigger Implementation Report

## 1. Synthesis Overview
- **Target Relation(s)**: `manufacturers`, `products`.
- **Architecture Compliance**: The implementation uses statement-level `AFTER UPDATE` triggers with `OLD TABLE` / `NEW TABLE` transition tables. Each trigger creates one `rdf_maintenance_queue` event and one `rdf_rule_contribution` row for every rule relevant to the updated relation. The trigger performs PostgreSQL-side maintenance computation only; it does not access GraphDB or perform the asynchronous worker’s deletion processing.
- **URI and mapping assumptions**: The supplied subject template `http://example.com⟨h⟩` is implemented as direct concatenation of `http://example.com` and the key’s text value. The rule graph URI is instantiated from the supplied queue-infrastructure template as `http://example.com/resource/tr/<rule_id>`. The provided context does not specify the SQL types of `products.title` or `products.sku`; their datatype templates below assume `xsd:string`. Change those two datatype values if the actual mapping metadata specifies otherwise. Literal values are recorded using their PostgreSQL text representation.

## 4. Generated PostgreSQL AFTER Trigger Code

```sql
CREATE OR REPLACE FUNCTION compute_changeset_manufacturers()
RETURNS trigger
LANGUAGE plpgsql
AS $function$
DECLARE
    v_event_id       bigint;
    v_rule_graph_uri text;
    v_contribution   jsonb;
    v_a_minus        jsonb;
    v_a_plus         jsonb;
    v_s2             jsonb;
    v_delta_plus_rel jsonb;
BEGIN
    INSERT INTO rdf_maintenance_queue (
        relation_name,
        operation_type,
        deleted_tuples,
        inserted_tuples
    )
    SELECT
        'manufacturers',
        'UPDATE',
        COALESCE(
            (SELECT jsonb_agg(to_jsonb(d))
             FROM old_manufacturers AS d),
            '[]'::jsonb
        ),
        COALESCE(
            (SELECT jsonb_agg(to_jsonb(i))
             FROM new_manufacturers AS i),
            '[]'::jsonb
        )
    RETURNING event_id INTO v_event_id;

    /*
     * tr-manufacturers-1: pivot-relevant CTR.
     * Only DeltaPlusPivot is required for this update relation.
     */
    v_rule_graph_uri :=
        'http://example.com/resource/tr/tr-manufacturers-1';

    SELECT jsonb_build_object(
        'rule_id', 'tr-manufacturers-1',
        'rule_type', 'CTR',
        'pivot_relation', 'manufacturers',
        'class_quad_template', jsonb_build_object(
            'predicate', 'rdf:type',
            'class', 'https://schema.org/Organization',
            'graph', v_rule_graph_uri
        ),
        'rdf_contributions', jsonb_build_object(
            'S2', '[]'::jsonb,
            'DeltaPlusPivot',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.id::text
                            )
                        )
                        FROM new_manufacturers AS i
                    ),
                    '[]'::jsonb
                ),
            'DeltaPlusRel', '[]'::jsonb,
            'DeltaPlus',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.id::text
                            )
                        )
                        FROM new_manufacturers AS i
                    ),
                    '[]'::jsonb
                )
        )
    )
    INTO v_contribution;

    INSERT INTO rdf_rule_contribution (
        event_id, rule_id, rule_graph_uri, relevance_type,
        pivot_relation, path, rule_contribution
    )
    VALUES (
        v_event_id,
        'tr-manufacturers-1',
        v_rule_graph_uri,
        'pivot',
        'manufacturers',
        '[]'::jsonb,
        v_contribution
    );

    /*
     * tr-manufacturers-2: pivot-relevant local DTR.
     */
    v_rule_graph_uri :=
        'http://example.com/resource/tr/tr-manufacturers-2';

    SELECT jsonb_build_object(
        'rule_id', 'tr-manufacturers-2',
        'rule_type', 'DTR',
        'pivot_relation', 'manufacturers',
        'datatype_quad_template', jsonb_build_object(
            'predicate', 'https://schema.org/name',
            'datatype', 'http://www.w3.org/2001/XMLSchema#string',
            'graph', v_rule_graph_uri
        ),
        'rdf_contributions', jsonb_build_object(
            'S2', '[]'::jsonb,
            'DeltaPlusPivot',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.id::text,
                                'object',
                                i.name::text
                            )
                        )
                        FROM new_manufacturers AS i
                        WHERE i.name IS NOT NULL
                    ),
                    '[]'::jsonb
                ),
            'DeltaPlusRel', '[]'::jsonb,
            'DeltaPlus',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.id::text,
                                'object',
                                i.name::text
                            )
                        )
                        FROM new_manufacturers AS i
                        WHERE i.name IS NOT NULL
                    ),
                    '[]'::jsonb
                )
        )
    )
    INTO v_contribution;

    INSERT INTO rdf_rule_contribution (
        event_id, rule_id, rule_graph_uri, relevance_type,
        pivot_relation, path, rule_contribution
    )
    VALUES (
        v_event_id,
        'tr-manufacturers-2',
        v_rule_graph_uri,
        'pivot',
        'manufacturers',
        '[]'::jsonb,
        v_contribution
    );

    /*
     * tr-manufacturers-3: pivot-relevant OTR with an IRI-valued object.
     */
    v_rule_graph_uri :=
        'http://example.com/resource/tr/tr-manufacturers-3';

    SELECT jsonb_build_object(
        'rule_id', 'tr-manufacturers-3',
        'rule_type', 'OTR',
        'pivot_relation', 'manufacturers',
        'object_quad_template', jsonb_build_object(
            'predicate', 'https://schema.org/url',
            'graph', v_rule_graph_uri
        ),
        'rdf_contributions', jsonb_build_object(
            'S2', '[]'::jsonb,
            'DeltaPlusPivot',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.id::text,
                                'object',
                                i.homepage::text
                            )
                        )
                        FROM new_manufacturers AS i
                        WHERE i.homepage IS NOT NULL
                    ),
                    '[]'::jsonb
                ),
            'DeltaPlusRel', '[]'::jsonb,
            'DeltaPlus',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.id::text,
                                'object',
                                i.homepage::text
                            )
                        )
                        FROM new_manufacturers AS i
                        WHERE i.homepage IS NOT NULL
                    ),
                    '[]'::jsonb
                )
        )
    )
    INTO v_contribution;

    INSERT INTO rdf_rule_contribution (
        event_id, rule_id, rule_graph_uri, relevance_type,
        pivot_relation, path, rule_contribution
    )
    VALUES (
        v_event_id,
        'tr-manufacturers-3',
        v_rule_graph_uri,
        'pivot',
        'manufacturers',
        '[]'::jsonb,
        v_contribution
    );

    /*
     * tr-products-5: relation-relevant OTR.
     * A_minus and A_plus are product tuples affected by the old and new
     * manufacturer tuples. S2 contains the post-update contributions for
     * A_plus. DeltaPlusRel is the set difference between post-update and
     * pre-update subject/object pairs.
     */
    SELECT COALESCE(jsonb_agg(to_jsonb(p)), '[]'::jsonb)
    INTO v_a_minus
    FROM products AS p
    JOIN old_manufacturers AS d
      ON p.brand_id = d.id;

    SELECT COALESCE(jsonb_agg(to_jsonb(p)), '[]'::jsonb)
    INTO v_a_plus
    FROM products AS p
    JOIN new_manufacturers AS i
      ON p.brand_id = i.id;

    SELECT COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'subject', x.subject,
                'object',  x.object
            )
        ),
        '[]'::jsonb
    )
    INTO v_s2
    FROM (
        SELECT DISTINCT
            'http://example.com' || p.product_id::text AS subject,
            'http://example.com' || i.id::text AS object
        FROM products AS p
        JOIN new_manufacturers AS i
          ON p.brand_id = i.id
    ) AS x;

    SELECT COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'subject', delta.subject,
                'object',  delta.object
            )
        ),
        '[]'::jsonb
    )
    INTO v_delta_plus_rel
    FROM (
        (
            SELECT DISTINCT
                'http://example.com' || p.product_id::text AS subject,
                'http://example.com' || i.id::text AS object
            FROM products AS p
            JOIN new_manufacturers AS i
              ON p.brand_id = i.id
        )
        EXCEPT
        (
            SELECT DISTINCT
                'http://example.com' || p.product_id::text AS subject,
                'http://example.com' || d.id::text AS object
            FROM products AS p
            JOIN old_manufacturers AS d
              ON p.brand_id = d.id
        )
    ) AS delta;

    v_rule_graph_uri :=
        'http://example.com/resource/tr/tr-products-5';

    SELECT jsonb_build_object(
        'rule_id', 'tr-products-5',
        'rule_type', 'OTR',
        'pivot_relation', 'products',
        'affected_tuples', jsonb_build_object(
            'A_minus', v_a_minus,
            'A_plus', v_a_plus
        ),
        'object_quad_template', jsonb_build_object(
            'predicate', 'https://schema.org/brand',
            'graph', v_rule_graph_uri
        ),
        'rdf_contributions', jsonb_build_object(
            'DeltaPlusPivot', '[]'::jsonb,
            'S2', v_s2,
            'DeltaPlusRel', v_delta_plus_rel,
            'DeltaPlus', v_delta_plus_rel
        )
    )
    INTO v_contribution;

    INSERT INTO rdf_rule_contribution (
        event_id, rule_id, rule_graph_uri, relevance_type,
        pivot_relation, path, rule_contribution
    )
    VALUES (
        v_event_id,
        'tr-products-5',
        v_rule_graph_uri,
        'relation',
        'products',
        jsonb_build_object(
            'foreign_key_path', jsonb_build_object(
                'from_relation', 'products',
                'from_column', 'brand_id',
                'to_relation', 'manufacturers',
                'to_column', 'id'
            )
        ),
        v_contribution
    );

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
DECLARE
    v_event_id       bigint;
    v_rule_graph_uri text;
    v_contribution   jsonb;
BEGIN
    INSERT INTO rdf_maintenance_queue (
        relation_name,
        operation_type,
        deleted_tuples,
        inserted_tuples
    )
    SELECT
        'products',
        'UPDATE',
        COALESCE(
            (SELECT jsonb_agg(to_jsonb(d))
             FROM old_products AS d),
            '[]'::jsonb
        ),
        COALESCE(
            (SELECT jsonb_agg(to_jsonb(i))
             FROM new_products AS i),
            '[]'::jsonb
        )
    RETURNING event_id INTO v_event_id;

    /*
     * tr-products-1: pivot-relevant CTR.
     */
    v_rule_graph_uri :=
        'http://example.com/resource/tr/tr-products-1';

    SELECT jsonb_build_object(
        'rule_id', 'tr-products-1',
        'rule_type', 'CTR',
        'pivot_relation', 'products',
        'class_quad_template', jsonb_build_object(
            'predicate', 'rdf:type',
            'class', 'https://schema.org/Product',
            'graph', v_rule_graph_uri
        ),
        'rdf_contributions', jsonb_build_object(
            'S2', '[]'::jsonb,
            'DeltaPlusPivot',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text
                            )
                        )
                        FROM new_products AS i
                    ),
                    '[]'::jsonb
                ),
            'DeltaPlusRel', '[]'::jsonb,
            'DeltaPlus',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text
                            )
                        )
                        FROM new_products AS i
                    ),
                    '[]'::jsonb
                )
        )
    )
    INTO v_contribution;

    INSERT INTO rdf_rule_contribution (
        event_id, rule_id, rule_graph_uri, relevance_type,
        pivot_relation, path, rule_contribution
    )
    VALUES (
        v_event_id,
        'tr-products-1',
        v_rule_graph_uri,
        'pivot',
        'products',
        '[]'::jsonb,
        v_contribution
    );

    /*
     * tr-products-2: pivot-relevant local DTR.
     * The datatype assumes products.title is mapped as xsd:string.
     */
    v_rule_graph_uri :=
        'http://example.com/resource/tr/tr-products-2';

    SELECT jsonb_build_object(
        'rule_id', 'tr-products-2',
        'rule_type', 'DTR',
        'pivot_relation', 'products',
        'datatype_quad_template', jsonb_build_object(
            'predicate', 'https://schema.org/name',
            'datatype', 'http://www.w3.org/2001/XMLSchema#string',
            'graph', v_rule_graph_uri
        ),
        'rdf_contributions', jsonb_build_object(
            'S2', '[]'::jsonb,
            'DeltaPlusPivot',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text,
                                'object',
                                i.title::text
                            )
                        )
                        FROM new_products AS i
                        WHERE i.title IS NOT NULL
                    ),
                    '[]'::jsonb
                ),
            'DeltaPlusRel', '[]'::jsonb,
            'DeltaPlus',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text,
                                'object',
                                i.title::text
                            )
                        )
                        FROM new_products AS i
                        WHERE i.title IS NOT NULL
                    ),
                    '[]'::jsonb
                )
        )
    )
    INTO v_contribution;

    INSERT INTO rdf_rule_contribution (
        event_id, rule_id, rule_graph_uri, relevance_type,
        pivot_relation, path, rule_contribution
    )
    VALUES (
        v_event_id,
        'tr-products-2',
        v_rule_graph_uri,
        'pivot',
        'products',
        '[]'::jsonb,
        v_contribution
    );

    /*
     * tr-products-3: pivot-relevant local DTR.
     * The datatype assumes products.sku is mapped as xsd:string.
     */
    v_rule_graph_uri :=
        'http://example.com/resource/tr/tr-products-3';

    SELECT jsonb_build_object(
        'rule_id', 'tr-products-3',
        'rule_type', 'DTR',
        'pivot_relation', 'products',
        'datatype_quad_template', jsonb_build_object(
            'predicate', 'https://schema.org/sku',
            'datatype', 'http://www.w3.org/2001/XMLSchema#string',
            'graph', v_rule_graph_uri
        ),
        'rdf_contributions', jsonb_build_object(
            'S2', '[]'::jsonb,
            'DeltaPlusPivot',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text,
                                'object',
                                i.sku::text
                            )
                        )
                        FROM new_products AS i
                        WHERE i.sku IS NOT NULL
                    ),
                    '[]'::jsonb
                ),
            'DeltaPlusRel', '[]'::jsonb,
            'DeltaPlus',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text,
                                'object',
                                i.sku::text
                            )
                        )
                        FROM new_products AS i
                        WHERE i.sku IS NOT NULL
                    ),
                    '[]'::jsonb
                )
        )
    )
    INTO v_contribution;

    INSERT INTO rdf_rule_contribution (
        event_id, rule_id, rule_graph_uri, relevance_type,
        pivot_relation, path, rule_contribution
    )
    VALUES (
        v_event_id,
        'tr-products-3',
        v_rule_graph_uri,
        'pivot',
        'products',
        '[]'::jsonb,
        v_contribution
    );

    /*
     * tr-products-4: pivot-relevant local DTR with the supplied xsd:decimal
     * datatype.
     */
    v_rule_graph_uri :=
        'http://example.com/resource/tr/tr-products-4';

    SELECT jsonb_build_object(
        'rule_id', 'tr-products-4',
        'rule_type', 'DTR',
        'pivot_relation', 'products',
        'datatype_quad_template', jsonb_build_object(
            'predicate', 'https://schema.org/price',
            'datatype', 'http://www.w3.org/2001/XMLSchema#decimal',
            'graph', v_rule_graph_uri
        ),
        'rdf_contributions', jsonb_build_object(
            'S2', '[]'::jsonb,
            'DeltaPlusPivot',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text,
                                'object',
                                i.price::text
                            )
                        )
                        FROM new_products AS i
                        WHERE i.price IS NOT NULL
                    ),
                    '[]'::jsonb
                ),
            'DeltaPlusRel', '[]'::jsonb,
            'DeltaPlus',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text,
                                'object',
                                i.price::text
                            )
                        )
                        FROM new_products AS i
                        WHERE i.price IS NOT NULL
                    ),
                    '[]'::jsonb
                )
        )
    )
    INTO v_contribution;

    INSERT INTO rdf_rule_contribution (
        event_id, rule_id, rule_graph_uri, relevance_type,
        pivot_relation, path, rule_contribution
    )
    VALUES (
        v_event_id,
        'tr-products-4',
        v_rule_graph_uri,
        'pivot',
        'products',
        '[]'::jsonb,
        v_contribution
    );

    /*
     * tr-products-5: pivot-relevant OTR.
     * The object URI is generated from the referenced manufacturer id.
     */
    v_rule_graph_uri :=
        'http://example.com/resource/tr/tr-products-5';

    SELECT jsonb_build_object(
        'rule_id', 'tr-products-5',
        'rule_type', 'OTR',
        'pivot_relation', 'products',
        'object_quad_template', jsonb_build_object(
            'predicate', 'https://schema.org/brand',
            'graph', v_rule_graph_uri
        ),
        'rdf_contributions', jsonb_build_object(
            'DeltaPlusPivot',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text,
                                'object',
                                'http://example.com' || m.id::text
                            )
                        )
                        FROM new_products AS i
                        JOIN manufacturers AS m
                          ON i.brand_id = m.id
                    ),
                    '[]'::jsonb
                ),
            'S2', '[]'::jsonb,
            'DeltaPlusRel', '[]'::jsonb,
            'DeltaPlus',
                COALESCE(
                    (
                        SELECT jsonb_agg(
                            jsonb_build_object(
                                'subject',
                                'http://example.com' || i.product_id::text,
                                'object',
                                'http://example.com' || m.id::text
                            )
                        )
                        FROM new_products AS i
                        JOIN manufacturers AS m
                          ON i.brand_id = m.id
                    ),
                    '[]'::jsonb
                )
        )
    )
    INTO v_contribution;

    INSERT INTO rdf_rule_contribution (
        event_id, rule_id, rule_graph_uri, relevance_type,
        pivot_relation, path, rule_contribution
    )
    VALUES (
        v_event_id,
        'tr-products-5',
        v_rule_graph_uri,
        'pivot',
        'products',
        jsonb_build_object(
            'foreign_key_path', jsonb_build_object(
                'from_relation', 'products',
                'from_column', 'brand_id',
                'to_relation', 'manufacturers',
                'to_column', 'id'
            )
        ),
        v_contribution
    );

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