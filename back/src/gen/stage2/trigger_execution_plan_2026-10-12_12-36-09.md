# Declarative Trigger Maintenance Plan

## 1. Scope and Formal Conventions

The supplied Transformation Rules identify three pivot relations: `artist`, `medium`, and `track`. Their subject URI identities are conditional on the corresponding URI-template attributes being unique and collision-free; the schema does not declare `artist.gid`, `medium.id`, or `track.id` unique.

Let \(V_1\) and \(V_2\) denote the database states before and after a statement affecting relation \(R\). For each relevant rule \(\psi\), let \(G_\psi(V)\) be the set of RDF triples produced by evaluating \(\psi\) in state \(V\). Define \(G(V)=\bigcup_\psi G_\psi(V)\) over the supplied rules.

For each update, define:

- \(A^-\): affected pivot tuples in the pre-update state \(V_1\).
- \(A^+\): affected pivot tuples in the post-update state \(V_2\).
- \(S2\): post-update rule contributions for affected pivots, evaluated against \(V_2\).
- \(\Delta^- = G(V_1)\setminus G(V_2)\) and \(\Delta^+ = G(V_2)\setminus G(V_1)\). The queue changesets are set differences; unaffected surviving support must be respected when RDF triples have multiple relational derivations.
- \(\Delta^+_{\text{pivot}}\): inserted CTR/class triples.
- \(\Delta^+_{\text{rel}}\): inserted DTR/OTR triples. Deletions are similarly partitioned into pivot and relation contributions when the queue requires that distinction.

No named graph or queue schema is specified, so the plan describes RDF triples, not quads or queue columns.

## 2. Relevant Relations Inventory

The following inventory covers every relation declared in the supplied schema. Relations with no listed rule or path occurrence have empty relevance and require no rule-derived maintenance computation.

| Relation | `relevant_rules` | `pivot_relevant_rules` | `relation_relevant_rules` | `multiple_path_occurrences` | `compute_a_minus` | `compute_a_plus` | `compute_s2` | `compute_delta_pivot` | `compute_delta_rel` | `compute_delta` |
|---|---|---|---|---|---|---|---|---|---|---|
| `artist` | `ψ_artist_01`, `ψ_artist_02`, `ψ_artist_03`, `ψ_artist_04`, `ψ_artist_14`, `ψ_artist_13`, `ψ_artist_07` | All listed rules | — | No rule path contains `artist` more than once; it occurs once as the pivot/path endpoint in the path rules | Yes | Yes | Yes | Yes | Yes | Yes |
| `artist_annotation` | `ψ_artist_13` | — | `ψ_artist_13` | No; once in its path | Yes | Yes | Yes | No | Yes | Yes |
| `l_artist_url` | `ψ_artist_14` (provisional candidate) | — | `ψ_artist_14` | No; once in the intended path | Yes | Yes | Yes, only provisionally until its path and joins are validated | No | Provisional only | Provisional only |
| `medium` | `ψ_medium_01`, `ψ_medium_05`, `ψ_medium_02` | All listed rules | — | No rule path contains `medium` | Yes | Yes | Yes | Yes | Yes | Yes |
| `track` | `ψ_track_01`, `ψ_track_02` | All listed rules | — | No rule path contains `track` | Yes | Yes | Yes | Yes | Yes | Yes |
| `alternative_medium` | ∅ | — | — | — | No | No | No | No | No | No |
| `alternative_track` | ∅ | — | — | — | No | No | No | No | No | No |
| `alternative_medium_track` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_alias_type` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_alias` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_attribute_type` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_attribute_type_allowed_value` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_attribute` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_ipi` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_isni` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_meta` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_tag` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_rating_raw` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_tag_raw` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_credit` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_credit_gid_redirect` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_credit_name` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_gid_redirect` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_type` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_release` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_release_nonva` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_release_va` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_release_pending_update` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_release_group` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_release_group_nonva` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_release_group_va` | ∅ | — | — | — | No | No | No | No | No | No |
| `artist_release_group_pending_update` | ∅ | — | — | — | No | No | No | No | No | No |
| `edit_artist` | ∅ | — | — | — | No | No | No | No | No | No |
| `editor_subscribe_artist` | ∅ | — | — | — | No | No | No | No | No | No |
| `editor_subscribe_artist_deleted` | ∅ | — | — | — | No | No | No | No | No | No |
| `editor_collection_artist` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_area_artist` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_artist` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_event` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_genre` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_instrument` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_label` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_mood` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_place` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_recording` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_release` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_release_group` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_series` | ∅ | — | — | — | No | No | No | No | No | No |
| `l_artist_work` | ∅ | — | — | — | No | No | No | No | No | No |
| `medium_attribute_type` | ∅ | — | — | — | No | No | No | No | No | No |
| `medium_attribute_type_allowed_format` | ∅ | — | — | — | No | No | No | No | No | No |
| `medium_attribute_type_allowed_value` | ∅ | — | — | — | No | No | No | No | No | No |
| `medium_attribute_type_allowed_value_allowed_format` | ∅ | — | — | — | No | No | No | No | No | No |
| `medium_attribute` | ∅ | — | — | — | No | No | No | No | No | No |
| `medium_cdtoc` | ∅ | — | — | — | No | No | No | No | No | No |
| `medium_format` | ∅ | — | — | — | No | No | No | No | No | No |
| `track_gid_redirect` | ∅ | — | — | — | No | No | No | No | No | No |
| `track_raw` | ∅ | — | — | — | No | No | No | No | No | No |
| `medium_index` | ∅ | — | — | — | No | No | No | No | No | No |

The rules also refer to `annotation`, `gender`, `link`, `link_type`, and `url`. These relations are **not declared** in the supplied schema, so they have no row among the schema relations above. They are nevertheless rule dependencies: updates to them would be relation-relevant to the rules identified below if those relations exist in the actual database.

## 3. Declarative Plans for Relations with Relevant Rules

# Declarative Trigger Maintenance Plan for Relation: `artist`

## 1. Relevant Rules Mapping (\(Relev(\texttt{artist})\))

- **Rule ID:** \(\psi_{\text{artist\_01}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** No relational path; local pivot rule.

- **Rule ID:** \(\psi_{\text{artist\_02}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** No relational path; local DTR.

- **Rule ID:** \(\psi_{\text{artist\_03}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** No relational path; local DTR.

- **Rule ID:** \(\psi_{\text{artist\_04}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** No relational path; local DTR.

- **Rule ID:** \(\psi_{\text{artist\_14}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** Once, as the starting pivot of the intended path through `l_artist_url`. This is a provisional OTR candidate, not a verified framework-conforming OTR.

- **Rule ID:** \(\psi_{\text{artist\_13}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** Once, as the starting pivot of the path through `artist_annotation` to `annotation`.

- **Rule ID:** \(\psi_{\text{artist\_07}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** Once, as the starting pivot of the FK path to `gender`.

**Multiple occurrences:** No rule path contains `artist` more than once.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\)):** The distinct `artist` tuples represented by the statement’s old row set, interpreted in \(V_1\). If an update changes a tuple’s pivot identity or URI-generating value, the old tuple/resource is included.
- **Affected Pivot Tuples for Insertion (\(A^+\)):** The distinct `artist` tuples represented by the statement’s new row set, interpreted in \(V_2\).
- **Post-Update Contributions (\(S2\)):** Evaluate all seven relevant rules in \(V_2\) for affected artist pivots in \(A^-\cup A^+\). This includes the class triple, local GUID/name/sort-label triples, and the path-rule contributions available in \(V_2\). The \(\psi_{\text{artist\_14}}\) contribution remains provisional until its path and OTR prerequisites are validated.
- **Deletion and Insertion Changesets (\(\Delta^-\) and \(\Delta^+\)):** Compare the complete pre- and post-update rule outputs, restricted to the affected-pivot maintenance region but accounting for surviving support from unaffected derivations. Class triples belong to the pivot component; local DTR, Path-DTR, and candidate OTR triples belong to the relation component.
  - Compute \(\Delta^+_{\text{pivot}}\) from newly supported \(\texttt{mo:MusicArtist}(s)\) triples.
  - Compute \(\Delta^+_{\text{rel}}\) from newly supported GUID, name, sort-label, annotation, gender, and—only if validated—candidate `owl:sameAs` triples.
  - Record \(\Delta^-\) and \(\Delta^+\) as the final net RDF triple differences, not merely the row-level derivation differences.

# Declarative Trigger Maintenance Plan for Relation: `artist_annotation`

## 1. Relevant Rules Mapping (\(Relev(\texttt{artist\_annotation})\))

- **Rule ID:** \(\psi_{\text{artist\_13}}\)  
  **Relevance Classification:** `relation-relevant`  
  **Relational Path Occurrences:** Once, in the path `artist.id → artist_annotation.artist → artist_annotation.annotation → annotation.id`.

**Multiple occurrences:** No; `artist_annotation` occurs once in the rule path.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\)):** Artist pivots in \(V_1\) whose `artist.id` is connected through an old `artist_annotation` row to an annotation tuple contributing to \(\psi_{\text{artist\_13}}\). For deletion or update, use the old association row and pre-update path state.
- **Affected Pivot Tuples for Insertion (\(A^+\)):** Artist pivots in \(V_2\) connected through a new `artist_annotation` row to an annotation tuple contributing to \(\psi_{\text{artist\_13}}\). For insertion or update, use the new association row and post-update path state.
- **Post-Update Contributions (\(S2\)):** For affected artist pivots in \(V_2\), evaluate \(\psi_{\text{artist\_13}}\): produce `rdfs:comment` triples only where the connected annotation has non-null `text`, using the specified `RDFLiteral` mapping.
- **Deletion and Insertion Changesets (\(\Delta^-\) and \(\Delta^+\)):** Compute the net difference of the annotation-comment triples supported before and after the association change, including support checks for duplicate derivations. This rule contributes to \(\Delta_{\text{rel}}\), not \(\Delta_{\text{pivot}}\).

**Schema validation:** `artist_annotation` and its FK to `artist` are declared. The `annotation` relation and the annotation-side FK are not declared in the supplied schema. The path cannot be fully validated or synthesized until that relation, its join key, and the FK are supplied.

# Declarative Trigger Maintenance Plan for Relation: `l_artist_url`

## 1. Relevant Rules Mapping (\(Relev(\texttt{l\_artist\_url})\))

- **Rule ID:** \(\psi_{\text{artist\_14}}\)  
  **Relevance Classification:** `relation-relevant`  
  **Relational Path Occurrences:** Once, in the intended path from `artist.id` through `l_artist_url` toward `link`, `link_type`, and `url`.

**Multiple occurrences:** No; `l_artist_url` occurs once in the intended path.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\)):** Artist pivots reached through old `l_artist_url` rows in \(V_1\), using the old row’s `entity0` and the remainder of the old path when determining whether the mapping selection condition holds.
- **Affected Pivot Tuples for Insertion (\(A^+\)):** Artist pivots reached through new `l_artist_url` rows in \(V_2\), using the new row’s `entity0` and the remainder of the post-update path when determining whether the mapping selection condition holds.
- **Post-Update Contributions (\(S2\)):** Provisional evaluation of the candidate `owl:sameAs` rule in \(V_2\) for affected artists, including the stated DBpedia selection condition and URL transformation. Do not treat this as a verified OTR contribution.
- **Deletion and Insertion Changesets (\(\Delta^-\) and \(\Delta^+\)):** Provisional net changes to candidate `owl:sameAs` triples, with support checks. No validated \(\Delta_{\text{pivot}}\) contribution is required for this rule; any relation changeset remains provisional until OTR conformance and path validity are established.

**Schema validation:** The FK `l_artist_url_fk_entity0` is declared, but the remaining path constraints are not. The rule report also identifies an ambiguous or erroneous `link_type` join and does not establish a target pivot relation or target CTR for the transformed external IRI. Therefore, a verified changeset for this rule cannot be finalized from the supplied information.

# Declarative Trigger Maintenance Plan for Relation: `medium`

## 1. Relevant Rules Mapping (\(Relev(\texttt{medium})\))

- **Rule ID:** \(\psi_{\text{medium\_01}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** No relational path; local pivot rule.

- **Rule ID:** \(\psi_{\text{medium\_05}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** No relational path; local DTR.

- **Rule ID:** \(\psi_{\text{medium\_02}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** No relational path; local DTR.

**Multiple occurrences:** No rule path contains `medium`.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\)):** The distinct `medium` tuples represented by the old row set in \(V_1\).
- **Affected Pivot Tuples for Insertion (\(A^+\)):** The distinct `medium` tuples represented by the new row set in \(V_2\).
- **Post-Update Contributions (\(S2\)):** Evaluate the medium CTR and both local DTRs in \(V_2\) for affected pivots. The DTR outputs are conditional on the specified non-null tests.
- **Deletion and Insertion Changesets (\(\Delta^-\) and \(\Delta^+\)):** Compute the final net difference for `mo:Record` class triples and `dc:title` and `mo:track_count` datatype triples. The class triple is the pivot component; datatype triples are the relation component. Account for the conditional `medium.id` URI-identity guarantee and surviving support.

# Declarative Trigger Maintenance Plan for Relation: `track`

## 1. Relevant Rules Mapping (\(Relev(\texttt{track})\))

- **Rule ID:** \(\psi_{\text{track\_01}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** No relational path; local pivot rule.

- **Rule ID:** \(\psi_{\text{track\_02}}\)  
  **Relevance Classification:** `pivot-relevant`  
  **Relational Path Occurrences:** No relational path; local DTR.

**Multiple occurrences:** No rule path contains `track`.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\)):** The distinct `track` tuples represented by the old row set in \(V_1\).
- **Affected Pivot Tuples for Insertion (\(A^+\)):** The distinct `track` tuples represented by the new row set in \(V_2\).
- **Post-Update Contributions (\(S2\)):** Evaluate the track CTR and \(\psi_{\text{track\_02}}\) in \(V_2\) for affected pivots. Emit the datatype contribution only when the stated `position` non-null condition holds.
- **Deletion and Insertion Changesets (\(\Delta^-\) and \(\Delta^+\)):** Compute the final net difference for `mo:Track` class triples and `mo:track_number` datatype triples. The class triple is the pivot component; the datatype triple is the relation component. Preserve the rule’s declared `xsd:nonNegativeInteger` datatype requirement; the schema’s `INTEGER NOT NULL` declaration does not establish that all values are nonnegative, and the URI-identity guarantee for `track.id` is conditional.

## 4. Dependencies Mentioned by Rules but Absent from the Supplied Schema

These are not declared relations in the supplied schema, but their rule paths make them relevant dependencies if present in the actual database:

| Relation | Relevant rule(s) | Classification | Path occurrences | Maintenance-plan status |
|---|---|---|---|---|
| `annotation` | \(\psi_{\text{artist\_13}}\) | `relation-relevant` | Once | Cannot fully validate: relation and annotation-side FK are absent. |
| `gender` | \(\psi_{\text{artist\_07}}\) | `relation-relevant` | Once | Cannot fully validate or synthesize from the supplied schema: relation definition and FK target are absent. |
| `link` | \(\psi_{\text{artist\_14}}\) | `relation-relevant` | Once in the intended path | Candidate rule only; relation definition and complete path constraints are absent. |
| `link_type` | \(\psi_{\text{artist\_14}}\) | `relation-relevant` | Once in the intended path | Candidate rule only; relation definition is absent and the reported join is ambiguous or erroneous. |
| `url` | \(\psi_{\text{artist\_14}}\) | `relation-relevant` | Once in the intended path | Candidate rule only; relation definition, URL type, and complete path constraints are absent. |

Until these dependencies and the candidate OTR’s missing target-pivot/CTR correspondence are resolved, they must not be treated as validated trigger-maintenance plans.