# Entity-preservation report

## Overall assessment

The mappings contain several **plausible entity-preserving patterns**, but the extracted metadata is not sufficient to certify the full set as conforming to the formal specification. In particular:

1. The `artist` and `medium` subject templates can serve as URI constructors for their respective pivot relations, **provided their template columns are non-null and unique**. Those schema constraints are not supplied.
2. The subject map referenced by `lb:artist_dbpedia`, `lb:artist_annotation`, and `lb:artist_gender` is missing (`lb:sm_artist`). Consequently, these mappings cannot currently be grounded in a known CTR and artist pivot identity.
3. The `owl:sameAs` mapping has a transformed IRI object and a multi-relation join path, but its subject identity, complete FK path, and exact join conditions cannot be validated from the supplied metadata.
4. The annotation and gender properties are structurally candidates for **Path-DTRs** from the artist pivot. The required paths must be validated against the schema, and the annotation path includes an association table.
5. The track-number mapping can be a Local-DTR for the `track` pivot if it is explicitly tied to the same URI constructor and identity as `lb:Track_psi_track_01`.

Accordingly, the specification is **conditionally satisfiable for the direct artist, medium, and track mappings, but not fully verified as supplied**. The missing subject-map definition and incomplete schema/FK evidence prevent a complete formal certification.

---

## Pivot relations and identity checks

| Mapping group | Candidate pivot relation | Subject URI constructor | Entity-preservation assessment |
|---|---|---|---|
| `lb:Artist` | `artist` | `http://musicbrainz.org/artist/{gid}#_` | Plausible CTR. Distinctness requires `artist.gid` to be non-null and unique. |
| `lb:artist_dbpedia` | Presumably `artist`, with related URL/link rows | Subject map absent | Cannot verify a CTR or establish the subject identity from the supplied metadata. |
| `lb:artist_annotation` | Presumably `artist` | Subject map absent | Candidate Path-DTR, but it cannot be formally attached to an artist CTR until the subject map is supplied. |
| `lb:artist_gender` | Presumably `artist` | Subject map absent | Candidate Path-DTR, but it cannot be formally attached to an artist CTR until the subject map is supplied. |
| `lb:Medium` | `medium` | `http://musicbrainz.org/record/{id}#_` | Plausible CTR. Distinctness requires `medium.id` to be non-null and unique. |
| `lb:Track_psi_track_01` | `track` | `http://musicbrainz.org/track/{id}#_` | Plausible CTR. Distinctness requires `track.id` to be non-null and unique. |
| `lb:Track_psi_track_02` | `track` | `http://musicbrainz.org/track/{id}#_` | Candidate Local-DTR for the same track identity as `lb:Track_psi_track_01`; the shared identity should be made explicit. |

A URI template is a valid URI constructor only when every placeholder is bound to the stated pivot tuple, the generated value is a valid IRI, and the constructor distinguishes distinct tuples of that pivot relation. The templates shown have one placeholder each; the necessary non-null and uniqueness constraints are **not present in the extracted schema evidence**. They therefore cannot be asserted as proven.

---

## Mapping-by-mapping analysis

### 1. `lb:Artist`

The logical table selects `gid`, `name`, and `sort_name` from `artist`. The three rows share the same subject template and class, so they should be treated as one class mapping with two local datatype-property mappings and the `mo:musicbrainz_guid` property.

**Candidate CTR**, conditional on `artist.gid` being non-null and unique:

```text
ctr-artist:
  mo:MusicArtist(s) ← artist(a), URI_artist(a,s)
```

where:

```text
URI_artist(a,s) ≡
  hasURI("http://musicbrainz.org/artist/{gid}#_", ⟨a.gid⟩, s)
```

**Candidate Local-DTRs:**

```text
dtr-artist-guid:
  mo:musicbrainz_guid(s,v) ←
    artist(a), URI_artist(a,s),
    nonNull(a.gid),
    RDFLiteral(a.gid,"gid",artist,v)
```

```text
dtr-artist-name:
  foaf:name(s,v) ←
    artist(a), URI_artist(a,s),
    nonNull(a.name),
    RDFLiteral(a.name,"name",artist,v)
```

```text
dtr-artist-sort-label:
  ov:sortLabel(s,v) ←
    artist(a), URI_artist(a,s),
    nonNull(a.sort_name),
    RDFLiteral(a.sort_name,"sort_name",artist,v)
```

These are entity-preserving in structure: their values come from attributes of the same artist pivot tuple, and they do not construct new resources. The datatype rules should emit values only when the relevant source attribute is non-null.

**Verification required:** confirm that `artist.gid` is a non-null unique key (or otherwise prove that the URI constructor is injective over the selected artist tuples).

---

### 2. `lb:artist_dbpedia`

The mapping’s logical table traverses `artist`, `l_artist_url`, `link`, `link_type`, and `url`, applies a Wikipedia-to-DBpedia URL transformation, and uses `owl:sameAs`. It is a candidate object-property mapping, not a datatype-property mapping.

However, its subject map refers to `lb:sm_artist`, whose definition is absent. Without that definition, the subject’s URI constructor, class, and relation to the `artist` pivot are unknown. The mapping therefore cannot be completed as an OTR using the supplied metadata.

The supplied path is reported as:

```text
l_artist_url.entity0 / l_artist_url.link / link_type / l_artist_url.entity1
artist.id           / link.id              / link_type.id / url.id
```

Only `l_artist_url_fk_entity0` is identified as a matching declared FK. The remaining edges of the path are not established as schema-validated FKs by the supplied evidence. In addition, the SQL condition is shown as:

```sql
INNER JOIN link_type ON link_type = link_type.id
```

As written, this does not clearly express a join from `link` to `link_type`; it appears to be missing or misidentifying the linking column. The intended join must be checked against the actual schema and corrected before the path can be accepted.

The object transformation is:

```text
REPLACE(
  REPLACE(url, 'wikipedia.org/wiki', 'dbpedia.org/resource'),
  'http://en.',
  'http://'
)
```

The selection condition restricts input values to specified Wikipedia URL patterns. This is a **deterministic object-IRI transformation**, not the URI constructor for the artist subject. Its output must be checked to ensure it is a valid IRI for every selected input. It must not be mistaken for proof of a subject CTR or a schema relationship.

**Assessment:** not formally verifiable as an OTR as supplied. It could be represented as an object-property rule only after the subject CTR is supplied, the complete relational path is validated, and the transformed object is shown to be a valid IRI. Under the given formal OTR pattern, the target resource’s class/pivot CTR must also be identified if this is to be certified as a relationship between pivot entities. An external DBpedia IRI alone does not provide that target CTR in the extracted metadata.

---

### 3. `lb:artist_annotation`

The logical table joins `annotation`, `artist_annotation`, and `artist`, and selects `gid` and `text`. The subject map again refers to the missing `lb:sm_artist`.

The intended semantic pattern is a **Path-DTR**: an artist pivot tuple is associated through the `artist_annotation` bridge to an annotation tuple, and the annotation’s `text` supplies `rdfs:comment`.

The reported child/parent columns are:

```text
artist_annotation.annotation / artist_annotation.artist
annotation.id                / artist.id
```

The supplied FK name is `artist_annotation_fk_artist`; this supports the artist-to-association-table connection only if the actual schema definition confirms the corresponding columns. The annotation-side FK is not identified as a declared constraint in the provided metadata. Thus, the full path cannot be schema-validated from this input.

The intended ordered path from the artist pivot to annotation is:

```text
artist
  ← artist_annotation (artist_annotation.artist = artist.id)
  → annotation        (artist_annotation.annotation = annotation.id)
```

This path can support a Path-DTR if both joins are valid and the annotation-side relation is confirmed. Multiple annotations per artist are compatible with a datatype property producing multiple comments; they do not create new artist entities.

**Candidate rule, conditional on the subject CTR and both path edges being verified:**

```text
dtr-artist-comment:
  rdfs:comment(s,v) ←
    artist(a), URI_artist(a,s),
    annotation(n), nonNull(n.text),
    RDFLiteral(n.text,"text",annotation,v),
    [artist_annotation_path](a,n)
```

**Assessment:** a plausible entity-preserving Path-DTR, but not verifiable as supplied because the subject map is missing and the complete FK path is not established.

---

### 4. `lb:artist_gender`

The logical table joins `artist` to `gender` on `artist.gender = gender.id`. The supplied FK name, `artist_fk_gender`, indicates a matching schema constraint. If that constraint confirms this join, the path from an artist to its referenced gender row is functional from the artist side, as required for the foreign-key navigation used here.

The subject map is nevertheless missing, so the rule cannot currently be attached to a verified artist CTR.

The value transformation is `LOWER(gender.name)`. It is listed both as the transformation function and in the logical-table projection (`LOWER(gender.name) AS gender`). The mapping must clarify whether the value being mapped is already transformed in the logical table or whether the DTR applies `LOWER` to the raw `gender.name`. Applying it twice is redundant, although for this particular function it is normally idempotent.

**Candidate Path-DTR using the raw source attribute:**

```text
dtr-artist-gender:
  foaf:gender(s,v) ←
    artist(a), URI_artist(a,s),
    gender(g), nonNull(g.name),
    RDFLiteral(g.name,"name",gender,u),
    LOWER(u,v),
    [artist_fk_gender](a,g)
```

Equivalently, if the logical-table alias `gender` is already the result of `LOWER(gender.name)`, use that projected value as the DTR input and do not apply the transformation again.

**Assessment:** structurally a valid candidate Path-DTR if the FK and join are confirmed and the missing artist subject map is supplied.

---

### 5. `lb:Medium`

The logical table selects attributes directly from `medium`, so `medium` is the candidate pivot. The subject template maps `medium.id` to the record IRI.

**Candidate CTR**, conditional on `medium.id` being non-null and unique:

```text
ctr-medium:
  mo:Record(s) ← medium(m), URI_medium(m,s)
```

where:

```text
URI_medium(m,s) ≡
  hasURI("http://musicbrainz.org/record/{id}#_", ⟨m.id⟩, s)
```

**Candidate Local-DTRs:**

```text
dtr-medium-title:
  dc:title(s,v) ←
    medium(m), URI_medium(m,s),
    nonNull(m.name),
    RDFLiteral(m.name,"name",medium,v)
```

```text
dtr-medium-track-count:
  mo:track_count(s,v) ←
    medium(m), URI_medium(m,s),
    nonNull(m.track_count),
    RDFLiteral(m.track_count,"track_count",medium,v)
```

These property mappings preserve the `medium` entity: the values come from attributes of the pivot tuple. The declared datatype `xsd:int` should also be consistent with the SQL type and the RDF lexical value.

**Verification required:** establish that `medium.id` is a non-null unique key and that the generated URI is valid. The appropriateness of mapping this pivot to `mo:Record` is a vocabulary/semantic modeling question; it does not, by itself, establish or invalidate tuple identity preservation.

---

### 6. `lb:Track_psi_track_01` and `lb:Track_psi_track_02`

`lb:Track_psi_track_01` selects `track.id`, uses the track URI template, and declares class `mo:Track`. It is a candidate CTR:

```text
ctr-track:
  mo:Track(s) ← track(t), URI_track(t,s)
```

where:

```text
URI_track(t,s) ≡
  hasURI("http://musicbrainz.org/track/{id}#_", ⟨t.id⟩, s)
```

Distinct track tuples generate distinct resources only if `track.id` is non-null and unique.

`lb:Track_psi_track_02` uses the same logical pivot and URI template, selects `position`, and applies the selection condition `track.position IS NOT NULL`. It can be represented as a Local-DTR attached to the same track CTR:

```text
dtr-track-number:
  mo:track_number(s,v) ←
    track(t), URI_track(t,s),
    t.position IS NOT NULL,
    nonNull(t.position),
    RDFLiteral(t.position,"position",track,v)
```

The selection condition and `nonNull` condition are effectively redundant for this column, but explicitly stating the non-null requirement is consistent with the DTR pattern.

The class is absent from the second mapping row. That does not prevent it from being a DTR if its subject map is exactly the same as the track CTR’s subject map. The mapping should explicitly document that relationship; otherwise, the metadata alone does not establish that both mappings use the same resource identity.

**Assessment:** the first mapping is a candidate CTR; the second is a candidate Local-DTR for it. Both depend on `track.id` being a non-null unique key and on the shared subject constructor being confirmed.

---

## Relational path and property classification summary

| Property | Intended TR pattern | Path/attribute source | Status |
|---|---|---|---|
| `mo:musicbrainz_guid` | Local-DTR | `artist.gid` | Candidate; artist subject identity needs key validation. |
| `foaf:name` | Local-DTR | `artist.name` | Candidate; artist subject identity needs key validation. |
| `ov:sortLabel` | Local-DTR | `artist.sort_name` | Candidate; artist subject identity needs key validation. |
| `owl:sameAs` | OTR-like mapping | Artist → `l_artist_url` → `link` → `link_type` / `url` | Not verified: missing subject CTR, incomplete FK evidence, and questionable `link_type` join. |
| `rdfs:comment` | Path-DTR | Artist → `artist_annotation` → `annotation.text` | Candidate; missing subject CTR and incomplete FK validation. |
| `foaf:gender` | Path-DTR | Artist → `gender.name`, transformed with `LOWER` | Candidate; missing subject CTR; confirm FK and avoid ambiguous/double transformation. |
| `dc:title` | Local-DTR | `medium.name` | Candidate; medium identity needs key validation. |
| `mo:track_count` | Local-DTR | `medium.track_count` | Candidate; medium identity needs key validation. |
| `mo:track_number` | Local-DTR | `track.position`, selected when non-null | Candidate; link it explicitly to the track CTR. |

---

## Constructs that prevent full verification

- **Missing subject-map definition:** `lb:sm_artist` is referenced by three mappings but not defined in the input. Its pivot relation, URI template, and any class mapping are therefore unknown.
- **Unproven URI uniqueness:** no primary-key, unique, or non-null declarations are supplied for `artist.gid`, `medium.id`, or `track.id`. The URI templates are plausible, but distinct-tuple-to-distinct-resource preservation cannot be proven without these constraints.
- **Incomplete FK evidence:** the annotation and DBpedia mappings traverse joins for which not every FK is identified as schema-declared.
- **Potentially incorrect DBpedia join:** `link_type = link_type.id` does not clearly connect `link` to `link_type`. The SQL and intended path must be checked.
- **Unspecified object target mapping:** the DBpedia transformation yields an external IRI, but no target class CTR or target pivot relation is provided. It is therefore not a fully specified OTR under the stated pattern.
- **Transformation placement ambiguity:** `LOWER(gender.name)` appears both in the logical-table projection and as the transformation function. Specify one application point.
- **Unstated null behavior:** local and path datatype rules should emit literals only for non-null source attributes; the relevant constraints or runtime behavior are not supplied.

---

## Recommended corrections

1. **Supply `lb:sm_artist` in full.** State its logical relation, subject template, placeholder expression, and class (if any). If it is intended to identify `artist` rows, make its subject constructor identical to `URI_artist` and use `artist` as the pivot.
2. **Provide schema key constraints.** Confirm that `artist.gid`, `medium.id`, and `track.id` are non-null unique keys, or provide another proof that each respective subject template is injective over the selected pivot tuples.
3. **Declare and validate all FK edges used by joins.** In particular, provide the exact FK definitions for both edges of the artist-to-annotation path and every edge of the artist-to-URL/link path. Represent each path in traversal order from its pivot.
4. **Correct and verify the DBpedia SQL join.** Use the actual FK columns connecting `link` to `link_type` and `l_artist_url` to `url`; do not rely on an ambiguous or self-referential join condition. Confirm that the selection predicate and transformation produce valid IRIs.
5. **Make the DBpedia mapping’s formal status explicit.** If it is to be an OTR under this specification, provide the target pivot/CTR and a schema-grounded relational path. If the target is intentionally an external resource not represented by a target pivot relation, document that it is outside the stated pivot-to-pivot OTR pattern rather than claiming full OTR conformance.
6. **Specify artist annotation and gender as Path-DTRs.** Attach both to the verified artist CTR, record the ordered paths, and confirm the relevant FK constraints. For gender, apply `LOWER` exactly once.
7. **Associate the track-number mapping with the track CTR.** Confirm that both track mappings use the same pivot relation and URI constructor; retain the `position IS NOT NULL` condition as the DTR selection condition.
8. **Record non-null behavior and datatype compatibility.** Ensure each DTR handles null source values as required, and validate that the SQL types and RDF datatypes are compatible.

**Conclusion:** the direct artist, medium, and track mappings have the right structural form for entity-preserving CTRs and DTRs, subject to key and URI-injectivity validation. The annotation and gender mappings are plausible Path-DTRs but cannot be attached to a verified artist identity as supplied. The DBpedia `owl:sameAs` mapping is not formally certifiable until its subject map, complete FK path, join condition, and target-resource treatment are resolved.