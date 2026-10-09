# Declarative Trigger Maintenance Plan

## Scope and notation

The supplied Transformation Rules mention the following relations as rule pivots or relational-path participants: `artist`, `artist_annotation`, `annotation`, `gender`, `l_artist_url`, `link`, `link_type`, `url`, `medium`, and `track`. The supplied schema excerpt does not define `annotation`, `gender`, `link`, `link_type`, or `url`; their relevance below follows the rule metadata, but their schema-level joins cannot be independently verified from the excerpt.

For a rule \(\psi\), let \(M_\psi(V,A)\) denote the rule’s RDF quads produced in database state \(V\) for the affected pivot set \(A\), respecting the rule’s selection condition and named graph. Let \(V_1\) and \(V_2\) be the pre-update and post-update states. Within the affected scope, compute:

- \(S1 = M_\psi(V_1,A^-)\): pre-update contributions for affected old-side pivots.
- \(S2 = M_\psi(V_2,A^+)\): post-update contributions for affected new-side pivots.
- \(\Delta^- = S1 \setminus S2\) and \(\Delta^+ = S2 \setminus S1\).

These are set differences of RDF quads, including the rule’s named graph. For relation-relevant rules, the affected pivot sets are obtained by traversing the rule’s specified path from the changed relation tuples in the corresponding state. For rules whose required URI construction or path join is unresolved, the affected scope can be identified, but the RDF contribution cannot be completed without that missing metadata.

## Relations not listed below

Every other relation in the supplied schema has \(Relev(R)=\varnothing\) under the supplied Transformation Rules. No rule-specific \(A^-\), \(A^+\), \(S2\), \(\Delta^-\), or \(\Delta^+\) computation is required for updates to those relations under this rule set.

# Declarative Trigger Maintenance Plan for Relation: `artist`

## 1. Relevant Rules Mapping (\(Relev(artist)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `ctr-artist-01` | `pivot-relevant` | No relational path; pivot only. |
| `dtr-artist-guid-01` | `pivot-relevant` | No relational path; pivot only. |
| `dtr-artist-name-01` | `pivot-relevant` | No relational path; pivot only. |
| `dtr-artist-sort-label-01` | `pivot-relevant` | No relational path; pivot only. |
| `otr-artist-dbpedia-01` | `pivot-relevant` | One occurrence of `artist` in the stated path. |
| `dtr-artist-annotation-01` | `pivot-relevant` | One occurrence of `artist` as the path’s pivot endpoint. |
| `dtr-artist-gender-01` | `pivot-relevant` | One occurrence of `artist` as the path’s pivot endpoint. |

The DBpedia-shaped rule is not validated as a framework-conforming OTR, and its subject URI is unresolved. The annotation and gender rules also have unresolved subject URI construction.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `artist` tuples from the update’s pre-state. For each rule, retain tuples that produced a contribution in \(V_1\), including the rule’s selection condition and required path match. For the three local DTRs, apply the corresponding `nonNull` condition; the schema declares `gid`, `name`, and `sort_name` `NOT NULL`.
- **Affected Pivot Tuples for Insertion (\(A^+\))**: New `artist` tuples from the post-state. Re-evaluate each rule’s selection condition and path match in \(V_2\).
- **Post-Update Contributions (\(S2\))**: Evaluate each rule over \(V_2\) for \(A^+\). The local DTR contributions use the specified URI constructor and literal conversion. The annotation and gender contributions require their stated paths and `nonNull` conditions. The DBpedia-shaped contribution remains blocked from complete synthesis until its subject URI is supplied; the `link_type` join also requires validation.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: For each rule, compare its old contributions for \(A^-\) with its post-update contributions for \(A^+\): \(\Delta^- = S1 \setminus S2\), \(\Delta^+ = S2 \setminus S1\). Include the rule’s specified named graph. Do not construct unresolved subject URIs or assume missing joins.

# Declarative Trigger Maintenance Plan for Relation: `artist_annotation`

## 1. Relevant Rules Mapping (\(Relev(artist\_annotation)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `dtr-artist-annotation-01` | `relation-relevant` | One occurrence; `artist_annotation` is the bridge relation in the stated path. |

The path traverses from `artist` through the inverse of `artist_annotation_fk_artist`, then from `artist_annotation.annotation` to `annotation.id`. The annotation join is described in the rule metadata, but its FK constraint name is not supplied.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `artist` pivots reached from `OLD artist_annotation` rows by the inverse traversal of `artist_annotation_fk_artist`, with the old path continuing to a matching `annotation` row in \(V_1\). Retain pivots whose old annotation text satisfies `nonNull(a.text)`.
- **Affected Pivot Tuples for Insertion (\(A^+\))**: `artist` pivots reached from `NEW artist_annotation` rows by the same stated bridge traversal and joined to `annotation` in \(V_2\). Retain pivots whose post-update annotation text satisfies `nonNull(a.text)`.
- **Post-Update Contributions (\(S2\))**: Evaluate `dtr-artist-annotation-01` in \(V_2\) for \(A^+\), using `RDFLiteral(a.text, "text", annotation, v, xsd:string)` and the rule’s named graph. The subject URI remains unresolved because the supplied definition of `lb:sm_artist` is missing.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: Compare old rule contributions for \(A^-\) with post-update contributions for \(A^+\). The path and affected pivots are specified, but complete RDF quads cannot be formed until the subject URI is supplied.

# Declarative Trigger Maintenance Plan for Relation: `annotation`

## 1. Relevant Rules Mapping (\(Relev(annotation)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `dtr-artist-annotation-01` | `relation-relevant` | One occurrence; `annotation` is the path’s terminal relation. |

`annotation` is referenced by the rule but is not defined in the supplied schema excerpt. The stated join is `artist_annotation.annotation → annotation.id`; its FK constraint name is not supplied.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `artist` pivots reached from old `annotation` tuples by traversing the stated join in \(V_1\), including the bridge through `artist_annotation`. Retain only pivots whose old annotation text satisfies `nonNull(a.text)`.
- **Affected Pivot Tuples for Insertion (\(A^+\))**: `artist` pivots reached from new `annotation` tuples by the same stated path in \(V_2\). Retain only pivots whose post-update annotation text satisfies `nonNull(a.text)`.
- **Post-Update Contributions (\(S2\))**: Evaluate the annotation DTR in \(V_2\) for \(A^+\), using the supplied literal conversion and named graph. Its subject URI is unresolved.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: Compare the old and post-update annotation-rule contributions within the affected scope. Do not infer an FK constraint or subject URI not established by the supplied metadata.

# Declarative Trigger Maintenance Plan for Relation: `gender`

## 1. Relevant Rules Mapping (\(Relev(gender)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `dtr-artist-gender-01` | `relation-relevant` | One occurrence; `gender` is the path’s referenced relation. |

The rule specifies `artist.gender → gender.id` via `artist_fk_gender`. `gender` is referenced by the rule but is not defined in the supplied schema excerpt.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `artist` pivots whose old `gender` value joins to an old `gender` tuple through the stated FK path in \(V_1\), and whose `LOWER(g.name)` satisfies `nonNull`.
- **Affected Pivot Tuples for Insertion (\(A^+\))**: `artist` pivots whose post-update `gender` value joins to a post-update `gender` tuple through the stated path in \(V_2\), and whose `LOWER(g.name)` satisfies `nonNull`.
- **Post-Update Contributions (\(S2\))**: Evaluate the rule in \(V_2\) for \(A^+\), applying `RDFLiteral(LOWER(g.name), "gender", gender, v, xsd:string)` and the rule’s named graph. The subject URI remains unresolved.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: Compare old and post-update contributions in the affected scope. Do not construct complete quads until the subject URI definition is supplied.

# Declarative Trigger Maintenance Plan for Relation: `l_artist_url`

## 1. Relevant Rules Mapping (\(Relev(l\_artist\_url)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `otr-artist-dbpedia-01` | `relation-relevant` | One occurrence; `l_artist_url` is traversed from `artist` to `url`. |

The supplied path uses `artist.id → l_artist_url.entity0` and `l_artist_url.link → link.id`, then the stated `link_type` and `url` joins. Only `l_artist_url_fk_entity0` is supplied as a matching FK name. The rule’s subject URI is unresolved, and the mapping is not validated as an entity-preserving OTR.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `artist` pivots reached from `OLD l_artist_url` rows through `l_artist_url.entity0` in \(V_1\). Restrict the old rule contribution to rows satisfying the stated `link_type.gid` and `url SIMILAR TO` selection conditions, using only validated path joins.
- **Affected Pivot Tuples for Insertion (\(A^+\))**: `artist` pivots reached from `NEW l_artist_url` rows through `l_artist_url.entity0` in \(V_2\). Apply the same selection conditions and path-join validation in the post-state.
- **Post-Update Contributions (\(S2\))**: The stated object conversion is `RDFIRI(REPLACE(REPLACE(url, "wikipedia.org/wiki", "dbpedia.org/resource"), "http://en.", "http://"), o)`. The subject URI is unresolved. The `link_type` join cannot be independently validated from the supplied SQL expression and FK metadata.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: Compare old and post-update rule contributions only after the subject URI and required joins are resolved. Do not infer missing FK constraints or treat this OTR-shaped rule as a validated entity-preserving OTR.

# Declarative Trigger Maintenance Plan for Relation: `link`

## 1. Relevant Rules Mapping (\(Relev(link)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `otr-artist-dbpedia-01` | `relation-relevant` | One occurrence; `link` is traversed between `l_artist_url` and `link_type`. |

`link` is referenced by the rule but is not defined in the supplied schema excerpt. The path metadata states `l_artist_url.link → link.id`; FK constraints for the path are not established by the supplied metadata.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `artist` pivots reachable through old `l_artist_url` rows whose `link` value joins to an old `link` tuple in \(V_1\), subject to the remainder of the rule path and selection condition.
- **Affected Pivot Tuples for Insertion (\(A^+\))**: `artist` pivots reachable through post-update `l_artist_url` and `link` tuples in \(V_2\), subject to the remainder of the rule path and selection condition.
- **Post-Update Contributions (\(S2\))**: Evaluate the stated DBpedia-shaped object mapping in \(V_2\), but only after the `link` joins, the `link_type` join, and the subject URI are resolved.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: Compare old and post-update contributions within the affected artist-pivot scope once those unresolved requirements are supplied. No join or URI construction is to be invented.

# Declarative Trigger Maintenance Plan for Relation: `link_type`

## 1. Relevant Rules Mapping (\(Relev(link\_type)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `otr-artist-dbpedia-01` | `relation-relevant` | One occurrence; `link_type` is a path relation used by the selection condition. |

`link_type` is referenced by the rule but is not defined in the supplied schema excerpt. The rule metadata records the selection `link_type.gid = '29651736-fa6d-48e4-aadc-a557c6add1cb'`. Its SQL contains `link_type ON link_type = link_type.id`, which is not independently resolvable as a validated join from the supplied metadata.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `artist` pivots reached through the rule’s stated path to old `link_type` tuples in \(V_1\), retaining only tuples satisfying the specified `gid` condition and the other rule selection condition.
- **Affected Pivot Tuples for Insertion (\(A^+\))**: `artist` pivots reached through the post-update rule path to post-update `link_type` tuples in \(V_2\), retaining only tuples satisfying the specified selection conditions.
- **Post-Update Contributions (\(S2\))**: The post-state result is conditional on resolving the `link_type` join and subject URI. The supplied object function can be applied only to qualifying `url` values after that resolution.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: Compare old and post-update contributions only once the join and subject URI are established. Do not infer an FK traversal from the ambiguous SQL join expression.

# Declarative Trigger Maintenance Plan for Relation: `url`

## 1. Relevant Rules Mapping (\(Relev(url)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `otr-artist-dbpedia-01` | `relation-relevant` | One occurrence; `url` is the path’s terminal relation and supplies the object value. |

`url` is referenced by the rule but is not defined in the supplied schema excerpt. The rule applies `url SIMILAR TO 'http://(de\|el\|en\|es\|ko\|pl\|pt).wikipedia.org/wiki/%'`.

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `artist` pivots reachable through the old `l_artist_url`, `link`, and `link_type` path to old `url` tuples in \(V_1\). Retain only tuples satisfying both stated selection conditions.
- **Affected Pivot Tuples for Insertion (\(A^+\))**: `artist` pivots reachable through the corresponding post-update path to post-update `url` tuples in \(V_2\), with both selection conditions re-evaluated.
- **Post-Update Contributions (\(S2\))**: Apply the specified nested `REPLACE` and `RDFIRI` conversion to qualifying post-state URL values. The subject URI and the `link_type` join remain unresolved.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: Compare old and post-update rule contributions within the affected scope only after all path joins and the subject URI are validated. The mapping remains OTR-shaped, not validated as an entity-preserving OTR.

# Declarative Trigger Maintenance Plan for Relation: `medium`

## 1. Relevant Rules Mapping (\(Relev(medium)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `ctr-medium-01` | `pivot-relevant` | No relational path; pivot only. |
| `dtr-medium-title-01` | `pivot-relevant` | No relational path; pivot only. |
| `dtr-medium-track-count-01` | `pivot-relevant` | No relational path; pivot only. |

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `medium` tuples in the update’s pre-state. For the title DTR, apply `nonNull(r.name)`; for the track-count DTR, apply `nonNull(r.track_count)`. Both columns are declared `NOT NULL` in the supplied schema.
- **Affected Pivot Tuples for Insertion (\(A^+\))**: New `medium` tuples in the post-state, with each DTR’s selection condition re-evaluated.
- **Post-Update Contributions (\(S2\))**: Evaluate the medium CTR and both local DTRs in \(V_2\), using `URI_medium(r,s) ≡ hasURI("http://musicbrainz.org/record/{id}#_", ⟨r.id⟩, s)`. Use the specified `dc:title` and `mo:track_count` predicates, literal conversions, datatypes, and rule-specific named graphs.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: Compute rule-specific old and post-update quads for the affected medium tuples, then set-difference them as \(\Delta^- = S1 \setminus S2\) and \(\Delta^+ = S2 \setminus S1\).

# Declarative Trigger Maintenance Plan for Relation: `track`

## 1. Relevant Rules Mapping (\(Relev(track)\))

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| `ctr-track-01` | `pivot-relevant` | No relational path; pivot only. |
| `dtr-track-number-01` | `pivot-relevant` | No relational path; pivot only. |

## 2. Maintenance Components to Be Computed

- **Affected Pivot Tuples for Deletion (\(A^-\))**: Old `track` tuples in the update’s pre-state. For the number DTR, retain tuples satisfying `track.position IS NOT NULL` (equivalently, `nonNull(r.position)`).
- **Affected Pivot Tuples for Insertion (\(A^+\))**: New `track` tuples in the post-state, re-evaluating the number DTR’s `position IS NOT NULL` condition.
- **Post-Update Contributions (\(S2\))**: Evaluate the track CTR and number DTR in \(V_2\), using `URI_track(r,s) ≡ hasURI("http://musicbrainz.org/track/{id}#_", ⟨r.id⟩, s)` and the supplied `mo:Track` and `mo:track_number` mappings. The DTR uses `RDFLiteral(r.position, "position", track, v, xsd:nonNegativeInteger)`.
- **Deletion and Insertion Changesets (\(\Delta^-\), \(\Delta^+\))**: Compute rule-specific old and post-update quads for the affected track tuples and derive \(\Delta^- = S1 \setminus S2\), \(\Delta^+ = S2 \setminus S1\). Include each rule’s supplied named graph.