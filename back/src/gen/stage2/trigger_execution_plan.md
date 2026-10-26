# Trigger Planning

This plan covers the eight rules in the **Final Validated Set**. “Yes” indicates that the component is required by the maintenance plan for that rule and relation; it does not mean the component will necessarily contain tuples for every update event. The relational path of `tr-products-5` contains one `manufacturers` occurrence.

## Relation: `manufacturers`

| relation | relevant_rules | rules | rule_classification | multiple_path_occurrences | compute_a_minus | compute_a_plus | compute_s2 | compute_delta_pivot | compute_delta_rel | compute_delta_plus | compute_delta_minus |
|---|---|---|---|---|---|---|---|---|---|---|---|
| manufacturers | tr-manufacturers-1 | `<https://schema.org/Organization>(s) ← manufacturers(r), URI_manufacturers(r,s)` | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| manufacturers | tr-manufacturers-2 | `<https://schema.org/name>(s,v) ← manufacturers(r), URI_manufacturers(r,s), nonNull(r.name), RDFLiteral(r.name,"name","manufacturers",v)` | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| manufacturers | tr-manufacturers-3 | `<https://schema.org/url>(s,o) ← manufacturers(r), URI_manufacturers(r,s), nonNull(r.homepage), RDFIRI(r.homepage,o)` | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| manufacturers | tr-products-5 | `<https://schema.org/brand>(s,o) ← products(d), URI_products(d,s), manufacturers(g), URI_manufacturers(g,o), FK_products_brand_id_manufacturers_id(d,g)` | relation-relevant | No | Yes | Yes | Yes | No | Yes | Yes | Yes |

## Relation: `products`

| relation | relevant_rules | rules | rule_classification | multiple_path_occurrences | compute_a_minus | compute_a_plus | compute_s2 | compute_delta_pivot | compute_delta_rel | compute_delta_plus | compute_delta_minus |
|---|---|---|---|---|---|---|---|---|---|---|---|
| products | tr-products-1 | `<https://schema.org/Product>(s) ← products(r), URI_products(r,s)` | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| products | tr-products-2 | `<https://schema.org/name>(s,v) ← products(r), URI_products(r,s), nonNull(r.title), RDFLiteral(r.title,"title","products",v)` | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| products | tr-products-3 | `<https://schema.org/sku>(s,v) ← products(r), URI_products(r,s), nonNull(r.sku), RDFLiteral(r.sku,"sku","products",v)` | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| products | tr-products-4 | `<https://schema.org/price>(s,v) ← products(r), URI_products(r,s), nonNull(r.price), RDFLiteral(r.price,"price","products",v)` | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| products | tr-products-5 | `<https://schema.org/brand>(s,o) ← products(d), URI_products(d,s), manufacturers(g), URI_manufacturers(g,o), FK_products_brand_id_manufacturers_id(d,g)` | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |

**Planning notes:** `Relev(manufacturers)` comprises `tr-manufacturers-1`, `tr-manufacturers-2`, `tr-manufacturers-3`, and `tr-products-5`. `Relev(products)` comprises `tr-products-1` through `tr-products-5`. The manufacturer rules are pivot-relevant for manufacturer updates; `tr-products-5` is relation-relevant for manufacturer updates and pivot-relevant for product updates. No relevant rule has multiple occurrences of the updated relation in its relational path.