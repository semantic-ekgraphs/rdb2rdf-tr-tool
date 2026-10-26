# Trigger Planning

This declarative plan covers the two relations that occur as pivots in the validated transformation rules: `manufacturers` and `products`. Each row describes one rule’s relevance to updates on the relation named in that section. No SQL is generated at this stage.

`compute_delta_pivot` indicates whether the pivot-relevant changeset contribution is required. Per Algorithm 1, that contribution includes deletions derived from the pre-update state and insertions derived from the post-update state. `compute_delta_plus` and `compute_delta_minus` indicate whether the final net insertion and deletion changesets are required, respectively.

## Relation: `manufacturers`

| relation | relevant_rules | rule_classification | multiple_path_occurrences | compute_a_minus | compute_a_plus | compute_s2 | compute_delta_pivot | compute_delta_rel | compute_delta_plus | compute_delta_minus |
|---|---|---|---|---|---|---|---|---|---|---|
| manufacturers | tr-manufacturers-1 | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| manufacturers | tr-manufacturers-2 | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| manufacturers | tr-manufacturers-3 | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| manufacturers | tr-products-5 | relation-relevant | No | Yes | Yes | Yes | No | Yes | Yes | Yes |

**Plan:** `Relev(manufacturers) = {tr-manufacturers-1, tr-manufacturers-2, tr-manufacturers-3, tr-products-5}`. The first three rules use `manufacturers` as their pivot. `tr-products-5` uses `manufacturers` in its relational path, joined from the `products` pivot via `products.brand_id = manufacturers.id`. That path contains one occurrence of `manufacturers`; it therefore requires affected-pivot analysis and post-update contribution comparison for the related product tuples.

## Relation: `products`

| relation | relevant_rules | rule_classification | multiple_path_occurrences | compute_a_minus | compute_a_plus | compute_s2 | compute_delta_pivot | compute_delta_rel | compute_delta_plus | compute_delta_minus |
|---|---|---|---|---|---|---|---|---|---|---|
| products | tr-products-1 | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| products | tr-products-2 | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| products | tr-products-3 | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| products | tr-products-4 | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |
| products | tr-products-5 | pivot-relevant | No | No | No | No | Yes | No | Yes | Yes |

**Plan:** `Relev(products) = {tr-products-1, tr-products-2, tr-products-3, tr-products-4, tr-products-5}`. All five rules use `products` as their pivot. `tr-products-5` also follows a path to `manufacturers`, but `products` occurs only once in that rule’s relational path, as its pivot relation. Updates to `products` therefore use the pivot-relevant contribution for this rule.

In this plan, **No** under `multiple_path_occurrences` means the updated relation does not occur more than once in the rule’s relational path.