# Transformation Rules Validation Report

## 1. Validation Summary
- **Overall Status**: `FAILED` (Inconsistencies Found).
- **Total Rules Evaluated**: 9
- **Compliance Rate**: 88.9% (8 out of 9 Transformation Rules fully match semantic specifications)

## 2. Audit Checklist & Consistency Analysis

### Rule Identifier: ctr-manufacturer-organization
- **Pivot Relation Audit**: PASS  
  The pivot relation `manufacturers` with primary key `id` is correctly identified.
- **Relational Path Audit**: PASS  
  No joins required; direct mapping from the `manufacturers` table.
- **URI Construction Functions**: PASS  
  URI template correctly uses `http://example.com⟨h1⟩` and the `id` field as placeholder.
- **Predicates & Selection Conditions**: PASS  
  RDF predicate `schema:Organization` correctly assigned; no selection conditions omitted.
- **Semantic Consistency Status**: PASS

### Rule Identifier: local-dtr-manufacturer-name
- **Pivot Relation Audit**: PASS  
  Pivot relation `manufacturers` with key `id` correctly used.
- **Relational Path Audit**: PASS  
  Accesses local attribute `name`—no joins needed.
- **URI Construction Functions**: PASS  
  Correct reuse of the manufacturer URI constructor.
- **Predicates & Selection Conditions**: PASS  
  Predicate `schema:name` and datatype `xsd:string` compliant; `nonNull` guard applied per R2RML `NOT NULL`.
- **Semantic Consistency Status**: PASS

### Rule Identifier: iri-attribute-manufacturer-url
- **Pivot Relation Audit**: PASS  
  Correct pivot `manufacturers` with key `id` for subject.
- **Relational Path Audit**: FAIL  
  The mapping has **no referenced pivot relation** for the object `homepage`; not supported as formal OTR.
- **URI Construction Functions**: FAIL  
  Object URI is constructed directly from an attribute value but lacks FK navigation and referenced pivot URI construction.
- **Predicates & Selection Conditions**: PASS  
  Predicate `schema:url` is aligned, and `nonNull` applied; however, semantic pattern violated.
- **Semantic Consistency Status**: FAIL  
  This is a non-conforming OTR candidate as per original R2RML semantics; it breaks entity-preservation and formal pattern rules for OTR.

### Rule Identifier: ctr-product-product
- **Pivot Relation Audit**: PASS  
  Pivot `products` keyed on `product_id` correctly identified.
- **Relational Path Audit**: PASS  
  No joins; direct use of `products`.
- **URI Construction Functions**: PASS  
  URI template correctly uses `product_id`.
- **Predicates & Selection Conditions**: PASS  
  `schema:Product` predicate properly assigned.
- **Semantic Consistency Status**: PASS

### Rule Identifier: local-dtr-product-name
- **Pivot Relation Audit**: PASS  
  Correct pivot relation `products` with key `product_id`.
- **Relational Path Audit**: PASS  
  Local attribute `title` accessed.
- **URI Construction Functions**: PASS  
  Correct URI reuse from `products`.
- **Predicates & Selection Conditions**: PASS  
  Predicate `schema:name`, datatype `xsd:string`, and `nonNull` condition correctly included.
- **Semantic Consistency Status**: PASS

### Rule Identifier: local-dtr-product-sku
- **Pivot Relation Audit**: PASS  
  Pivot relation correctly identified.
- **Relational Path Audit**: PASS  
  Local attribute access.
- **URI Construction Functions**: PASS  
  URI construction matches original.
- **Predicates & Selection Conditions**: PASS  
  Correct predicate `schema:sku`; datatype and selection condition consistent.
- **Semantic Consistency Status**: PASS

### Rule Identifier: local-dtr-product-price
- **Pivot Relation Audit**: PASS  
  Correctly identified `products` pivot.
- **Relational Path Audit**: PASS  
  Direct attribute usage.
- **URI Construction Functions**: PASS  
  URI consistent with product pivot.
- **Predicates & Selection Conditions**: PASS  
  Predicate `schema:price` with explicit decimal datatype and `nonNull`.
- **Semantic Consistency Status**: PASS

### Rule Identifier: otr-product-brand
- **Pivot Relation Audit**: PASS  
  Source pivot: `products` (product_id), referenced pivot: `manufacturers` (id) properly identified.
- **Relational Path Audit**: PASS  
  Foreign key navigation from `products.brand_id` → `manufacturers.id` correctly implemented.
- **URI Construction Functions**: PASS  
  Both source and target URI constructors conform.
- **Predicates & Selection Conditions**: PASS  
  Predicate `schema:brand` matches R2RML; `nonNull` condition on `brand_id` properly enforced.
- **Semantic Consistency Status**: PASS

## 3. Discrepancies & Feedback

- **Rule ID:** iri-attribute-manufacturer-url  
- **Detected Issue:**  
  This mapping attempts to construct an object IRI directly from the attribute `homepage` string value without a referenced pivot relation or foreign-key path, violating the formal definition of OTRs which require a proper referenced pivot and FK-navigation. It is neither a valid OTR nor a Local-DTR (despite object being an IRI). This breaks the pattern of entity preservation and mapping semantics as specified in the original R2RML.  
- **Required Correction:**  
  To achieve full semantic equivalence and satisfy formal OTR rules, either:  
  1. Map the `homepage` attribute as a literal-valued property by converting to a Local-DTR with `schema:url` predicate and literal object.  
  2. Introduce a new referenced entity and corresponding FK relation that backs the `homepage` URI as an object with a referenced pivot relation, enabling a valid OTR with the object URI constructed from that referenced entity.  
  The correction must enforce entity preservation and formal transformation rule definitions.

## 4. Final Validated Set of Transformation Rules

The following Transformation Rules are fully validated and semantically consistent with the original R2RML mappings and validated metadata:

- `ctr-manufacturer-organization`  
- `local-dtr-manufacturer-name`  
- `ctr-product-product`  
- `local-dtr-product-name`  
- `local-dtr-product-sku`  
- `local-dtr-product-price`  
- `otr-product-brand`  

**Note:** The `iri-attribute-manufacturer-url` rule is excluded from the valid final set due to semantic non-conformance and should be revised before production deployment.

---

*End of Transformation Rules Validation Report*