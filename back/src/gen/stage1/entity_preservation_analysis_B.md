# Entity-Preservation Analisys

**Assessment basis:** Per the stated key assumption, `manufacturers.id` and `products.product_id` are treated as `SERIAL` primary keys; any `UUID` column is treated as unique. The extracted metadata does not show a UUID being used in either subject template. No selection conditions or transformation functions are specified.

| relation | pivot_relation | entity_preserving | uri_function | relational_path | issue | recommended_correction |
|---|---|---|---|---|---|---|
| `manufacturers` — class and local datatype-property mappings | `manufacturers` | **Yes for the class identity and local datatype properties.** The subject is rooted in the pivot tuple, and the `SERIAL` primary key makes the URI injective over tuples of this relation. `schema:name` is a local datatype property. | `URI_manufacturers(m,s) ≡ hasURI("http://example.com{h1}", ⟨m.id⟩, s)` | None for `schema:name`; it uses `manufacturers.name`. | The URI template is not relation-specific. If a product has the same identifier value, the manufacturer and product templates can generate the same IRI, potentially conflating distinct entities across the two relations. | Use distinct, stable relation-specific URI paths, for example `http://example.com/manufacturer/{id}`. A unique UUID may also be used as the placeholder if desired. |
| `manufacturers` — `schema:url` | `manufacturers` (subject pivot) | **Not established as entity-preserving under the specified TR patterns.** The mapping emits an IRI from `homepage`, but the metadata gives no pivot relation or FK path for that IRI. | Subject URI as above; object IRI is constructed from `homepage` using the column’s IRI term map. | None. `homepage` is a column on `manufacturers`, not a declared FK path to another pivot relation. | A value generated as an IRI is not, on the supplied schema evidence, an object corresponding to a related pivot tuple. The mapping is therefore not a validated OTR. Also, the metadata does not establish that every non-null `homepage` value is a valid IRI. | If `schema:url` is intended to be a literal URL value, map it as a literal with an appropriate datatype. If it is intended to link to an RDF entity, model that entity and its FK/path explicitly and define a target CTR; ensure values are valid IRIs. |
| `products` — class and local datatype-property mappings | `products` | **Yes for the class identity and local datatype properties.** The subject is rooted in the pivot tuple, and—under the stated key assumption—`product_id` is the `SERIAL` primary key, so distinct product tuples generate distinct subject IRIs. The local attributes support DTRs. | `URI_products(p,s) ≡ hasURI("http://example.com{h1}", ⟨p.product_id⟩, s)` | None for `schema:name`, `schema:sku`, or `schema:price`; they use `products.title`, `products.sku`, and `products.price`, respectively. | As with manufacturers, the shared URI pattern can collide across relations if `product_id` equals a manufacturer `id`. `sku` and `price` may be nullable; null values must not produce datatype-property triples. | Use a product-specific URI path, such as `http://example.com/product/{product_id}`. Preserve null suppression for nullable values. |
| `products` → `manufacturers` — `schema:brand` | Domain pivot: `products`; range pivot: `manufacturers` | **Yes, as an object-property mapping**, provided the stated FK is enforced. A product’s `brand_id` follows a schema-declared FK to the manufacturer pivot, whose subject URI is constructed from `manufacturers.id`. | Subject: `URI_products(p,s)`. Object: `URI_manufacturers(m,o)`. | `products(p) —[products.brand_id = manufacturers.id; FK products(brand_id) REFERENCES manufacturers(id)]→ manufacturers(m)` | The FK is unnamed, but its declared child and parent columns identify the path; a constraint name is not required. A nullable `brand_id` means some products have no path and consequently no `schema:brand` triple. | No structural correction is needed if the FK is enforced and `manufacturers.id` is the referenced key. Emit the OTR only for rows with a non-null, valid FK. |

## Transformation-rule forms

Let the URI constructors be:

- `URI_manufacturers(m,s) ≡ hasURI("http://example.com{h1}", ⟨m.id⟩, s)`
- `URI_products(p,s) ≡ hasURI("http://example.com{h1}", ⟨p.product_id⟩, s)`

The class transformation rules are:

```text
CTR-Manufacturer:
schema:Organization(s) ← manufacturers(m), URI_manufacturers(m,s)

CTR-Product:
schema:Product(s) ← products(p), URI_products(p,s)
```

The local datatype-property rules are:

```text
DTR-Manufacturer-Name:
schema:name(s,v) ← manufacturers(m), URI_manufacturers(m,s),
                    nonNull(m.name),
                    RDFLiteral(m.name,"name",manufacturers,v)

DTR-Product-Name:
schema:name(s,v) ← products(p), URI_products(p,s),
                    nonNull(p.title),
                    RDFLiteral(p.title,"title",products,v)

DTR-Product-SKU:
schema:sku(s,v) ← products(p), URI_products(p,s),
                   nonNull(p.sku),
                   RDFLiteral(p.sku,"sku",products,v)

DTR-Product-Price:
schema:price(s,v) ← products(p), URI_products(p,s),
                     nonNull(p.price),
                     RDFLiteral(p.price,"price",products,v)
```

The object-property rule for `schema:brand` is:

```text
OTR-Product-Brand:
schema:brand(s,o) ← products(p), URI_products(p,s),
                     manufacturers(m), URI_manufacturers(m,o),
                     FK(products.brand_id, manufacturers.id)(p,m)
```

**Overall finding:** The manufacturer and product class mappings preserve tuple identity within their respective pivot relations under the stated primary-key assumption. The local datatype-property mappings and FK-backed `schema:brand` mapping fit the entity-preserving patterns. The `schema:url` mapping is the identified structural exception: its IRI object is not grounded in a related pivot tuple or validated relational path. Distinct URI namespaces for the manufacturer and product pivots are also recommended to prevent cross-relation IRI collisions.