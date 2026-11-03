# PostgreSQL AFTER Trigger Implementation Report

## 1. Synthesis Overview
- **Target Relation(s)**: `manufacturers` and `products`.
- **Architecture Compliance**: Both triggers are statement-level `AFTER UPDATE` triggers using `OLD TABLE` and `NEW TABLE` transition relations. Each trigger inserts one event into `rdf_maintenance_queue` and one rule-contribution row per relevant rule into `rdf_rule_contribution`. The trigger performs PostgreSQL-side maintenance only; it does not access SPARQL or GraphDB.
- **URI and graph construction**: The supplied subject templates are implemented by concatenating `http://example.com` with the relevant integer key. Rule graph URIs use the maintenance-queue convention `http://example.com/resource/tr/<rule_id>`.
- **Delta scope**: `DeltaPlus` contains the applicable pivot- or relation-side insertion contributions. The trigger does not calculate or apply final deletion changesets: the asynchronous worker is responsible for retrieving the prior GraphDB state and computing deletions. For relation-relevant `tr-products-5`, `DeltaPlusRel` excludes brand pairs also present through the deleted manufacturer tuples.
- **Schema assumptions**: The queue tables described in the supplied infrastructure already exist. The relational columns used below are those named in the validated metadata and transformation rules. Default product and manufacturer literals are represented as `xsd:string`, their RDF 1.1 datatype interpretation. The supplied metadata does not define an implementation of `hasURI`; the SQL therefore uses direct concatenation for the provided templates rather than inventing a database function.

## 4. Generated PostgreSQL AFTER Trigger Code

```sql
CREATE OR REPLACE FUNCTION compute_changeset_manufacturers()
RETURNS trigger
LANGUAGE plpgsql
AS $function$
DECLARE
    v_event_id bigint;
    v_deleted jsonb;
    v_inserted jsonb;
BEGIN
    SELECT COALESCE(jsonb_agg(to_jsonb(d)), '[]'::jsonb)
      INTO v_deleted
      FROM deleted_manufacturers AS d;

    SELECT COALESCE(jsonb_agg(to_jsonb(i)), '[]'::jsonb)
      INTO v_inserted
      FROM inserted_manufacturers AS i;

    INSERT INTO rdf_maintenance_queue
        (relation_name, operation_type, deleted_tuples, inserted_tuples)
    VALUES
        ('manufacturers', 'UPDATE', v_deleted, v_inserted)
    RETURNING event_id INTO v_event_id;

    /*
     * tr-manufacturers-1: CTR
     * DeltaPlusPivot contains only subjects not already emitted by the
     * deleted side of this update.
     */
    INSERT INTO rdf_rule_contribution
        (event_id, rule_id, rule_graph_uri, relevance_type,
         pivot_relation, path, rule_contribution)
    SELECT
        v_event_id,
        'tr-manufacturers-1',
        'http://example.com/resource/tr/tr-manufacturers-1',
        'pivot-relevant',
        'manufacturers',
        jsonb_build_object('relations', jsonb_build_array('manufacturers')),
        jsonb_build_object(
            'rule_id', 'tr-manufacturers-1',
            'rule_type', 'CTR',
            'pivot_relation', 'manufacturers',
            'class_quad_template', jsonb_build_object(
                'predicate', 'rdf:type',
                'class', 'https://schema.org/Organization',
                'graph', 'http://example.com/resource/tr/tr-manufacturers-1'
            ),
            'rdf_contributions', jsonb_build_object(
                'S2', '[]'::jsonb,
                'DeltaPlus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.id::text
                           ))
                    FROM inserted_manufacturers AS i
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM deleted_manufacturers AS d
                        WHERE 'http://example.com' || d.id::text
                            = 'http://example.com' || i.id::text
                    )
                ), '[]'::jsonb)
            )
        );

    /*
     * tr-manufacturers-2: DTR, schema:name.
     */
    INSERT INTO rdf_rule_contribution
        (event_id, rule_id, rule_graph_uri, relevance_type,
         pivot_relation, path, rule_contribution)
    SELECT
        v_event_id,
        'tr-manufacturers-2',
        'http://example.com/resource/tr/tr-manufacturers-2',
        'pivot-relevant',
        'manufacturers',
        jsonb_build_object('relations', jsonb_build_array('manufacturers')),
        jsonb_build_object(
            'rule_id', 'tr-manufacturers-2',
            'rule_type', 'DTR',
            'affected_tuples', jsonb_build_object(
                'A_minus', '[]'::jsonb,
                'A_plus', '[]'::jsonb
            ),
            'datatype_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/name',
                'datatype', 'http://www.w3.org/2001/XMLSchema#string',
                'graph', 'http://example.com/resource/tr/tr-manufacturers-2'
            ),
            'rdf_contributions', jsonb_build_object(
                'DeltaPlusPivot', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.id::text,
                               'object', i.name
                           ))
                    FROM inserted_manufacturers AS i
                    WHERE i.name IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_manufacturers AS d
                          WHERE d.id = i.id
                            AND d.name IS NOT DISTINCT FROM i.name
                      )
                ), '[]'::jsonb),
                'S2', '[]'::jsonb,
                'DeltaPlusRel', '[]'::jsonb,
                'DeltaPlus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.id::text,
                               'object', i.name
                           ))
                    FROM inserted_manufacturers AS i
                    WHERE i.name IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_manufacturers AS d
                          WHERE d.id = i.id
                            AND d.name IS NOT DISTINCT FROM i.name
                      )
                ), '[]'::jsonb)
            )
        );

    /*
     * tr-manufacturers-3: IRI-valued schema:url.
     */
    INSERT INTO rdf_rule_contribution
        (event_id, rule_id, rule_graph_uri, relevance_type,
         pivot_relation, path, rule_contribution)
    SELECT
        v_event_id,
        'tr-manufacturers-3',
        'http://example.com/resource/tr/tr-manufacturers-3',
        'pivot-relevant',
        'manufacturers',
        jsonb_build_object('relations', jsonb_build_array('manufacturers')),
        jsonb_build_object(
            'rule_id', 'tr-manufacturers-3',
            'rule_type', 'OTR',
            'affected_tuples', jsonb_build_object(
                'A_minus', '[]'::jsonb,
                'A_plus', '[]'::jsonb
            ),
            'object_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/url',
                'graph', 'http://example.com/resource/tr/tr-manufacturers-3'
            ),
            'rdf_contributions', jsonb_build_object(
                'DeltaPlusPivot', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.id::text,
                               'object', i.homepage
                           ))
                    FROM inserted_manufacturers AS i
                    WHERE i.homepage IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_manufacturers AS d
                          WHERE d.id = i.id
                            AND d.homepage IS NOT DISTINCT FROM i.homepage
                      )
                ), '[]'::jsonb),
                'S2', '[]'::jsonb,
                'DeltaPlusRel', '[]'::jsonb,
                'DeltaPlus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.id::text,
                               'object', i.homepage
                           ))
                    FROM inserted_manufacturers AS i
                    WHERE i.homepage IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_manufacturers AS d
                          WHERE d.id = i.id
                            AND d.homepage IS NOT DISTINCT FROM i.homepage
                      )
                ), '[]'::jsonb)
            )
        );

    /*
     * tr-products-5: relation-relevant when manufacturers is updated.
     * A_minus/A_plus identify affected product tuples. S2 is the post-update
     * brand contribution for products joined to inserted manufacturer rows.
     * DeltaPlusRel removes pairs already represented by deleted manufacturer
     * rows, so it records only newly introduced brand pairs.
     */
    INSERT INTO rdf_rule_contribution
        (event_id, rule_id, rule_graph_uri, relevance_type,
         pivot_relation, path, rule_contribution)
    SELECT
        v_event_id,
        'tr-products-5',
        'http://example.com/resource/tr/tr-products-5',
        'relation-relevant',
        'products',
        jsonb_build_object(
            'relations', jsonb_build_array('products', 'manufacturers'),
            'join', jsonb_build_object(
                'child_relation', 'products',
                'child_column', 'brand_id',
                'parent_relation', 'manufacturers',
                'parent_column', 'id'
            )
        ),
        jsonb_build_object(
            'rule_id', 'tr-products-5',
            'rule_type', 'OTR',
            'affected_tuples', jsonb_build_object(
                'A_minus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'product_id', p.product_id,
                               'brand_id', p.brand_id
                           ))
                    FROM products AS p
                    JOIN deleted_manufacturers AS d
                      ON p.brand_id = d.id
                ), '[]'::jsonb),
                'A_plus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'product_id', p.product_id,
                               'brand_id', p.brand_id
                           ))
                    FROM products AS p
                    JOIN inserted_manufacturers AS i
                      ON p.brand_id = i.id
                ), '[]'::jsonb)
            ),
            'object_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/brand',
                'graph', 'http://example.com/resource/tr/tr-products-5'
            ),
            'rdf_contributions', jsonb_build_object(
                'DeltaPlusPivot', '[]'::jsonb,
                'S2', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || p.product_id::text,
                               'object', 'http://example.com' || i.id::text
                           ))
                    FROM products AS p
                    JOIN inserted_manufacturers AS i
                      ON p.brand_id = i.id
                ), '[]'::jsonb),
                'DeltaPlusRel', COALESCE((
                    SELECT jsonb_agg(n.pair)
                    FROM (
                        SELECT DISTINCT jsonb_build_object(
                                   'subject', 'http://example.com' || p.product_id::text,
                                   'object', 'http://example.com' || i.id::text
                               ) AS pair,
                               p.product_id,
                               i.id AS manufacturer_id
                        FROM products AS p
                        JOIN inserted_manufacturers AS i
                          ON p.brand_id = i.id
                    ) AS n
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM products AS p_old
                        JOIN deleted_manufacturers AS d
                          ON p_old.brand_id = d.id
                        WHERE p_old.product_id = n.product_id
                          AND d.id = n.manufacturer_id
                    )
                ), '[]'::jsonb),
                'DeltaPlus', COALESCE((
                    SELECT jsonb_agg(n.pair)
                    FROM (
                        SELECT DISTINCT jsonb_build_object(
                                   'subject', 'http://example.com' || p.product_id::text,
                                   'object', 'http://example.com' || i.id::text
                               ) AS pair,
                               p.product_id,
                               i.id AS manufacturer_id
                        FROM products AS p
                        JOIN inserted_manufacturers AS i
                          ON p.brand_id = i.id
                    ) AS n
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM products AS p_old
                        JOIN deleted_manufacturers AS d
                          ON p_old.brand_id = d.id
                        WHERE p_old.product_id = n.product_id
                          AND d.id = n.manufacturer_id
                    )
                ), '[]'::jsonb)
            )
        );

    RETURN NULL;
END;
$function$;


CREATE TRIGGER manufacturers_after_update
AFTER UPDATE ON manufacturers
REFERENCING
    OLD TABLE AS deleted_manufacturers
    NEW TABLE AS inserted_manufacturers
FOR EACH STATEMENT
EXECUTE FUNCTION compute_changeset_manufacturers();


CREATE OR REPLACE FUNCTION compute_changeset_products()
RETURNS trigger
LANGUAGE plpgsql
AS $function$
DECLARE
    v_event_id bigint;
    v_deleted jsonb;
    v_inserted jsonb;
BEGIN
    SELECT COALESCE(jsonb_agg(to_jsonb(d)), '[]'::jsonb)
      INTO v_deleted
      FROM deleted_products AS d;

    SELECT COALESCE(jsonb_agg(to_jsonb(i)), '[]'::jsonb)
      INTO v_inserted
      FROM inserted_products AS i;

    INSERT INTO rdf_maintenance_queue
        (relation_name, operation_type, deleted_tuples, inserted_tuples)
    VALUES
        ('products', 'UPDATE', v_deleted, v_inserted)
    RETURNING event_id INTO v_event_id;

    /*
     * tr-products-1: CTR.
     */
    INSERT INTO rdf_rule_contribution
        (event_id, rule_id, rule_graph_uri, relevance_type,
         pivot_relation, path, rule_contribution)
    SELECT
        v_event_id,
        'tr-products-1',
        'http://example.com/resource/tr/tr-products-1',
        'pivot-relevant',
        'products',
        jsonb_build_object('relations', jsonb_build_array('products')),
        jsonb_build_object(
            'rule_id', 'tr-products-1',
            'rule_type', 'CTR',
            'pivot_relation', 'products',
            'class_quad_template', jsonb_build_object(
                'predicate', 'rdf:type',
                'class', 'https://schema.org/Product',
                'graph', 'http://example.com/resource/tr/tr-products-1'
            ),
            'rdf_contributions', jsonb_build_object(
                'S2', '[]'::jsonb,
                'DeltaPlus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.product_id::text
                           ))
                    FROM inserted_products AS i
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM deleted_products AS d
                        WHERE d.product_id = i.product_id
                    )
                ), '[]'::jsonb)
            )
        );

    /*
     * tr-products-2: DTR, schema:name from title.
     */
    INSERT INTO rdf_rule_contribution
        (event_id, rule_id, rule_graph_uri, relevance_type,
         pivot_relation, path, rule_contribution)
    SELECT
        v_event_id,
        'tr-products-2',
        'http://example.com/resource/tr/tr-products-2',
        'pivot-relevant',
        'products',
        jsonb_build_object('relations', jsonb_build_array('products')),
        jsonb_build_object(
            'rule_id', 'tr-products-2',
            'rule_type', 'DTR',
            'affected_tuples', jsonb_build_object(
                'A_minus', '[]'::jsonb,
                'A_plus', '[]'::jsonb
            ),
            'datatype_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/name',
                'datatype', 'http://www.w3.org/2001/XMLSchema#string',
                'graph', 'http://example.com/resource/tr/tr-products-2'
            ),
            'rdf_contributions', jsonb_build_object(
                'DeltaPlusPivot', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.product_id::text,
                               'object', i.title
                           ))
                    FROM inserted_products AS i
                    WHERE i.title IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_products AS d
                          WHERE d.product_id = i.product_id
                            AND d.title IS NOT DISTINCT FROM i.title
                      )
                ), '[]'::jsonb),
                'S2', '[]'::jsonb,
                'DeltaPlusRel', '[]'::jsonb,
                'DeltaPlus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.product_id::text,
                               'object', i.title
                           ))
                    FROM inserted_products AS i
                    WHERE i.title IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_products AS d
                          WHERE d.product_id = i.product_id
                            AND d.title IS NOT DISTINCT FROM i.title
                      )
                ), '[]'::jsonb)
            )
        );

    /*
     * tr-products-3: DTR, schema:sku.
     */
    INSERT INTO rdf_rule_contribution
        (event_id, rule_id, rule_graph_uri, relevance_type,
         pivot_relation, path, rule_contribution)
    SELECT
        v_event_id,
        'tr-products-3',
        'http://example.com/resource/tr/tr-products-3',
        'pivot-relevant',
        'products',
        jsonb_build_object('relations', jsonb_build_array('products')),
        jsonb_build_object(
            'rule_id', 'tr-products-3',
            'rule_type', 'DTR',
            'affected_tuples', jsonb_build_object(
                'A_minus', '[]'::jsonb,
                'A_plus', '[]'::jsonb
            ),
            'datatype_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/sku',
                'datatype', 'http://www.w3.org/2001/XMLSchema#string',
                'graph', 'http://example.com/resource/tr/tr-products-3'
            ),
            'rdf_contributions', jsonb_build_object(
                'DeltaPlusPivot', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.product_id::text,
                               'object', i.sku
                           ))
                    FROM inserted_products AS i
                    WHERE i.sku IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_products AS d
                          WHERE d.product_id = i.product_id
                            AND d.sku IS NOT DISTINCT FROM i.sku
                      )
                ), '[]'::jsonb),
                'S2', '[]'::jsonb,
                'DeltaPlusRel', '[]'::jsonb,
                'DeltaPlus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.product_id::text,
                               'object', i.sku
                           ))
                    FROM inserted_products AS i
                    WHERE i.sku IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_products AS d
                          WHERE d.product_id = i.product_id
                            AND d.sku IS NOT DISTINCT FROM i.sku
                      )
                ), '[]'::jsonb)
            )
        );

    /*
     * tr-products-4: DTR, schema:price.
     */
    INSERT INTO rdf_rule_contribution
        (event_id, rule_id, rule_graph_uri, relevance_type,
         pivot_relation, path, rule_contribution)
    SELECT
        v_event_id,
        'tr-products-4',
        'http://example.com/resource/tr/tr-products-4',
        'pivot-relevant',
        'products',
        jsonb_build_object('relations', jsonb_build_array('products')),
        jsonb_build_object(
            'rule_id', 'tr-products-4',
            'rule_type', 'DTR',
            'affected_tuples', jsonb_build_object(
                'A_minus', '[]'::jsonb,
                'A_plus', '[]'::jsonb
            ),
            'datatype_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/price',
                'datatype', 'http://www.w3.org/2001/XMLSchema#decimal',
                'graph', 'http://example.com/resource/tr/tr-products-4'
            ),
            'rdf_contributions', jsonb_build_object(
                'DeltaPlusPivot', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.product_id::text,
                               'object', i.price::text
                           ))
                    FROM inserted_products AS i
                    WHERE i.price IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_products AS d
                          WHERE d.product_id = i.product_id
                            AND d.price IS NOT DISTINCT FROM i.price
                      )
                ), '[]'::jsonb),
                'S2', '[]'::jsonb,
                'DeltaPlusRel', '[]'::jsonb,
                'DeltaPlus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.product_id::text,
                               'object', i.price::text
                           ))
                    FROM inserted_products AS i
                    WHERE i.price IS NOT NULL
                      AND NOT EXISTS (
                          SELECT 1
                          FROM deleted_products AS d
                          WHERE d.product_id = i.product_id
                            AND d.price IS NOT DISTINCT FROM i.price
                      )
                ), '[]'::jsonb)
            )
        );

    /*
     * tr-products-5: pivot-relevant when products is updated.
     * The foreign-key path is products.brand_id = manufacturers.id.
     */
    INSERT INTO rdf_rule_contribution
        (event_id, rule_id, rule_graph_uri, relevance_type,
         pivot_relation, path, rule_contribution)
    SELECT
        v_event_id,
        'tr-products-5',
        'http://example.com/resource/tr/tr-products-5',
        'pivot-relevant',
        'products',
        jsonb_build_object(
            'relations', jsonb_build_array('products', 'manufacturers'),
            'join', jsonb_build_object(
                'child_relation', 'products',
                'child_column', 'brand_id',
                'parent_relation', 'manufacturers',
                'parent_column', 'id'
            )
        ),
        jsonb_build_object(
            'rule_id', 'tr-products-5',
            'rule_type', 'OTR',
            'affected_tuples', jsonb_build_object(
                'A_minus', '[]'::jsonb,
                'A_plus', '[]'::jsonb
            ),
            'object_quad_template', jsonb_build_object(
                'predicate', 'https://schema.org/brand',
                'graph', 'http://example.com/resource/tr/tr-products-5'
            ),
            'rdf_contributions', jsonb_build_object(
                'DeltaPlusPivot', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.product_id::text,
                               'object', 'http://example.com' || m.id::text
                           ))
                    FROM inserted_products AS i
                    JOIN manufacturers AS m
                      ON m.id = i.brand_id
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM deleted_products AS d
                        JOIN manufacturers AS old_m
                          ON old_m.id = d.brand_id
                        WHERE d.product_id = i.product_id
                          AND 'http://example.com' || old_m.id::text
                              = 'http://example.com' || m.id::text
                    )
                ), '[]'::jsonb),
                'S2', '[]'::jsonb,
                'DeltaPlusRel', '[]'::jsonb,
                'DeltaPlus', COALESCE((
                    SELECT jsonb_agg(jsonb_build_object(
                               'subject', 'http://example.com' || i.product_id::text,
                               'object', 'http://example.com' || m.id::text
                           ))
                    FROM inserted_products AS i
                    JOIN manufacturers AS m
                      ON m.id = i.brand_id
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM deleted_products AS d
                        JOIN manufacturers AS old_m
                          ON old_m.id = d.brand_id
                        WHERE d.product_id = i.product_id
                          AND 'http://example.com' || old_m.id::text
                              = 'http://example.com' || m.id::text
                    )
                ), '[]'::jsonb)
            )
        );

    RETURN NULL;
END;
$function$;


CREATE TRIGGER products_after_update
AFTER UPDATE ON products
REFERENCING
    OLD TABLE AS deleted_products
    NEW TABLE AS inserted_products
FOR EACH STATEMENT
EXECUTE FUNCTION compute_changeset_products();
```