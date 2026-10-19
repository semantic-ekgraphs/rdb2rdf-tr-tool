# Declarative Incremental-Maintenance Plans

No SQL is generated at this stage. The plans below cover the two pivot relations present in the transformation rules: `manufacturers` and `products`.

**Conventions**

- **Pivot-relevant** means the updated relation is the rule’s pivot relation.
- **Relation-relevant** means the updated relation occurs along a relational path used by the rule, but is not its pivot relation.
- \(A^-\) and \(A^+\) are the affected pre-update and post-update tuples, respectively, in the scope of the rule.
- \(S2\) denotes the rule contributions recomputed from the post-update state for the affected scope.
- \(\Delta^+_{\text{pivot}}\) and \(\Delta^+_{\text{rel}}\) denote candidate insertions attributable to pivot-side and relational-path changes, respectively. Final changesets must account for RDF set semantics and any overlap with already-present triples.
- `multiple_path_occurrences` is **Yes** only if the relation being analyzed occurs more than once in a rule’s relational path. The pivot at the start of a path is not counted as an additional path occurrence.

## Relation: `manufacturers`

### Relevant rules and classification

| relation | relevant_rules | rule_classification | multiple_path_occurrences |
|---|---|---|---|
| `manufacturers` | `tr-manufacturers-1` | pivot-relevant | No |
| `manufacturers` | `tr-manufacturers-2` | pivot-relevant | No |
| `manufacturers` | `tr-manufacturers-3` | pivot-relevant | No |
| `manufacturers` | `tr-products-5` | relation-relevant | No |

`tr-products-5` is relevant because `manufacturers` occurs as the referenced endpoint of the declared `products(brand_id) → manufacturers(id)` path. It occurs once on that path. `tr-manufacturers-3` is included as supplied: despite its nonconforming OTR-shaped label, its formula depends directly on a `manufacturers` pivot row and has no relational path.

### Maintenance components

| maintenance_components | Declarative plan |
|---|---|
| \(A^-\) | Pre-update manufacturer tuples affected by the statement, from the old image (`OLD TABLE` conceptually). These are the pivot tuples whose `tr-manufacturers-1`, `tr-manufacturers-2`, and `tr-manufacturers-3` contributions may need removal. Also identify product pivot tuples related to the old manufacturer image through `products.brand_id = manufacturers.id`, for the relation-relevant `tr-products-5` scope. |
| \(A^+\) | Post-update manufacturer tuples affected by the statement, from the new image (`NEW TABLE` conceptually). These are the pivot tuples whose manufacturer-rule contributions may need insertion. Also identify product pivot tuples related to the new manufacturer image through the declared FK path, for the relation-relevant `tr-products-5` scope. |
| \(S2\) | Post-update contributions for the affected scope: the manufacturer-rule outputs for \(A^+\), plus the `tr-products-5` outputs for affected product pivots joined to the post-update manufacturers through `products.brand_id = manufacturers.id`. The manufacturer rules use the supplied URI construction and mappings for `schema:Organization`, `schema:name`, and the direct `schema:url` mapping. |
| \(\Delta^+_{\text{pivot}}\) | Candidate post-update insertions produced by the pivot-relevant rules `tr-manufacturers-1`, `tr-manufacturers-2`, and `tr-manufacturers-3` from \(A^+\). |
| \(\Delta^+_{\text{rel}}\) | Candidate post-update insertions for `tr-products-5` attributable to the changed manufacturer endpoint, using affected product pivots and the post-update FK join. |
| \(\Delta^+\) | Final net insertion changeset for the relevant rules: contributions present after the update and absent before it, after set-semantic deduplication. It includes eligible insertions from both \(\Delta^+_{\text{pivot}}\) and \(\Delta^+_{\text{rel}}\). |
| \(\Delta^-\) | Final net deletion changeset for the relevant rules: contributions present before the update and absent after it, after set-semantic deduplication. It includes removals from the manufacturer pivot rules and any `tr-products-5` contributions invalidated by the changed manufacturer endpoint. |

## Relation: `products`

### Relevant rules and classification

| relation | relevant_rules | rule_classification | multiple_path_occurrences |
|---|---|---|---|
| `products` | `tr-products-1` | pivot-relevant | No |
| `products` | `tr-products-2` | pivot-relevant | No |
| `products` | `tr-products-3` | pivot-relevant | No |
| `products` | `tr-products-4` | pivot-relevant | No |
| `products` | `tr-products-5` | pivot-relevant | No |

There are no relation-relevant rules for `products`: no other rule’s relational path refers to `products`. In `tr-products-5`, `products` is the pivot, and it occurs only once; the path proceeds from that pivot to `manufacturers`.

### Maintenance components

| maintenance_components | Declarative plan |
|---|---|
| \(A^-\) | Pre-update product tuples affected by the statement. These are the pivot tuples whose contributions under `tr-products-1` through `tr-products-5` may need removal. |
| \(A^+\) | Post-update product tuples affected by the statement. These are the pivot tuples whose contributions under `tr-products-1` through `tr-products-5` may need insertion. |
| \(S2\) | Post-update contributions for \(A^+\): the product class and local datatype contributions, plus `tr-products-5` contributions where the post-update product tuple has a non-null `brand_id` matching a manufacturer through the declared FK path. |
| \(\Delta^+_{\text{pivot}}\) | Candidate post-update insertions produced by `tr-products-1` through `tr-products-5` from \(A^+\), with `tr-products-5` evaluated using the post-update manufacturer relation. |
| \(\Delta^+_{\text{rel}}\) | None for a products update: no relevant rule uses `products` as a non-pivot relation along its relational path. |
| \(\Delta^+\) | Final net insertion changeset for the relevant product rules: contributions present after the update and absent before it, after set-semantic deduplication. |
| \(\Delta^-\) | Final net deletion changeset for the relevant product rules: contributions present before the update and absent after it, after set-semantic deduplication. |