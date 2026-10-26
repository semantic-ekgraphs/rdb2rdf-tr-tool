# PostgreSQL AFTER Trigger Implementation Report

## 1. Synthesis Overview
- **Target Relation(s)**: `manufacturers` and `products` (statement-level `UPDATE` events).
- **Architecture Compliance**: The triggers use `AFTER UPDATE ... FOR EACH STATEMENT` transition tables (`OLD TABLE` / `NEW TABLE`) and enqueue one maintenance event per statement, followed by one rule contribution per relevant transformation rule. The trigger computes the rule-level affected tuples and RDF contribution deltas; asynchronous RDF materialization remains the worker’s responsibility.

## 4. Generated PostgreSQL AFTER Trigger Code

```sql
-- Assumptions:
--   * rdf_maintenance_queue and rdf_rule_contribution already exist with the
--     schemas supplied in the maintenance-queue specification.
--   * The relation columns used below are those referenced by the supplied
--     transformation rules: manufacturers(id, name, homepage) and
--     products(product_id, title, sku, price, brand_id).
--   * URI templates are instantiated as supplied: the placeholder value is
--     concatenated directly after 'http://example.com'.
--   * The helper stores RDF contributions as JSON values for the asynchronous
--     worker. It does not apply changes to an RDF store.

CREATE OR REPLACE FUNCTION rdf_jsonb_array_difference(
    p_left  jsonb,
    p_right jsonb
)
RETURNS jsonb
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT COALESCE(jsonb_agg(x.value), '[]'::jsonb)
    FROM (
        SELECT value
        FROM jsonb_array_elements(COALESCE(p_left, '[]'::jsonb))
        EXCEPT
        SELECT value
        FROM jsonb_array_elements(COALESCE(p_right, '[]'::jsonb))
    ) AS x;
$$;


CREATE OR REPLACE FUNCTION rdf_publish_rule_contribution(
    p_event_id       bigint,
    p_rule_id        text,
    p_relevance_type text,
    p_pivot_relation text,
    p_path           jsonb,
    p_rule_metadata  jsonb,
    p_a_minus        jsonb,
    p_a_plus         jsonb,
    p_s1             jsonb,
    p_s2             jsonb
)
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    v_delta_plus  jsonb;
    v_delta_minus jsonb;
    v_contribution jsonb;
BEGIN
    v_delta_plus  := rdf_jsonb_array_difference(p_s2, p_s1);
    v_delta_minus := rdf_jsonb_array_difference(p_s1, p_s2);

    v_contribution :=
        COALESCE(p_rule_metadata, '{}'::jsonb)
        || jsonb_build_object(
            'rule_id', p_rule_id,
            'pivot_relation', p_pivot_relation,
            'A-', COALESCE(p_a_minus, '[]'::jsonb),
            'A+', COALESCE(p_a_plus, '[]'::jsonb),
            'rdf_contributions', jsonb_build_object(
                'S2', COALESCE(p_s2, '[]'::jsonb),
                'DeltaPlus', v_delta_plus,
                'DeltaMinus', v_delta_minus
            )
        );

    INSERT INTO rdf_rule_contribution (
        event_id,
        rule_id,
        rule_graph_uri,
        relevance_type,
        pivot_relation,
        path,
        rule_contribution
    )
    VALUES (
        p_event_id,
        p_rule_id,
        'http://example.com/resource/tr/' || p_rule_id,
        p_relevance_type,
        p_pivot_relation,
        COALESCE(p_path, '[]'::jsonb),
        v_contribution
    );
END;
$$;


CREATE OR REPLACE FUNCTION compute_changeset_manufacturers()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_event_id bigint;
    v_deleted jsonb;
    v_inserted jsonb;

    v_a_minus jsonb;
    v_a_plus jsonb;
    v_s1 jsonb;
    v_s2 jsonb;
BEGIN
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_deleted
      FROM old_manufacturers AS o;

    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_inserted
      FROM new_manufacturers AS n;

    INSERT INTO rdf_maintenance_queue (
        relation_name,
        operation_type,
        deleted_tuples,
        inserted_tuples
    )
    VALUES (
        'manufacturers',
        'UPDATE',
        v_deleted,
        v_inserted
    )
    RETURNING event_id INTO v_event_id;

    -- tr-manufacturers-1: CTR, manufacturer class membership.
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_a_minus
      FROM old_manufacturers AS o;
    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_a_plus
      FROM new_manufacturers AS n;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || o.id::text
               )),
               '[]'::jsonb
           )
      INTO v_s1
      FROM old_manufacturers AS o;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || n.id::text
               )),
               '[]'::jsonb
           )
      INTO v_s2
      FROM new_manufacturers AS n;

    PERFORM rdf_publish_rule_contribution(
        v_event_id,
        'tr-manufacturers-1',
        'pivot-relevant',
        'manufacturers',
        '[]'::jsonb,
        jsonb_build_object(
            'rule_type', 'CTR',
            'class_quad_template', jsonb_build_object(
                'predicate', 'rdf:type',
                'class', 'https://schema.org/Organization',
                'graph', 'http://example.com/resource/tr/tr-manufacturers-1'
            )
        ),
        v_a_minus, v_a_plus, v_s1, v_s2
    );

    -- tr-manufacturers-2: Local-DTR, manufacturer name.
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_a_minus
      FROM old_manufacturers AS o;
    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_a_plus
      FROM new_manufacturers AS n;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || o.id::text,
                   'object', jsonb_build_object(
                       'value', o.name::text,
                       'datatype', 'http://www.w3.org/2001/XMLSchema#string'
                   )
               )),
               '[]'::jsonb
           )
      INTO v_s1
      FROM old_manufacturers AS o
     WHERE o.name IS NOT NULL;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || n.id::text,
                   'object', jsonb_build_object(
                       'value', n.name::text,
                       'datatype', 'http://www.w3.org/2001/XMLSchema#string'
                   )
               )),
               '[]'::jsonb
           )
      INTO v_s2
      FROM new_manufacturers AS n
     WHERE n.name IS NOT NULL;

    PERFORM rdf_publish_rule_contribution(
        v_event_id,
        'tr-manufacturers-2',
        'pivot-relevant',
        'manufacturers',
        '[]'::jsonb,
        jsonb_build_object(
            'rule_type', 'DTR',
            'datatype_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/name',
                'datatype', 'http://www.w3.org/2001/XMLSchema#string',
                'graph', 'http://example.com/resource/tr/tr-manufacturers-2'
            )
        ),
        v_a_minus, v_a_plus, v_s1, v_s2
    );

    -- tr-manufacturers-3: reification/value-derived IRI OTR.
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_a_minus
      FROM old_manufacturers AS o;
    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_a_plus
      FROM new_manufacturers AS n;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || o.id::text,
                   'object', o.homepage::text
               )),
               '[]'::jsonb
           )
      INTO v_s1
      FROM old_manufacturers AS o
     WHERE o.homepage IS NOT NULL;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || n.id::text,
                   'object', n.homepage::text
               )),
               '[]'::jsonb
           )
      INTO v_s2
      FROM new_manufacturers AS n
     WHERE n.homepage IS NOT NULL;

    PERFORM rdf_publish_rule_contribution(
        v_event_id,
        'tr-manufacturers-3',
        'pivot-relevant',
        'manufacturers',
        '[]'::jsonb,
        jsonb_build_object(
            'rule_type', 'OTR',
            'object_property_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/url',
                'graph', 'http://example.com/resource/tr/tr-manufacturers-3',
                'object_kind', 'IRI'
            )
        ),
        v_a_minus, v_a_plus, v_s1, v_s2
    );

    -- tr-products-5: relation-relevant update to manufacturers.
    -- A-/A+ are the product pivot tuples reached through brand_id = id.
    -- S1 is the contribution before the manufacturer update; S2 is the
    -- post-update contribution for products currently matching the new rows.
    SELECT COALESCE(jsonb_agg(to_jsonb(p)), '[]'::jsonb)
      INTO v_a_minus
      FROM products AS p
      JOIN old_manufacturers AS o ON p.brand_id = o.id;
    SELECT COALESCE(jsonb_agg(to_jsonb(p)), '[]'::jsonb)
      INTO v_a_plus
      FROM products AS p
      JOIN new_manufacturers AS n ON p.brand_id = n.id;

    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || p.product_id::text,
                   'object', 'http://example.com' || o.id::text
               )),
               '[]'::jsonb
           )
      INTO v_s1
      FROM products AS p
      JOIN old_manufacturers AS o ON p.brand_id = o.id;

    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || p.product_id::text,
                   'object', 'http://example.com' || n.id::text
               )),
               '[]'::jsonb
           )
      INTO v_s2
      FROM products AS p
      JOIN new_manufacturers AS n ON p.brand_id = n.id;

    PERFORM rdf_publish_rule_contribution(
        v_event_id,
        'tr-products-5',
        'relation-relevant',
        'products',
        '[{"from":"products.brand_id","to":"manufacturers.id"}]'::jsonb,
        jsonb_build_object(
            'rule_type', 'OTR',
            'object_property_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/brand',
                'graph', 'http://example.com/resource/tr/tr-products-5',
                'subject_template', 'http://example.com⟨h⟩',
                'subject_placeholder_order', jsonb_build_array(
                    jsonb_build_object('relation', 'products', 'attribute', 'product_id')
                ),
                'object_template', 'http://example.com⟨h⟩',
                'object_placeholder_order', jsonb_build_array(
                    jsonb_build_object('relation', 'manufacturers', 'attribute', 'id')
                )
            )
        ),
        v_a_minus, v_a_plus, v_s1, v_s2
    );

    RETURN NULL;
END;
$$;


CREATE TRIGGER manufacturers_compute_changeset_after_update
AFTER UPDATE ON manufacturers
REFERENCING OLD TABLE AS old_manufacturers
            NEW TABLE AS new_manufacturers
FOR EACH STATEMENT
EXECUTE FUNCTION compute_changeset_manufacturers();


CREATE OR REPLACE FUNCTION compute_changeset_products()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_event_id bigint;
    v_deleted jsonb;
    v_inserted jsonb;

    v_a_minus jsonb;
    v_a_plus jsonb;
    v_s1 jsonb;
    v_s2 jsonb;
BEGIN
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_deleted
      FROM old_products AS o;

    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_inserted
      FROM new_products AS n;

    INSERT INTO rdf_maintenance_queue (
        relation_name,
        operation_type,
        deleted_tuples,
        inserted_tuples
    )
    VALUES (
        'products',
        'UPDATE',
        v_deleted,
        v_inserted
    )
    RETURNING event_id INTO v_event_id;

    -- tr-products-1: CTR, product class membership.
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_a_minus
      FROM old_products AS o;
    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_a_plus
      FROM new_products AS n;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || o.product_id::text
               )),
               '[]'::jsonb
           )
      INTO v_s1
      FROM old_products AS o;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || n.product_id::text
               )),
               '[]'::jsonb
           )
      INTO v_s2
      FROM new_products AS n;

    PERFORM rdf_publish_rule_contribution(
        v_event_id,
        'tr-products-1',
        'pivot-relevant',
        'products',
        '[]'::jsonb,
        jsonb_build_object(
            'rule_type', 'CTR',
            'class_quad_template', jsonb_build_object(
                'predicate', 'rdf:type',
                'class', 'https://schema.org/Product',
                'graph', 'http://example.com/resource/tr/tr-products-1'
            )
        ),
        v_a_minus, v_a_plus, v_s1, v_s2
    );

    -- tr-products-2: Local-DTR, product title.
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_a_minus
      FROM old_products AS o;
    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_a_plus
      FROM new_products AS n;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || o.product_id::text,
                   'object', jsonb_build_object(
                       'value', o.title::text,
                       'datatype', 'http://www.w3.org/2001/XMLSchema#string'
                   )
               )),
               '[]'::jsonb
           )
      INTO v_s1
      FROM old_products AS o
     WHERE o.title IS NOT NULL;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || n.product_id::text,
                   'object', jsonb_build_object(
                       'value', n.title::text,
                       'datatype', 'http://www.w3.org/2001/XMLSchema#string'
                   )
               )),
               '[]'::jsonb
           )
      INTO v_s2
      FROM new_products AS n
     WHERE n.title IS NOT NULL;

    PERFORM rdf_publish_rule_contribution(
        v_event_id,
        'tr-products-2',
        'pivot-relevant',
        'products',
        '[]'::jsonb,
        jsonb_build_object(
            'rule_type', 'DTR',
            'datatype_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/name',
                'datatype', 'http://www.w3.org/2001/XMLSchema#string',
                'graph', 'http://example.com/resource/tr/tr-products-2'
            )
        ),
        v_a_minus, v_a_plus, v_s1, v_s2
    );

    -- tr-products-3: Local-DTR, product SKU.
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_a_minus
      FROM old_products AS o;
    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_a_plus
      FROM new_products AS n;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || o.product_id::text,
                   'object', jsonb_build_object('value', o.sku::text)
               )),
               '[]'::jsonb
           )
      INTO v_s1
      FROM old_products AS o
     WHERE o.sku IS NOT NULL;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || n.product_id::text,
                   'object', jsonb_build_object('value', n.sku::text)
               )),
               '[]'::jsonb
           )
      INTO v_s2
      FROM new_products AS n
     WHERE n.sku IS NOT NULL;

    PERFORM rdf_publish_rule_contribution(
        v_event_id,
        'tr-products-3',
        'pivot-relevant',
        'products',
        '[]'::jsonb,
        jsonb_build_object(
            'rule_type', 'DTR',
            'datatype_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/sku',
                'graph', 'http://example.com/resource/tr/tr-products-3'
            )
        ),
        v_a_minus, v_a_plus, v_s1, v_s2
    );

    -- tr-products-4: Local-DTR, product price.
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_a_minus
      FROM old_products AS o;
    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_a_plus
      FROM new_products AS n;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || o.product_id::text,
                   'object', jsonb_build_object(
                       'value', o.price::text,
                       'datatype', 'http://www.w3.org/2001/XMLSchema#decimal'
                   )
               )),
               '[]'::jsonb
           )
      INTO v_s1
      FROM old_products AS o
     WHERE o.price IS NOT NULL;
    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || n.product_id::text,
                   'object', jsonb_build_object(
                       'value', n.price::text,
                       'datatype', 'http://www.w3.org/2001/XMLSchema#decimal'
                   )
               )),
               '[]'::jsonb
           )
      INTO v_s2
      FROM new_products AS n
     WHERE n.price IS NOT NULL;

    PERFORM rdf_publish_rule_contribution(
        v_event_id,
        'tr-products-4',
        'pivot-relevant',
        'products',
        '[]'::jsonb,
        jsonb_build_object(
            'rule_type', 'DTR',
            'datatype_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/price',
                'datatype', 'http://www.w3.org/2001/XMLSchema#decimal',
                'graph', 'http://example.com/resource/tr/tr-products-4'
            )
        ),
        v_a_minus, v_a_plus, v_s1, v_s2
    );

    -- tr-products-5: OTR, product brand relationship.
    SELECT COALESCE(jsonb_agg(to_jsonb(o)), '[]'::jsonb)
      INTO v_a_minus
      FROM old_products AS o;
    SELECT COALESCE(jsonb_agg(to_jsonb(n)), '[]'::jsonb)
      INTO v_a_plus
      FROM new_products AS n;

    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || o.product_id::text,
                   'object', 'http://example.com' || m.id::text
               )),
               '[]'::jsonb
           )
      INTO v_s1
      FROM old_products AS o
      JOIN manufacturers AS m ON m.id = o.brand_id;

    SELECT COALESCE(
               jsonb_agg(jsonb_build_object(
                   'subject', 'http://example.com' || n.product_id::text,
                   'object', 'http://example.com' || m.id::text
               )),
               '[]'::jsonb
           )
      INTO v_s2
      FROM new_products AS n
      JOIN manufacturers AS m ON m.id = n.brand_id;

    PERFORM rdf_publish_rule_contribution(
        v_event_id,
        'tr-products-5',
        'pivot-relevant',
        'products',
        '[{"from":"products.brand_id","to":"manufacturers.id"}]'::jsonb,
        jsonb_build_object(
            'rule_type', 'OTR',
            'object_property_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/brand',
                'graph', 'http://example.com/resource/tr/tr-products-5',
                'subject_template', 'http://example.com⟨h⟩',
                'subject_placeholder_order', jsonb_build_array(
                    jsonb_build_object('relation', 'products', 'attribute', 'product_id')
                ),
                'object_template', 'http://example.com⟨h⟩',
                'object_placeholder_order', jsonb_build_array(
                    jsonb_build_object('relation', 'manufacturers', 'attribute', 'id')
                )
            )
        ),
        v_a_minus, v_a_plus, v_s1, v_s2
    );

    RETURN NULL;
END;
$$;


CREATE TRIGGER products_compute_changeset_after_update
AFTER UPDATE ON products
REFERENCING OLD TABLE AS old_products
            NEW TABLE AS new_products
FOR EACH STATEMENT
EXECUTE FUNCTION compute_changeset_products();
```

