# Declarative Trigger Maintenance Plan for Relation: `artist`

## 1. Relevant Rules Mapping ($Relev(artist)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{artist\_01}}$ | pivot-relevant | 0; local pivot rule |
| $\psi_{\text{artist\_02}}$ | pivot-relevant | 0; local DTR |
| $\psi_{\text{artist\_03}}$ | pivot-relevant | 0; local DTR |
| $\psi_{\text{artist\_04}}$ | pivot-relevant | 0; local DTR |
| $\psi_{\text{artist\_14}}^{\text{candidate}}$ | pivot-relevant | 1 endpoint occurrence in the intended path; candidate rule, not verified as a conforming OTR |
| $\psi_{\text{artist\_13}}$ | pivot-relevant | 1 endpoint occurrence in the artist-to-annotation path |
| $\psi_{\text{artist\_07}}$ | pivot-relevant | 1 endpoint occurrence in the artist-to-gender path |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Old `artist` pivot tuples from the statement’s deleted/updated rows. Re-evaluate every rule in $Relev(artist)$ against these pre-update pivot values and the corresponding pre-update relational state. |
| $A^+$ | New `artist` pivot tuples from the statement’s inserted/updated rows. Re-evaluate every rule in $Relev(artist)$ against these post-update pivot values and the post-update relational state. |
| $S2$ | Post-update rule contributions for affected artist pivots: evaluate the relevant CTR, local DTRs, path DTRs, and provisional candidate rule in state $V2$. Use this state to establish whether the resource and each output remain supported after the update. |
| $\Delta^+_{\text{pivot}}$ | New class contributions from $\psi_{\text{artist\_01}}$ for affected artists, accounting for the `artist` URI constructor and class mapping. |
| $\Delta^+_{\text{rel}}$ | New property contributions from the affected rules: local DTR outputs, path-DTR outputs, and the provisional `owl:sameAs` output where its path and conditions hold in $V2$. |
| $\Delta^+$ | Final insertion changeset: post-update RDF outputs for affected artists that are absent from the corresponding pre-update output set. |
| $\Delta^-$ | Final deletion changeset: pre-update RDF outputs for affected artists that are absent from the corresponding post-update output set. |

# Declarative Trigger Maintenance Plan for Relation: `medium`

## 1. Relevant Rules Mapping ($Relev(medium)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{medium\_01}}$ | pivot-relevant | 0; local pivot rule |
| $\psi_{\text{medium\_05}}$ | pivot-relevant | 0; local DTR |
| $\psi_{\text{medium\_02}}$ | pivot-relevant | 0; local DTR |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Old `medium` pivot tuples from deleted/updated rows. |
| $A^+$ | New `medium` pivot tuples from inserted/updated rows. |
| $S2$ | Post-update `mo:Record`, `dc:title`, and `mo:track_count` contributions for affected medium pivots, including the URI and non-null conditions. |
| $\Delta^+_{\text{pivot}}$ | New `mo:Record` class contributions from $\psi_{\text{medium\_01}}$. |
| $\Delta^+_{\text{rel}}$ | New `dc:title` and `mo:track_count` contributions from the local DTRs. |
| $\Delta^+$ | Post-update outputs for affected media absent from the pre-update outputs. |
| $\Delta^-$ | Pre-update outputs for affected media absent from the post-update outputs. |

# Declarative Trigger Maintenance Plan for Relation: `track`

## 1. Relevant Rules Mapping ($Relev(track)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{track\_01}}$ | pivot-relevant | 0; local pivot rule |
| $\psi_{\text{track\_02}}$ | pivot-relevant | 0; local DTR |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Old `track` pivot tuples from deleted/updated rows. |
| $A^+$ | New `track` pivot tuples from inserted/updated rows. |
| $S2$ | Post-update `mo:Track` and `mo:track_number` contributions for affected track pivots, applying the rule’s position condition and literal mapping. |
| $\Delta^+_{\text{pivot}}$ | New `mo:Track` class contributions from $\psi_{\text{track\_01}}$. |
| $\Delta^+_{\text{rel}}$ | New `mo:track_number` contributions from $\psi_{\text{track\_02}}$. |
| $\Delta^+$ | Post-update outputs for affected tracks absent from the pre-update outputs. |
| $\Delta^-$ | Pre-update outputs for affected tracks absent from the post-update outputs. |

# Declarative Trigger Maintenance Plan for Relation: `artist_annotation`

## 1. Relevant Rules Mapping ($Relev(artist\_annotation)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{artist\_13}}$ | relation-relevant | 1; association relation on the artist-to-annotation path |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Artist pivots connected to deleted/updated association rows through the pre-update artist-to-annotation path. |
| $A^+$ | Artist pivots connected to inserted/updated association rows through the post-update artist-to-annotation path. |
| $S2$ | Post-update `rdfs:comment` contributions for affected artists, using the post-update association rows, annotation tuples, and the `nonNull(annotation.text)` condition. |
| $\Delta^+_{\text{pivot}}$ | Empty: this relation does not change the artist pivot relation or its CTR support. |
| $\Delta^+_{\text{rel}}$ | New `rdfs:comment` outputs from $\psi_{\text{artist\_13}}$ for affected artists. |
| $\Delta^+$ | Post-update comment triples absent from the pre-update comment outputs for the affected artists. |
| $\Delta^-$ | Pre-update comment triples absent from the post-update comment outputs for the affected artists. |

**Validation constraint:** the schema excerpt defines `artist_annotation.artist` but does not define the referenced `annotation` relation or the annotation-side foreign key. The complete traversal cannot be schema-validated from the supplied schema.

# Declarative Trigger Maintenance Plan for Relation: `annotation`

## 1. Relevant Rules Mapping ($Relev(annotation)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{artist\_13}}$ | relation-relevant | 1; terminal relation on the artist-to-annotation path |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Artist pivots connected in the pre-update state to deleted/updated annotation tuples through `artist_annotation`. |
| $A^+$ | Artist pivots connected in the post-update state to inserted/updated annotation tuples through `artist_annotation`. |
| $S2$ | Post-update `rdfs:comment` contributions for affected artists, requiring a valid post-update path and non-null `annotation.text`. |
| $\Delta^+_{\text{pivot}}$ | Empty: annotation updates do not change artist pivot membership or artist class contributions. |
| $\Delta^+_{\text{rel}}$ | New `rdfs:comment` outputs from $\psi_{\text{artist\_13}}$. |
| $\Delta^+$ | Post-update comment triples absent from the pre-update comment outputs for the affected artists. |
| $\Delta^-$ | Pre-update comment triples absent from the post-update comment outputs for the affected artists. |

**Validation constraint:** `annotation` and its path foreign-key metadata are not present in the supplied schema excerpt, so the affected-artist path cannot be fully schema-validated.

# Declarative Trigger Maintenance Plan for Relation: `gender`

## 1. Relevant Rules Mapping ($Relev(gender)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{artist\_07}}$ | relation-relevant | 1; terminal relation on the artist-to-gender path |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Artist pivots connected in the pre-update state to deleted/updated gender tuples through `artist.gender → gender.id`. |
| $A^+$ | Artist pivots connected in the post-update state to inserted/updated gender tuples through `artist.gender → gender.id`. |
| $S2$ | Post-update `foaf:gender` contributions for affected artists, applying `nonNull(gender.name)` and the `LOWER` transformation. |
| $\Delta^+_{\text{pivot}}$ | Empty: gender updates do not change artist pivot membership or artist class contributions. |
| $\Delta^+_{\text{rel}}$ | New `foaf:gender` outputs from $\psi_{\text{artist\_07}}$. |
| $\Delta^+$ | Post-update gender triples absent from the pre-update gender outputs for the affected artists. |
| $\Delta^-$ | Pre-update gender triples absent from the post-update gender outputs for the affected artists. |

**Validation constraint:** the supplied schema excerpt does not define the `gender` relation or its attributes. The rule’s path and value attribute therefore cannot be validated against the supplied schema.

# Declarative Trigger Maintenance Plan for Relation: `l_artist_url`

## 1. Relevant Rules Mapping ($Relev(l\_artist\_url)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{artist\_14}}^{\text{candidate}}$ | relation-relevant | 1; association relation on the intended artist-to-URL path |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Artist pivots connected in the pre-update state to deleted/updated `l_artist_url` rows through the intended `entity0` traversal. |
| $A^+$ | Artist pivots connected in the post-update state to inserted/updated `l_artist_url` rows through the intended `entity0` traversal. |
| $S2$ | Post-update candidate `owl:sameAs` contributions for affected artists, evaluated using the complete intended path, mapping selection condition, URL replacement, and IRI conversion. |
| $\Delta^+_{\text{pivot}}$ | Empty: changes to `l_artist_url` do not change artist pivot membership or artist class contributions. |
| $\Delta^+_{\text{rel}}$ | New candidate `owl:sameAs` outputs supported by the post-update path and conditions. |
| $\Delta^+$ | Post-update candidate `owl:sameAs` triples absent from the pre-update candidate outputs for the affected artists. |
| $\Delta^-$ | Pre-update candidate `owl:sameAs` triples absent from the post-update candidate outputs for the affected artists. |

**Validation constraint:** `l_artist_url_fk_entity0` is supplied, but the complete intended path is not schema-validated. The endpoint joins and the candidate OTR’s target-pivot/target-CTR requirements remain unresolved; this plan does not treat the candidate rule as a verified conforming OTR.

# Declarative Trigger Maintenance Plan for Relation: `link`

## 1. Relevant Rules Mapping ($Relev(link)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{artist\_14}}^{\text{candidate}}$ | relation-relevant | 1; intermediate relation on the intended candidate-rule path |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Artist pivots connected in the pre-update state to deleted/updated `link` tuples through the intended candidate-rule path. |
| $A^+$ | Artist pivots connected in the post-update state to inserted/updated `link` tuples through the intended candidate-rule path. |
| $S2$ | Post-update candidate `owl:sameAs` contributions for affected artists, evaluating the path and all candidate-rule selection and conversion conditions in $V2$. |
| $\Delta^+_{\text{pivot}}$ | Empty: `link` updates do not change artist pivot membership or artist class contributions. |
| $\Delta^+_{\text{rel}}$ | New candidate `owl:sameAs` outputs supported by the post-update path. |
| $\Delta^+$ | Post-update candidate `owl:sameAs` triples absent from the pre-update candidate outputs for the affected artists. |
| $\Delta^-$ | Pre-update candidate `owl:sameAs` triples absent from the post-update candidate outputs for the affected artists. |

**Validation constraint:** the supplied schema excerpt does not define `link`; the intended joins involving it, including the reported ambiguous `link_type` join, must be clarified before this rule can be validated or safely maintained.

# Declarative Trigger Maintenance Plan for Relation: `link_type`

## 1. Relevant Rules Mapping ($Relev(link\_type)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{artist\_14}}^{\text{candidate}}$ | relation-relevant | 1; intermediate relation on the intended candidate-rule path |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Artist pivots connected in the pre-update state to deleted/updated `link_type` tuples through the intended candidate-rule path. |
| $A^+$ | Artist pivots connected in the post-update state to inserted/updated `link_type` tuples through the intended candidate-rule path. |
| $S2$ | Post-update candidate `owl:sameAs` contributions for affected artists, applying the link-type selection condition and the complete intended path in $V2$. |
| $\Delta^+_{\text{pivot}}$ | Empty: `link_type` updates do not change artist pivot membership or artist class contributions. |
| $\Delta^+_{\text{rel}}$ | New candidate `owl:sameAs` outputs supported by the post-update path and selection condition. |
| $\Delta^+$ | Post-update candidate `owl:sameAs` triples absent from the pre-update candidate outputs for the affected artists. |
| $\Delta^-$ | Pre-update candidate `owl:sameAs` triples absent from the post-update candidate outputs for the affected artists. |

**Validation constraint:** `link_type` is not defined in the supplied schema excerpt, and its join condition in the candidate rule is reported as ambiguous or erroneous. No executable path can be assumed until it is clarified.

# Declarative Trigger Maintenance Plan for Relation: `url`

## 1. Relevant Rules Mapping ($Relev(url)$)

| Rule ID | Relevance Classification | Relational Path Occurrences |
|---|---|---|
| $\psi_{\text{artist\_14}}^{\text{candidate}}$ | relation-relevant | 1; terminal relation on the intended artist-to-URL path |

## 2. Maintenance Components to Be Computed

| Component | Declarative specification |
|---|---|
| $A^-$ | Artist pivots connected in the pre-update state to deleted/updated `url` tuples through the intended candidate-rule path. |
| $A^+$ | Artist pivots connected in the post-update state to inserted/updated `url` tuples through the intended candidate-rule path. |
| $S2$ | Post-update candidate `owl:sameAs` contributions for affected artists, applying `nonNull(url.url)`, the URL-selection condition, replacement transformations, and IRI conversion. |
| $\Delta^+_{\text{pivot}}$ | Empty: `url` updates do not change artist pivot membership or artist class contributions. |
| $\Delta^+_{\text{rel}}$ | New candidate `owl:sameAs` outputs supported by the post-update path and candidate conditions. |
| $\Delta^+$ | Post-update candidate `owl:sameAs` triples absent from the pre-update candidate outputs for the affected artists. |
| $\Delta^-$ | Pre-update candidate `owl:sameAs` triples absent from the post-update candidate outputs for the affected artists. |

**Validation constraint:** `url` and its attributes are not defined in the supplied schema excerpt. The source URL’s type and the validity of every transformed value as an IRI are also unestablished.

# Consolidated Declarative Execution Plan

| Relation | Relevant rules | Pivot-relevant rules | Relation-relevant rules | Multiple occurrences in a relational path? | Compute $A^-$ | Compute $A^+$ | Compute $S2$ | Compute $\Delta^+_{\text{pivot}}$ | Compute $\Delta^+_{\text{rel}}$ | Compute final $\Delta^+$ and $\Delta^-$ |
|---|---|---|---|---|---|---|---|---|---|---|
| `artist` | $\psi_{\text{artist\_01}}$, $\psi_{\text{artist\_02}}$, $\psi_{\text{artist\_03}}$, $\psi_{\text{artist\_04}}$, $\psi_{\text{artist\_14}}^{\text{candidate}}$, $\psi_{\text{artist\_13}}$, $\psi_{\text{artist\_07}}$ | All listed rules | None | No; each path endpoint occurrence is single | Old deleted/updated artist pivots | New inserted/updated artist pivots | Re-evaluate all relevant rule outputs in $V2$ for affected artists and validate support | Evaluate the artist CTR contribution | Evaluate local/path DTRs and the provisional candidate property contribution | Difference affected rule outputs between $V1$ and $V2$ |
| `medium` | $\psi_{\text{medium\_01}}$, $\psi_{\text{medium\_05}}$, $\psi_{\text{medium\_02}}$ | All listed rules | None | No relational paths | Old deleted/updated medium pivots | New inserted/updated medium pivots | Re-evaluate class and local DTR contributions in $V2$ | Evaluate the medium CTR contribution | Evaluate title and track-count contributions | Difference affected rule outputs between $V1$ and $V2$ |
| `track` | $\psi_{\text{track\_01}}$, $\psi_{\text{track\_02}}$ | Both listed rules | None | No relational paths | Old deleted/updated track pivots | New inserted/updated track pivots | Re-evaluate class and local DTR contributions in $V2$ | Evaluate the track CTR contribution | Evaluate the track-number contribution | Difference affected rule outputs between $V1$ and $V2$ |
| `artist_annotation` | $\psi_{\text{artist\_13}}$ | None | $\psi_{\text{artist\_13}}$ | No; one occurrence | Artists connected to old association rows in $V1$ | Artists connected to new association rows in $V2$ | Re-evaluate comments over the post-update path | Empty | Evaluate affected comment outputs | Difference affected comment outputs between $V1$ and $V2$ |
| `annotation` | $\psi_{\text{artist\_13}}$ | None | $\psi_{\text{artist\_13}}$ | No; one occurrence | Artists connected to old annotation tuples in $V1$ | Artists connected to new annotation tuples in $V2$ | Re-evaluate comments over the post-update path | Empty | Evaluate affected comment outputs | Difference affected comment outputs between $V1$ and $V2$ |
| `gender` | $\psi_{\text{artist\_07}}$ | None | $\psi_{\text{artist\_07}}$ | No; one occurrence | Artists connected to old gender tuples in $V1$ | Artists connected to new gender tuples in $V2$ | Re-evaluate transformed gender outputs in $V2$ | Empty | Evaluate affected gender outputs | Difference affected gender outputs between $V1$ and $V2$ |
| `l_artist_url` | $\psi_{\text{artist\_14}}^{\text{candidate}}$ | None | $\psi_{\text{artist\_14}}^{\text{candidate}}$ | No; one occurrence | Artists connected to old association rows in $V1$ | Artists connected to new association rows in $V2$ | Re-evaluate candidate outputs in $V2$; full path remains unvalidated | Empty | Evaluate candidate property outputs, if the rule is validated | Difference affected candidate outputs between $V1$ and $V2$ |
| `link` | $\psi_{\text{artist\_14}}^{\text{candidate}}$ | None | $\psi_{\text{artist\_14}}^{\text{candidate}}$ | No; one occurrence | Artists connected through old path rows in $V1$ | Artists connected through new path rows in $V2$ | Re-evaluate candidate outputs in $V2$; joins remain unresolved | Empty | Evaluate candidate property outputs, if the rule is validated | Difference affected candidate outputs between $V1$ and $V2$ |
| `link_type` | $\psi_{\text{artist\_14}}^{\text{candidate}}$ | None | $\psi_{\text{artist\_14}}^{\text{candidate}}$ | No; one occurrence | Artists connected through old path rows in $V1$ | Artists connected through new path rows in $V2$ | Re-evaluate candidate outputs in $V2$; selection join remains unresolved | Empty | Evaluate candidate property outputs, if the rule is validated | Difference affected candidate outputs between $V1$ and $V2$ |
| `url` | $\psi_{\text{artist\_14}}^{\text{candidate}}$ | None | $\psi_{\text{artist\_14}}^{\text{candidate}}$ | No; one occurrence | Artists connected to old URL tuples in $V1$ | Artists connected to new URL tuples in $V2$ | Re-evaluate candidate outputs in $V2$, including URL filters and transformations | Empty | Evaluate candidate property outputs, if the rule is validated | Difference affected candidate outputs between $V1$ and $V2$ |

For every row, the final changesets are set differences of the affected rule outputs: $\Delta^+ = Q(V2) \setminus Q(V1)$ and $\Delta^- = Q(V1) \setminus Q(V2)$. No named graph or quad context is specified in the supplied rules; graph selection must therefore be supplied separately rather than inferred. The conditional uniqueness guarantees for the URI templates must also be established before treating pivot resources as identity-preserving.