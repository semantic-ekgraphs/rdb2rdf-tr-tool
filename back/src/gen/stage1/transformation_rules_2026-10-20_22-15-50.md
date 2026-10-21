## Transformation Rule specification

### URI constructors

The subject templates are represented exactly as supplied. The shared, undelimited template is a potential cross-pivot IRI collision risk; the recommended relation-specific templates are noted below.

\[
\begin{aligned}
URI_{\text{manufacturers}}(r,s)
&\equiv
hasURI(\text{“http://example.com⟨h⟩”},\langle r.id\rangle,s)\\
URI_{\text{products}}(r,s)
&\equiv
hasURI(\text{“http://example.com⟨h⟩”},\langle r.product\_id\rangle,s)
\end{aligned}
\]

In the formulas, `nonNull(x)` represents R2RML’s omission of a triple when its source column is null. Literal datatype annotations are stated alongside the formulas; `RDFLiteral` follows the formalism’s signature.

| triples_map_id | rule_id | rule_type | pivot_relation | uri_constructor | entity_preservation | formula |
|---|---|---|---|---|---|---|
| `<http://example.com#ManufacturerMapping>` | `tr-manufacturers-1` | CTR | `manufacturers` | `URI_manufacturers(r,s) ≡ hasURI("http://example.com⟨h⟩", ⟨r.id⟩, s)` | **Yes.** The `manufacturers` primary key `id` supplies the subject identity. Distinct rows have distinct subjects within this pivot, assuming canonical integer instantiation. The shared template can collide with product IRIs across pivots, and its lack of a delimiter is a URI-template risk. | `<https://schema.org/Organization>(s) ← manufacturers(r), URI_manufacturers(r,s)` |
| `<http://example.com#ManufacturerMapping>` | `tr-manufacturers-2` | Local-DTR | `manufacturers` | `URI_manufacturers(r,s) ≡ hasURI("http://example.com⟨h⟩", ⟨r.id⟩, s)` | **Yes.** The property value comes directly from the pivot tuple’s `name` attribute; the subject identity is supplied by the PK-backed CTR. The value is emitted when non-null. | `<https://schema.org/name>(s,v) ← manufacturers(r), URI_manufacturers(r,s), nonNull(r.name), RDFLiteral(r.name,"name","manufacturers",v)`<br><br>`v` has datatype `xsd:string`. |
| `<http://example.com#ManufacturerMapping>` | `tr-manufacturers-3` | OTR (reification) | `manufacturers` | `URI_manufacturers(r,s) ≡ hasURI("http://example.com⟨h⟩", ⟨r.id⟩, s)` | **Yes, conditionally.** The manufacturer subject is PK-backed. The object is an IRI derived from the `homepage` value, not a resource generated from a target pivot relation. This follows the reification-OTR form identified in the supplied analysis; confirm that an IRI object is intended for `schema:url`. | `<https://schema.org/url>(s,o) ← manufacturers(r), URI_manufacturers(r,s), nonNull(r.homepage), RDFIRI(r.homepage,o)` |
| `<http://example.com#ProductMapping>` | `tr-products-1` | CTR | `products` | `URI_products(r,s) ≡ hasURI("http://example.com⟨h⟩", ⟨r.product_id⟩, s)` | **Yes.** The `products` primary key `product_id` supplies the subject identity. Distinct rows have distinct subjects within this pivot, assuming canonical integer instantiation. The shared template can collide with manufacturer IRIs across pivots, and its lack of a delimiter is a URI-template risk. | `<https://schema.org/Product>(s) ← products(r), URI_products(r,s)` |
| `<http://example.com#ProductMapping>` | `tr-products-2` | Local-DTR | `products` | `URI_products(r,s) ≡ hasURI("http://example.com⟨h⟩", ⟨r.product_id⟩, s)` | **Yes.** The property value comes directly from the pivot tuple’s `title` attribute; the subject identity is supplied by the PK-backed CTR. The value is emitted when non-null. | `<https://schema.org/name>(s,v) ← products(r), URI_products(r,s), nonNull(r.title), RDFLiteral(r.title,"title","products",v)`<br><br>The R2RML mapping does not specify a datatype; the default literal datatype for this SQL string value is `xsd:string`. |
| `<http://example.com#ProductMapping>` | `tr-products-3` | Local-DTR | `products` | `URI_products(r,s) ≡ hasURI("http://example.com⟨h⟩", ⟨r.product_id⟩, s)` | **Yes.** `sku` is a datatype value, not the subject identity. Its `UNIQUE` constraint does not replace `product_id` as the pivot key. The value is emitted when non-null. | `<https://schema.org/sku>(s,v) ← products(r), URI_products(r,s), nonNull(r.sku), RDFLiteral(r.sku,"sku","products",v)`<br><br>The R2RML mapping does not specify a datatype; the default literal datatype for this SQL string value is `xsd:string`. |
| `<http://example.com#ProductMapping>` | `tr-products-4` | Local-DTR | `products` | `URI_products(r,s) ≡ hasURI("http://example.com⟨h⟩", ⟨r.product_id⟩, s)` | **Yes.** The property value comes directly from the pivot tuple’s `price` attribute; the subject identity is supplied by the PK-backed CTR. The value is emitted when non-null. | `<https://schema.org/price>(s,v) ← products(r), URI_products(r,s), nonNull(r.price), RDFLiteral(r.price,"price","products",v)`<br><br>`v` has datatype `xsd:decimal`. |
| `<http://example.com#ProductMapping>` | `tr-products-5` | OTR (regular) | `products` | Subject: `URI_products(d,s) ≡ hasURI("http://example.com⟨h⟩", ⟨d.product_id⟩, s)`; object: `URI_manufacturers(g,o) ≡ hasURI("http://example.com⟨h⟩", ⟨g.id⟩, o)` | **Yes, assuming the declared foreign key is enforced.** The product is connected to a PK-identified manufacturer by the schema path `products(brand_id) → manufacturers(id)`. The supplied schema gives no constraint name; `FK_products_brand_id_manufacturers_id` is a descriptive alias only. | `<https://schema.org/brand>(s,o) ← products(d), URI_products(d,s), manufacturers(g), URI_manufacturers(g,o), FK_products_brand_id_manufacturers_id(d,g)`<br><br>The final body term is the relational path predicate, where `FK_products_brand_id_manufacturers_id(d,g)` holds iff `d.brand_id = g.id` for tuples related by the declared foreign key. |

### URI-template recommendation

To avoid the identified delimiter and cross-pivot collision risks, use distinct, delimited subject templates, for example:

- Manufacturers: `http://example.com/manufacturer/{id}`
- Products: `http://example.com/product/{product_id}`

For the `schema:url` rule, retain the IRI-valued mapping only if that object treatment is intended; otherwise map `homepage` as a literal.