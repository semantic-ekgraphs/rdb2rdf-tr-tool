## Input validation failure: certified Rule URIs are missing

The supplied rule list provides rule IDs and triples-map IDs, but it does **not** provide the certified **Rule URI** for any of the eight rules. The specification requires that the certified URI be used unchanged as the named graph URI and `rdf_rule_contribution.rule_graph_uri`; it expressly prohibits constructing or substituting a URI when one is missing.

Therefore, validation fails for all eight rules. I cannot generate valid rule-contribution rows or executable `Compute_Changeset_R` functions and triggers without inventing graph URIs. The planning results below are still derivable from the supplied rules; the SQL synthesis is blocked until the eight certified Rule URIs are supplied.

## A) Analytical tables

### Updates on `manufacturers`

| Ψ | pivot(Ψ) | path(Ψ) | Type (pivot/relation) | Affected tuples | Justification |
|---|---|---|---|---|---|
| `tr-manufacturers-1` | `manufacturers` | No non-pivot relational path | pivot | Not applicable | Pivot-relevant because `pivot(Ψ) = manufacturers`. |
| `tr-manufacturers-2` | `manufacturers` | No non-pivot relational path | pivot | Not applicable | Pivot-relevant because `pivot(Ψ) = manufacturers`. |
| `tr-manufacturers-3` | `manufacturers` | No non-pivot relational path | pivot | Not applicable | Pivot-relevant because `pivot(Ψ) = manufacturers`. |
| `tr-products-5` | `products` | `products(d) → manufacturers(g)`, with `d.brand_id = g.id` | relation | `A−` and `A+` are the affected `products` pivot tuples connected to the deleted or inserted manufacturer tuple, respectively, by `brand_id = id`. | Relation-relevant: `manufacturers(g)` occurs in the rule body as the non-pivot target of the foreign-key path. The rule’s pivot relation is `products`, not `manufacturers`. |

### Updates on `products`

| Ψ | pivot(Ψ) | path(Ψ) | Type (pivot/relation) | Affected tuples | Justification |
|---|---|---|---|---|---|
| `tr-products-1` | `products` | No non-pivot relational path | pivot | Not applicable | Pivot-relevant because `pivot(Ψ) = products`. |
| `tr-products-2` | `products` | No non-pivot relational path | pivot | Not applicable | Pivot-relevant because `pivot(Ψ) = products`. |
| `tr-products-3` | `products` | No non-pivot relational path | pivot | Not applicable | Pivot-relevant because `pivot(Ψ) = products`. |
| `tr-products-4` | `products` | No non-pivot relational path | pivot | Not applicable | Pivot-relevant because `pivot(Ψ) = products`. |
| `tr-products-5` | `products` | `products(d) → manufacturers(g)`, with `d.brand_id = g.id` | pivot | Not applicable to relation relevance; pivot contributions are generated from inserted `products` tuples and the post-update `manufacturers` relation. | Pivot-relevant because `pivot(Ψ) = products`. The rule also has a non-pivot path to `manufacturers`, but that does not make it relation-relevant to updates on `products`: the `products(d)` occurrence is the pivot occurrence, and there is no second `products` occurrence. |

For `tr-products-5`, the maintenance-plan `relevance_type` is `"relation"` for updates on `manufacturers` and `"pivot"` for updates on `products`. None of the listed rules is both pivot- and relation-relevant to the same updated relation.

## B) PostgreSQL function `Compute_Changeset_R`

**Not generated:** the required graph URI for every relevant rule is absent. Generating the function would require inserting `rdf_rule_contribution.rule_graph_uri` values and embedding graph values in the quad templates. Supplying guessed or synthesized values would violate the stated Rule URI validation requirement.

## C) PostgreSQL triggers

**Not generated:** the triggers cannot produce the required, valid rule-contribution records without the certified Rule URIs. Please provide the exact Rule URI for each of the eight rule IDs; no replacement URI should be inferred.