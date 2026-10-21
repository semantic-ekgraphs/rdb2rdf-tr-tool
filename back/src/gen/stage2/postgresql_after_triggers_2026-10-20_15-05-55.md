# PostgreSQL AFTER Trigger Implementation Report

## 1. Synthesis Overview
- **Target Relation(s)**: `manufacturers` and `products`.
- **Architecture Compliance**: The execution plan calls for statement-level `AFTER UPDATE` triggers using `REFERENCING OLD TABLE` and `REFERENCING NEW TABLE`, followed by population of the asynchronous maintenance queue. A production trigger implementation cannot be provided safely from the supplied context: the queue and contribution table definitions, their required JSON schemas, and the rule-to-named-graph URI mapping are not included. Inventing these contracts would violate the requirement not to hallucinate queue fields or RDF metadata.

## 2. Trigger Execution & Component Computation
- **Snapshot Capture**: For an update on either relation, the transition tables would supply the old and new statement snapshots, corresponding to the update’s \(\Delta^-\) and \(\Delta^+\). PostgreSQL exposes these tables to the trigger function under the names declared in the trigger’s `REFERENCING` clause.
- **Affected Deletion Tuples ($A^-[\Psi](u)$)**: For pivot-relevant rules, the old transition rows are the affected pivot tuples. For `tr-products-5` when `manufacturers` changes, affected products must be identified through the pre-update `products(brand_id) → manufacturers(id)` relationship.
- **Affected Insertion Tuples ($A^+[\Psi](u)$)**: For pivot-relevant rules, the new transition rows are the affected pivot tuples. For `tr-products-5` when `manufacturers` changes, affected products must be identified through the post-update relationship.
- **Post-Update Contributions ($S2[\Psi](u)$)**: The rules requiring post-update path evaluation are `tr-products-5` for updates to `manufacturers` and `products`. For manufacturer updates, this requires evaluating affected products against the post-update manufacturer state; for product updates, it requires evaluating the new product rows against the manufacturer relation.
- **Changesets Computation ($\Delta^+(u)$ and $\Delta^-(u)$)**: Algorithm 1 supplies the formal basis for relevance, affected tuples, and per-rule contributions. Algorithm 2’s asynchronous-worker operations must remain outside the trigger. The trigger-side final changesets must aggregate per-rule negative and positive RDF contributions, retaining rule provenance so contributions from separate rules are not conflated.

## 3. Asynchronous Maintenance Queue Integration
The supplied material names `rdf_maintenance_queue` and `rdf_rule_contribution`, but does not specify their columns, keys, constraints, required JSON structure, or enqueue interface. It also does not give the URI identifying the named graph for each rule. Consequently, the required serialization and queue insertion cannot be stated or verified against the actual infrastructure. Supplying guessed table columns, JSON keys, or graph URIs would not be a statically reliable integration.

To complete the queue integration, the necessary inputs are:
- DDL for `rdf_maintenance_queue` and `rdf_rule_contribution`, including required columns and constraints;
- the prescribed JSON schema or templates for rule contributions and changesets;
- the queue’s expected enqueue operation and worker-facing contract; and
- the named-graph URI for each transformation rule, plus the exact URI-template substitution and RDF literal serialization conventions.

## 4. Generated PostgreSQL AFTER Trigger Code
No trigger or PL/pgSQL function code is emitted. Without the queue contract and rule graph identifiers, any code that inserts into the queue would necessarily invent schema elements or RDF metadata, so it could not be represented as the requested production-ready, statically verified implementation.