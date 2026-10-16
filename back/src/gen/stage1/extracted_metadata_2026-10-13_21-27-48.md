| triples_map_id | logical_table | transformation_function | selection_condition | subject_template | subject_class | rdf_predicate | object_source | object_source_type | datatype | term_type | object_template | child_column | parent_column | foreign_key |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `<#ManufacturerMapping>` | `manufacturers` | — | — | `http://example.com{id}` | `schema:Organization` | `rdf:type` | `schema:Organization` (class IRI) | — | — | `rr:IRI` | — | — | — | — |
| `<#ManufacturerMapping>` | `manufacturers` | — | — | `http://example.com{id}` | `schema:Organization` | `schema:name` | `name` | `VARCHAR(100) NOT NULL` | `xsd:string` | `rr:Literal` (default) | — | — | — | — |
| `<#ManufacturerMapping>` | `manufacturers` | — | — | `http://example.com{id}` | `schema:Organization` | `schema:url` | `homepage` | `VARCHAR(255)` | — | `rr:IRI` | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `rdf:type` | `schema:Product` (class IRI) | — | — | `rr:IRI` | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `schema:name` | `title` | `VARCHAR(150) NOT NULL` | — | `rr:Literal` (default) | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `schema:sku` | `sku` | `VARCHAR(50) UNIQUE` | — | `rr:Literal` (default) | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `schema:price` | `price` | `DECIMAL(10, 2)` | `xsd:decimal` | `rr:Literal` (default) | — | — | — | — |
| `<#ProductMapping>` | `products` | — | — | `http://example.com{product_id}` | `schema:Product` | `schema:brand` | `parentTriplesMap <#ManufacturerMapping>` | — | — | `rr:IRI` (default for referencing object map) | — | `brand_id` | `id` | — |

— indicates that the mapping does not specify a value for that field or it is not applicable. No transformation functions or selection conditions are present. The `brand_id` foreign key is declared in the schema without a named `CONSTRAINT`, so no constraint name is reported.