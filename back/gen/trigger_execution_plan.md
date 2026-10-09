# Declarative Trigger Maintenance Plan

## Definitions and scope

Let \(V_1\) and \(V_2\) denote the database states immediately before and after an update. For rule \(\psi\), let \(Q_\psi(V)\) be the RDF quads produced by that rule in state \(V\), including its selection condition, URI construction, predicate, object construction, and named graph.

For each applicable rule:

- **Pivot update:** \(A^-_\psi\) is the set of old pivot tuples whose rule output may change; \(A^+_\psi\) is the corresponding set of new pivot tuples.
- **Path-relation update:** \(A^-_\psi\) is the set of pivots connected to changed path tuples in \(V_1\); \(A^+_\psi\) is the set of pivots connected to changed path tuples in \(V_2\). Include both old and new path connections when a changed row moves between pivots.
- **Post-update contribution:** \(S2_\psi = Q_\psi(V_2)\) restricted to \(A^+_\psi\), evaluated using the complete post-update path and the rule’s selection condition.
- **Rule-level changesets:** \(\Delta^-_\psi = Q_\psi(V_1)|_{A^-_\psi} \setminus Q_\psi(V_2)|_{A^+_\psi}\); \(\Delta^+_\psi = Q_\psi(V_2)|_{A^+_\psi} \setminus Q_\psi(V_1)|_{A^-_\psi}\). Compare complete RDF quads, including graph, subject, predicate, and object.
- **Pivot/path components:** `compute_delta_pivot` applies the changeset calculation to pivot-relevant rules; `compute_delta_rel` applies it to relation-relevant rules. `compute_delta` is the set union of those applicable components. For a rule classified as both kinds of affected update dependency, its rule output is computed once and its resulting quad changes are not duplicated.

“Multiple path occurrences” counts occurrences of a relation within the rule’s relational path; a pivot relation named as the path’s starting point is not an additional occurrence. No supplied rule contains multiple occurrences of the updated relation in its path.

The plans below cover every relation explicitly declared in the supplied DDL, plus `annotation`, `gender`, `link`, `link_type`, and `url`, which occur in the supplied rules but have no corresponding `CREATE TABLE` definition in the supplied schema excerpt. Relations not listed in any rule have empty \(Relev(R)\) and require no mapping-specific maintenance.

## Relation plans

| Relation \(R\) | `relevant_rules` | `pivot_relevant_rules` | `relation_relevant_rules` | `multiple_path_occurrences` | `compute_a_minus` | `compute_a_plus` | `compute_s2` | `compute_delta_pivot` | `compute_delta_rel` | `compute_delta` |
|---|---|---|---|---|---|---|---|---|---|---|
| `alternative_medium` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `alternative_track` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `alternative_medium_track` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist` | `ctr-artist-01`; `dtr-artist-guid-01`; `dtr-artist-name-01`; `dtr-artist-sort-label-01`; `otr-artist-dbpedia-01`; `dtr-artist-annotation-01`; `dtr-artist-gender-01` | `ctr-artist-01`; `dtr-artist-guid-01`; `dtr-artist-name-01`; `dtr-artist-sort-label-01`; `otr-artist-dbpedia-01`; `dtr-artist-annotation-01`; `dtr-artist-gender-01` | \(\varnothing\) (the rules’ `artist` references are their pivot, not a separate path relation occurrence) | No; `artist` occurs once as the pivot/path root | Old `artist` tuples in the update’s old transition rows. For each affected old pivot, identify old outputs of the applicable rules; local DTR outputs apply their `nonNull` condition. | New `artist` tuples in the update’s new transition rows. Include outputs only where the rule’s selection condition holds. | Re-evaluate the applicable rule outputs for new pivots in \(V_2\). The DBpedia, annotation, and gender rules have unresolved subject URI metadata; their post-update outputs are not fully synthesizable until that is resolved. | Compute old-versus-post-update quad differences for the pivot-relevant rules. | None as a separate relation-relevant component. | Union the applicable pivot-rule quad changes; do not emit unresolved URI-dependent outputs until the URI definition is supplied. |
| `artist_alias_type` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_alias` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_annotation` | `dtr-artist-annotation-01` | \(\varnothing\) | `dtr-artist-annotation-01` | No; once | Old pivots connected to changed old `artist_annotation` rows in \(V_1\), following the inverse `artist_annotation_fk_artist` traversal. | Pivots connected to changed new `artist_annotation` rows in \(V_2\), following the same traversal. | Re-evaluate `nonNull(a.text)` and the annotation path for the post-update pivots. Subject URI is unresolved because the `lb:sm_artist` definition was not supplied. | None | Compute the rule’s quad changes from old and new path contributions. The annotation-to-`annotation.id` join is present, but its FK constraint name is not supplied. | Relation-rule changes only, subject to resolving the subject URI. |
| `artist_attribute_type` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_attribute_type_allowed_value` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_attribute` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_ipi` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_isni` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_meta` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_tag` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_rating_raw` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_tag_raw` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_credit` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_credit_gid_redirect` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_credit_name` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_gid_redirect` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_type` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_release` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_release_nonva` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_release_va` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_release_pending_update` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_release_group` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_release_group_nonva` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_release_group_va` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `artist_release_group_pending_update` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `edit_artist` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `editor_subscribe_artist` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `editor_subscribe_artist_deleted` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `editor_collection_artist` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_area_artist` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_artist` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_event` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_genre` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_instrument` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_label` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_mood` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_place` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_recording` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_release` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_release_group` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_series` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `l_artist_url` | `otr-artist-dbpedia-01` | \(\varnothing\) | `otr-artist-dbpedia-01` | No; once | For changed old link rows, identify old `artist` pivots through `artist.id → l_artist_url.entity0` in \(V_1\), using only the supplied matching FK `l_artist_url_fk_entity0`. | Identify pivots connected to changed new link rows through the same supplied traversal in \(V_2\). | Re-evaluate the complete rule path and selection condition in \(V_2\). The mapping’s subject URI is unresolved; its other path joins are not all independently validated. | None | Compute old-versus-post-update rule quads for affected artist pivots. Do not assume unnamed FK constraints or repair the supplied join expressions. | Relation-rule changes only; the rule is OTR-shaped but not validated as an entity-preserving OTR from the supplied metadata. |
| `l_artist_work` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `medium` | `ctr-medium-01`; `dtr-medium-title-01`; `dtr-medium-track-count-01` | `ctr-medium-01`; `dtr-medium-title-01`; `dtr-medium-track-count-01` | \(\varnothing\) | No | Old `medium` tuples in the update’s old transition rows. For DTR outputs, apply `nonNull(r.name)` and `nonNull(r.track_count)` respectively. | New `medium` tuples in the update’s new transition rows, subject to the corresponding non-null conditions. | Re-evaluate the class and local DTR outputs for new pivots in \(V_2\). | Compute old-versus-post-update quad differences for the pivot rules. | None | Union the applicable pivot-rule quad changes. |
| `medium_attribute_type` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `medium_attribute_type_allowed_format` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `medium_attribute_type_allowed_value` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `medium_attribute_type_allowed_value_allowed_format` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `medium_attribute` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `medium_cdtoc` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `medium_format` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `track` | `ctr-track-01`; `dtr-track-number-01` | `ctr-track-01`; `dtr-track-number-01` | \(\varnothing\) | No | Old `track` tuples in the update’s old transition rows. For the number DTR, retain only tuples satisfying `track.position IS NOT NULL`. | New `track` tuples in the update’s new transition rows, retaining only tuples satisfying `track.position IS NOT NULL`. | Re-evaluate the class and track-number DTR outputs for new pivots in \(V_2\), preserving the supplied `xsd:nonNegativeInteger` literal mapping. | Compute old-versus-post-update quad differences for the pivot rules. | None | Union the applicable pivot-rule quad changes. |
| `track_gid_redirect` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `track_raw` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `medium_index` | \(\varnothing\) | \(\varnothing\) | \(\varnothing\) | No | N/A | N/A | N/A | N/A | N/A | None |
| `annotation` *(referenced by rule; no table definition supplied)* | `dtr-artist-annotation-01` | \(\varnothing\) | `dtr-artist-annotation-01` | No; once | For changed old annotation rows, identify old artist pivots through `artist_annotation.annotation → annotation.id` in \(V_1\). | Identify pivots connected to changed new annotation rows through that join in \(V_2\). | Re-evaluate `nonNull(a.text)` and the rule output in \(V_2\); the subject URI remains unresolved. | None | Compute old-versus-post-update path-rule quad differences. The join is stated in the rule, but its FK constraint name is absent. | Relation-rule changes only, subject to resolving the subject URI. |
| `gender` *(referenced by rule; no table definition supplied)* | `dtr-artist-gender-01` | \(\varnothing\) | `dtr-artist-gender-01` | No; once | For changed old gender rows, identify old artist pivots through `artist.gender → gender.id` using the supplied `artist_fk_gender` traversal in \(V_1\). | Identify pivots connected to changed new gender rows through that traversal in \(V_2\). | Re-evaluate `nonNull(LOWER(g.name))` and the `LOWER(g.name)` literal mapping in \(V_2\); the subject URI remains unresolved. | None | Compute old-versus-post-update path-rule quad differences. | Relation-rule changes only, subject to resolving the subject URI. |
| `link` *(referenced by rule; no table definition supplied)* | `otr-artist-dbpedia-01` | \(\varnothing\) | `otr-artist-dbpedia-01` | No; once in the stated relational path | Identify old artist pivots connected to changed old `link` rows through the stated `l_artist_url.link → link.id` traversal in \(V_1\). Its FK constraint is not established by the supplied metadata. | Identify pivots connected to changed new `link` rows through the stated traversal in \(V_2\), without assuming an unstated FK. | Re-evaluate the supplied rule path and selection condition in \(V_2\); the subject URI and independent validation of the path remain unresolved. | None | Compute path-rule quad differences only to the extent that the specified joins can be resolved from the available metadata. | Relation-rule changes only; do not infer missing constraints or alter the supplied join expression. |
| `link_type` *(referenced by rule; no table definition supplied)* | `otr-artist-dbpedia-01` | \(\varnothing\) | `otr-artist-dbpedia-01` | No; once in the stated relational path | Identify old artist pivots connected to changed old `link_type` rows through the stated path in \(V_1\). The supplied SQL join expression does not establish an independently validated FK traversal. | Identify pivots connected to changed new `link_type` rows through the stated path in \(V_2\), subject to resolving that join. | Re-evaluate the stated `link_type.gid` selection condition and rule path in \(V_2\) only after the join is resolved. The subject URI remains unresolved. | None | Compute path-rule quad differences only when the supplied path can be interpreted unambiguously. | Relation-rule changes only; no join or FK may be hallucinated. |
| `url` *(referenced by rule; no table definition supplied)* | `otr-artist-dbpedia-01` | \(\varnothing\) | `otr-artist-dbpedia-01` | No; once in the stated relational path | Identify old artist pivots connected to changed old URL rows through `l_artist_url.entity1 → url.id` in \(V_1\). The FK constraint is not established by the supplied metadata. | Identify pivots connected to changed new URL rows through the stated path in \(V_2\), without assuming an unstated FK. | Re-evaluate the supplied URL `SIMILAR TO` condition and `RDFIRI(REPLACE(REPLACE(...)))` object construction in \(V_2\). The subject URI remains unresolved. | None | Compute old-versus-post-update path-rule quad differences only where the specified joins are resolved. | Relation-rule changes only; the OTR-shaped mapping is not validated as an entity-preserving OTR from the supplied information. |

## Rule occurrence and synthesis constraints

- All relevant-rule occurrences are single occurrences in their stated relational paths; no self-join or repeated occurrence of an updated relation is specified.
- Updates to `artist` affect all seven artist-pivot rules. Updates to `artist_annotation`, `annotation`, `gender`, `l_artist_url`, `link`, `link_type`, or `url` affect only the corresponding path rule shown above.
- Updates to `medium` affect its CTR and two local DTRs; updates to `track` affect its CTR and number DTR. The track DTR’s `position IS NOT NULL` condition must be retained.
- The URI constructor for the artist annotation, gender, and DBpedia rules cannot be synthesized from the supplied inputs because the definition of `lb:sm_artist` is missing.
- The DBpedia mapping’s path and joins are not fully validated: only `l_artist_url_fk_entity0` is supplied as a matching FK name, the other FK constraints are not established, and the stated `link_type` SQL join expression does not independently establish the described traversal. The mapping is therefore retained as an OTR-shaped rule for relevance planning, not treated as a validated entity-preserving OTR.
- No RDF changeset is required for a relation whose \(Relev(R)\) is empty.