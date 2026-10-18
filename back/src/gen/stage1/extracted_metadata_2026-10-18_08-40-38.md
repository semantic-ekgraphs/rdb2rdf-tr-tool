| triples_map_id | logical_table | transformation_function | selection_condition | subject_template | subject_class | rdf_predicate | object_source | object_source_type | attribute_condition | datatype | term_type | object_template | child_column | parent_column | foreign_key |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `<#ManufacturerMapping>` | `manufacturers` | — | — | `http://example.com{id}` | `schema:Organization` | `rdf:type` | `id` | `INT` | `PRIMARY KEY` | — | `rr:IRI` | — | — | — | — |
| `<#ManufacturerMapping>` | `manufacturers` | — | — | `http://example.com{id}` | `schema:Organization` | `schema:name` | `name` | `VARCHAR(100)` | `NOT NULL` | `xsd:string` | `rr:Literal` | — | — | — | — |
| `<#ManufacturerMapping>` | `manufacturers` | — | — | `http://example.com{id}` | `schema:Organization` | `schema:url` | `homepage` | `VARCHAR(255)` | — | — | `rr:IRI` | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `rdf:type` | `product_id` | `INT` | `PRIMARY KEY` | — | `rr:IRI` | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `schema:name` | `title` | `VARCHAR(150)` | `NOT NULL` | — | `rr:Literal` | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `schema:sku` | `sku` | `VARCHAR(50)` | `UNIQUE` | — | `rr:Literal` | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `schema:price` | `price` | `DECIMAL(10, 2)` | — | `xsd:decimal` | `rr:Literal` | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `schema:brand` | — | — | — | — | `rr:IRI` | — | `brand_id` | `id` | — |

No SQL transformation functions or selection conditions are specified. The `schema:brand` mapping joins `products.brand_id` to `manufacturers.id`; the supplied schema does not give that foreign key a constraint name, so `foreign_key` is left blank.