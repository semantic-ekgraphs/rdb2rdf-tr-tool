## Declarative incremental-maintenance plan

**Interpretation of the flags:** `A⁻` and `A⁺` identify affected pivot tuples before and after the update. `S2` is marked **Yes** when maintenance needs a post-update relational-path join; for rules without such a join, contributions can be derived directly from the affected tuples. `Delta+` and `Delta−` indicate whether positive and negative RDF contributions must be maintained. A flag indicates a component may be required; the resulting delta may be empty for a particular update.

### Relation: `manufacturers`

`Relev(manufacturers)` includes the three rules whose pivot is `manufacturers`, and `tr-products-5`, whose relational path references `manufacturers`.

| relation | relevant_rules | rule_classification | multiple_path_occurrences | compute_a_minus | compute_a_plus | compute_s2 | compute_delta_pivot | compute_delta_rel | compute_delta_plus | compute_delta_minus |
|---|---|---|---|---|---|---|---|---|---|---|
| manufacturers | tr-manufacturers-1 | pivot-relevant | No | Yes | Yes | No | Yes | No | Yes | Yes |
| manufacturers | tr-manufacturers-2 | pivot-relevant | No | Yes | Yes | No | Yes | No | Yes | Yes |
| manufacturers | tr-manufacturers-3 | pivot-relevant | No | Yes | Yes | No | Yes | No | Yes | Yes |
| manufacturers | tr-products-5 | relation-relevant | No | Yes | Yes | Yes | No | Yes | Yes | Yes |

**Plan notes:**
- `tr-manufacturers-1`, `tr-manufacturers-2`, and `tr-manufacturers-3` are maintained from affected manufacturer pivot tuples. The `schema:url` rule is included as supplied, despite being identified as a nonconforming OTR-shaped mapping.
- `tr-products-5` is affected through the `products(brand_id) → manufacturers(id)` path. Its maintenance requires identifying affected product pivots and evaluating the post-update path join. The path contains `manufacturers` once, so there are no multiple occurrences of this relation in the path.

### Relation: `products`

`Relev(products)` consists of the five rules whose pivot is `products`.

| relation | relevant_rules | rule_classification | multiple_path_occurrences | compute_a_minus | compute_a_plus | compute_s2 | compute_delta_pivot | compute_delta_rel | compute_delta_plus | compute_delta_minus |
|---|---|---|---|---|---|---|---|---|---|---|
| products | tr-products-1 | pivot-relevant | No | Yes | Yes | No | Yes | No | Yes | Yes |
| products | tr-products-2 | pivot-relevant | No | Yes | Yes | No | Yes | No | Yes | Yes |
| products | tr-products-3 | pivot-relevant | No | Yes | Yes | No | Yes | No | Yes | Yes |
| products | tr-products-4 | pivot-relevant | No | Yes | Yes | No | Yes | No | Yes | Yes |
| products | tr-products-5 | pivot-relevant | No | Yes | Yes | Yes | Yes | No | Yes | Yes |

**Plan notes:**
- The first four rules map product pivot tuples directly, so their contributions do not require a post-update relational-path join.
- `tr-products-5` is pivot-relevant when `products` changes. Its `manufacturers` path join is needed to determine the resulting `schema:brand` contributions. The path contains `products` once, so there are no multiple occurrences of this relation in the path.