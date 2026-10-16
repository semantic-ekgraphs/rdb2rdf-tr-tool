# Generated Transformation Rules Report

## 1. Overview

The two TriplesMaps contain **8 triple-producing mapping assertions**: 2 class assertions and 6 property assertions. **Seven assertions compile** into entity-preserving Transformation Rules: 2 Class Transformation Rules (CTRs), 4 Local Datatype Transformation Rules (Local DTRs), and 1 Object Property Transformation Rule (OTR). No Path DTR is present.

The `schema:url` assertion is not compiled as a valid TR. Its object map produces an IRI from `manufacturers.homepage`, but the supplied schema identifies neither a target pivot relation nor a foreign-key path to one. It also does not meet the Local DTR pattern, which requires an RDF literal. Treating this assertion as an OTR or Local DTR would therefore be unsupported by the supplied metadata.

The URI constructors below preserve the subject templates as specified in the R2RML mappings:

```text
URI_manufacturers(m,s) ≡
  hasURI("http://example.com{h1}", ⟨m.id⟩, s)

URI_products(p,s) ≡
  hasURI("http://example.com{h1}", ⟨p.product_id⟩, s)
```

Under the stated primary-key assumption, each constructor is injective within its own pivot relation. Because both templates use the same URI pattern, an identifier shared across the two relations could produce a cross-relation IRI collision; relation-specific URI paths are recommended.

No selection conditions or transformation functions are specified. `nonNull` conditions are included where needed to suppress triples for nullable values.

## 2. Compiled Transformation Rules

### 2.1 Manufacturer class assertion

- **TriplesMap Identifier**: `<#ManufacturerMapping>`
- **Rule Identifier**: `ψ_manufacturer_class`
- **Rule Type**: `CTR` (Class Transformation Rule)
- **Pivot Relation**: `manufacturers`
- **Formal TR Specification**:

```text
ψ_manufacturer_class:
  schema:Organization(s) ←
    manufacturers(m),
    URI_manufacturers(m,s)
```

- **Relational Path**: None.

### 2.2 Manufacturer name

- **TriplesMap Identifier**: `<#ManufacturerMapping>`
- **Rule Identifier**: `ψ_manufacturer_name`
- **Rule Type**: `Local DTR` (Local Datatype Transformation Rule)
- **Pivot Relation**: `manufacturers`
- **Formal TR Specification**:

```text
ψ_manufacturer_name:
  schema:name(s,v) ←
    manufacturers(m),
    URI_manufacturers(m,s),
    nonNull(m.name),
    RDFLiteral(m.name,"name",manufacturers,v)
```

The R2RML mapping explicitly assigns `xsd:string` to this literal.

- **Relational Path**: None; `name` is an attribute of the pivot relation.

### 2.3 Manufacturer URL assertion — not compiled

- **TriplesMap Identifier**: `<#ManufacturerMapping>`
- **Rule Identifier**: None; no compliant TR is generated.
- **Rule Type**: Not classifiable as a valid `CTR`, `OTR`, `Local DTR`, or `Path DTR` from the supplied evidence.
- **Pivot Relation**: `manufacturers` is the subject pivot; no object pivot is identified.
- **Formal TR Specification**: None. A Local DTR would require an `RDFLiteral` result, while an OTR would require a target pivot and a validated relational path. The mapping instead converts `manufacturers.homepage` to an IRI, and no such target relation or path is supplied.
- **Relational Path**: None identified.

To compile this assertion as an OTR, the schema would need to identify the related entity and a valid FK path. If `schema:url` is intended to hold a literal URL value instead, the R2RML object map should produce a literal.

### 2.4 Product class assertion

- **TriplesMap Identifier**: `<#ProductMapping>`
- **Rule Identifier**: `ψ_product_class`
- **Rule Type**: `CTR` (Class Transformation Rule)
- **Pivot Relation**: `products`
- **Formal TR Specification**:

```text
ψ_product_class:
  schema:Product(s) ←
    products(p),
    URI_products(p,s)
```

- **Relational Path**: None.

### 2.5 Product name

- **TriplesMap Identifier**: `<#ProductMapping>`
- **Rule Identifier**: `ψ_product_name`
- **Rule Type**: `Local DTR` (Local Datatype Transformation Rule)
- **Pivot Relation**: `products`
- **Formal TR Specification**:

```text
ψ_product_name:
  schema:name(s,v) ←
    products(p),
    URI_products(p,s),
    nonNull(p.title),
    RDFLiteral(p.title,"title",products,v)
```

- **Relational Path**: None; `title` is an attribute of the pivot relation.

### 2.6 Product SKU

- **TriplesMap Identifier**: `<#ProductMapping>`
- **Rule Identifier**: `ψ_product_sku`
- **Rule Type**: `Local DTR` (Local Datatype Transformation Rule)
- **Pivot Relation**: `products`
- **Formal TR Specification**:

```text
ψ_product_sku:
  schema:sku(s,v) ←
    products(p),
    URI_products(p,s),
    nonNull(p.sku),
    RDFLiteral(p.sku,"sku",products,v)
```

- **Relational Path**: None; `sku` is an attribute of the pivot relation.

### 2.7 Product price

- **TriplesMap Identifier**: `<#ProductMapping>`
- **Rule Identifier**: `ψ_product_price`
- **Rule Type**: `Local DTR` (Local Datatype Transformation Rule)
- **Pivot Relation**: `products`
- **Formal TR Specification**:

```text
ψ_product_price:
  schema:price(s,v) ←
    products(p),
    URI_products(p,s),
    nonNull(p.price),
    RDFLiteral(p.price,"price",products,v)
```

The R2RML mapping explicitly assigns `xsd:decimal` to this literal.

- **Relational Path**: None; `price` is an attribute of the pivot relation.

### 2.8 Product brand

- **TriplesMap Identifier**: `<#ProductMapping>`
- **Rule Identifier**: `ψ_product_brand`
- **Rule Type**: `OTR` (Object Property Transformation Rule)
- **Pivot Relation**: Domain pivot: `products`; range pivot: `manufacturers`
- **Formal TR Specification**:

```text
ψ_product_brand:
  schema:brand(s,o) ←
    products(p),
    URI_products(p,s),
    manufacturers(m),
    URI_manufacturers(m,o),
    FK_brand(p,m)
```

where the final body predicate denotes the schema-validated relational path:

```text
FK_brand(p,m) ≡
  p.brand_id = m.id
  ∧ FK products(brand_id) REFERENCES manufacturers(id)
```

- **Relational Path**: `products(p) —[products.brand_id = manufacturers.id; FK products(brand_id) REFERENCES manufacturers(id)]→ manufacturers(m)`. The path is the final term in the rule body. The FK is unnamed; its declared columns identify the path. The rule yields no brand triple for a product with a null `brand_id` or without a matching referenced manufacturer.