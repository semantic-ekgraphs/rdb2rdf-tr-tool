# Generated Transformation Rules Report

## 1. Overview

Compiled **12 rules** from the supplied R2RML mappings:

| Rule category | Count |
|---|---:|
| CTR | 3 |
| OTR | 1 |
| Local DTR | 6 |
| Path DTR | 2 |
| **Total** | **12** |

The `owl:sameAs` mapping is classified as an **OTR candidate**, but the supplied metadata does not establish a target pivot relation or target CTR for its external IRI. Its rule is therefore given as a provisional operational formula, **not as a verified OTR conforming to the framework**. The annotation path is also incompletely validated because the supplied metadata does not name all required foreign-key constraints.

The subject URI predicates used below are:

- `URI_artist(a,s) ≡ hasURI("http://musicbrainz.org/artist/{gid}#_", ⟨a.gid⟩, s)`
- `URI_medium(m,s) ≡ hasURI("http://musicbrainz.org/record/{id}#_", ⟨m.id⟩, s)`
- `URI_track(t,s) ≡ hasURI("http://musicbrainz.org/track/{id}#_", ⟨t.id⟩, s)`

The distinct-tuple identity guarantee for these predicates is **conditional**: the supplied metadata does not establish that `artist.gid`, `medium.id`, or `track.id` is unique. In the specifications, `RDFLiteral(x,A,R,v)` denotes the literal representation of value `x` from attribute `A` of relation `R`; `nonNull(x)` denotes that `x` is not null.

## 2. Compiled Transformation Rules

### 2.1 Artist class

- **TriplesMap Identifier**: `lb:Artist`
- **Rule Identifier**: `\psi_artist_01`
- **Rule Type**: CTR
- **Pivot Relation**: `artist`
- **Formal TR Specification**:

  \[
  \psi_{\text{artist\_01}}:
  \quad
  \texttt{mo:MusicArtist}(s)
  \leftarrow
  \texttt{artist}(a),\ URI_{\texttt{artist}}(a,s)
  \]

  Subject identity is conditional on `artist.gid` being unique and template instantiation being collision-free.

- **Relational Path**: None; this is a local pivot rule.

---

### 2.2 Artist MusicBrainz GUID

- **TriplesMap Identifier**: `lb:Artist`
- **Rule Identifier**: `\psi_artist_02`
- **Rule Type**: Local DTR
- **Pivot Relation**: `artist`
- **Formal TR Specification**:

  \[
  \psi_{\text{artist\_02}}:
  \quad
  \texttt{mo:musicbrainz\_guid}(s,v)
  \leftarrow
  \texttt{artist}(a),\ URI_{\texttt{artist}}(a,s),
  \ nonNull(a.gid),
  \ RDFLiteral(a.gid,\texttt{"gid"},\texttt{artist},v)
  \]

  The mapped literal datatype is `xsd:string`. Subject identity is conditional on `artist.gid` being unique.

- **Relational Path**: None; local DTR attribute `artist.gid`.

---

### 2.3 Artist name

- **TriplesMap Identifier**: `lb:Artist`
- **Rule Identifier**: `\psi_artist_03`
- **Rule Type**: Local DTR
- **Pivot Relation**: `artist`
- **Formal TR Specification**:

  \[
  \psi_{\text{artist\_03}}:
  \quad
  \texttt{foaf:name}(s,v)
  \leftarrow
  \texttt{artist}(a),\ URI_{\texttt{artist}}(a,s),
  \ nonNull(a.name),
  \ RDFLiteral(a.name,\texttt{"name"},\texttt{artist},v)
  \]

  The mapped literal datatype is `xsd:string`. Subject identity is conditional on `artist.gid` being unique.

- **Relational Path**: None; local DTR attribute `artist.name`.

---

### 2.4 Artist sort label

- **TriplesMap Identifier**: `lb:Artist`
- **Rule Identifier**: `\psi_artist_04`
- **Rule Type**: Local DTR
- **Pivot Relation**: `artist`
- **Formal TR Specification**:

  \[
  \psi_{\text{artist\_04}}:
  \quad
  \texttt{ov:sortLabel}(s,v)
  \leftarrow
  \texttt{artist}(a),\ URI_{\texttt{artist}}(a,s),
  \ nonNull(a.sort\_name),
  \ RDFLiteral(a.sort\_name,\texttt{"sort\_name"},\texttt{artist},v)
  \]

  The mapped literal datatype is `xsd:string`. Subject identity is conditional on `artist.gid` being unique.

- **Relational Path**: None; local DTR attribute `artist.sort_name`.

---

### 2.5 Artist external DBpedia link

- **TriplesMap Identifier**: `lb:artist_dbpedia`
- **Rule Identifier**: `\psi_artist_14`
- **Rule Type**: OTR — **candidate; not verified as a conforming OTR**
- **Pivot Relation**: `artist` for the subject. No target pivot relation is established for the external IRI.
- **Formal TR Specification**:

  The framework’s OTR pattern requires a target pivot tuple and a target CTR that generates the object resource. Neither is supplied for the transformed external IRI, so a verified, framework-conforming OTR cannot be formed. The following is the provisional operational rule represented by the mapping:

  \[
  \begin{aligned}
  \psi_{\text{artist\_14}}^{\text{candidate}}:
  \quad
  \texttt{owl:sameAs}(s,o)
  \leftarrow\;&
  \texttt{artist}(a),\ URI_{\texttt{artist}}(a,s),\\
  &\texttt{l\_artist\_url}(x),\
  \texttt{link}(l),\
  \texttt{link\_type}(lt),\
  \texttt{url}(u),\\
  &\delta_{\text{dbpedia}}(lt,u),\
  \texttt{nonNull}(u.url),\\
  &u'=\operatorname{REPLACE}(
       \operatorname{REPLACE}(u.url,
       \texttt{'wikipedia.org/wiki'},
       \texttt{'dbpedia.org/resource'}),
       \texttt{'http://en.'},
       \texttt{'http://'}),\\
  &\operatorname{RDFIRI}(u',o),\
  \phi_{\text{dbpedia}}(a,x,l,lt,u)
  \end{aligned}
  \]

  Here, \(\delta_{\text{dbpedia}}\) is the mapping selection condition:

  \[
  lt.gid=\texttt{'29651736-fa6d-48e4-aadc-a557c6add1cb'}
  \quad\land\quad
  u.url\ \texttt{SIMILAR TO}\
  \texttt{'http://(de|el|en|es|ko|pl|pt).wikipedia.org/wiki/\%'}
  \]

  The `owl:sameAs` object is intended to be an IRI, but the supplied metadata does not establish the source URL’s schema type or prove that every transformed value is a valid IRI. This formula captures the mapping’s apparent intent; it does **not** establish the target-pivot correspondence required by a conforming OTR.

- **Relational Path**: The intended traversal is:

  \[
  \phi_{\text{dbpedia}}:
  \quad
  \texttt{artist.id}
  \rightarrow
  \texttt{l\_artist\_url.entity0}
  \rightarrow
  \texttt{l\_artist\_url.link}
  \rightarrow
  \texttt{link}
  \rightarrow
  \texttt{link\_type}
  \quad\text{and}\quad
  \texttt{l\_artist\_url.entity1}
  \rightarrow
  \texttt{url.id}
  \]

  This path is placed as the final body term. Only `l_artist_url_fk_entity0` is named in the supplied metadata; the complete path is therefore **not schema-validated**. The SQL join `link_type = link_type.id` is ambiguous or erroneous as written and must be corrected or clarified before this rule can be validated.

---

### 2.6 Artist annotation comment

- **TriplesMap Identifier**: `lb:artist_annotation`
- **Rule Identifier**: `\psi_artist_13`
- **Rule Type**: Path DTR
- **Pivot Relation**: `artist`
- **Formal TR Specification**:

  \[
  \begin{aligned}
  \psi_{\text{artist\_13}}:
  \quad
  \texttt{rdfs:comment}(s,v)
  \leftarrow\;&
  \texttt{artist}(a),\ URI_{\texttt{artist}}(a,s),\\
  &\texttt{annotation}(n),\
  \texttt{nonNull}(n.text),\
  \texttt{RDFLiteral}(n.text,\texttt{"text"},\texttt{annotation},v),\\
  &\phi_{\text{annotation}}(a,n)
  \end{aligned}
  \]

  The mapped literal datatype is `xsd:string`. Subject identity is conditional on `artist.gid` being unique.

- **Relational Path**: The intended artist-to-annotation traversal is:

  \[
  \phi_{\text{annotation}}:
  \quad
  \texttt{artist.id}
  \rightarrow
  \texttt{artist\_annotation.artist}
  \rightarrow
  \texttt{artist\_annotation.annotation}
  \rightarrow
  \texttt{annotation.id}
  \]

  This path is the final body term. The supplied metadata names `artist_annotation_fk_artist`, but does not name the annotation-side FK; consequently, the complete path is not schema-validated. The `text` column’s schema type and nullability are also not supplied.

---

### 2.7 Artist gender

- **TriplesMap Identifier**: `lb:artist_gender`
- **Rule Identifier**: `\psi_artist_07`
- **Rule Type**: Path DTR
- **Pivot Relation**: `artist`
- **Formal TR Specification**:

  \[
  \begin{aligned}
  \psi_{\text{artist\_07}}:
  \quad
  \texttt{foaf:gender}(s,v)
  \leftarrow\;&
  \texttt{artist}(a),\ URI_{\texttt{artist}}(a,s),\\
  &\texttt{gender}(g),\
  \texttt{nonNull}(g.name),\\
  &\texttt{RDFLiteral}(g.name,\texttt{"name"},\texttt{gender},v_0),\\
  &\operatorname{LOWER}([v_0],v),\
  F_{\texttt{artist\_fk\_gender}}(a,g)
  \end{aligned}
  \]

  The mapping’s value transformation is `LOWER(gender.name)` and the declared RDF datatype is `xsd:string`. Subject identity is conditional on `artist.gid` being unique.

- **Relational Path**: The final body term is the schema-validated FK traversal:

  \[
  F_{\texttt{artist\_fk\_gender}}(a,g):
  \quad
  \texttt{artist.gender}
  \rightarrow
  \texttt{gender.id}
  \]

  The supplied metadata does not state the type or nullability of `gender.name`.

---

### 2.8 Medium class

- **TriplesMap Identifier**: `lb:Medium`
- **Rule Identifier**: `\psi_medium_01`
- **Rule Type**: CTR
- **Pivot Relation**: `medium`
- **Formal TR Specification**:

  \[
  \psi_{\text{medium\_01}}:
  \quad
  \texttt{mo:Record}(s)
  \leftarrow
  \texttt{medium}(m),\ URI_{\texttt{medium}}(m,s)
  \]

  Subject identity is conditional on `medium.id` being unique and template instantiation being collision-free. Confirm that representing medium rows as `mo:Record` in the `/record/` namespace is intentional.

- **Relational Path**: None; this is a local pivot rule.

---

### 2.9 Medium title

- **TriplesMap Identifier**: `lb:Medium`
- **Rule Identifier**: `\psi_medium_05`
- **Rule Type**: Local DTR
- **Pivot Relation**: `medium`
- **Formal TR Specification**:

  \[
  \psi_{\text{medium\_05}}:
  \quad
  \texttt{dc:title}(s,v)
  \leftarrow
  \texttt{medium}(m),\ URI_{\texttt{medium}}(m,s),
  \ nonNull(m.name),
  \ RDFLiteral(m.name,\texttt{"name"},\texttt{medium},v)
  \]

  The mapped literal datatype is `xsd:string`. Subject identity is conditional on `medium.id` being unique.

- **Relational Path**: None; local DTR attribute `medium.name`.

---

### 2.10 Medium track count

- **TriplesMap Identifier**: `lb:Medium`
- **Rule Identifier**: `\psi_medium_02`
- **Rule Type**: Local DTR
- **Pivot Relation**: `medium`
- **Formal TR Specification**:

  \[
  \psi_{\text{medium\_02}}:
  \quad
  \texttt{mo:track\_count}(s,v)
  \leftarrow
  \texttt{medium}(m),\ URI_{\texttt{medium}}(m,s),
  \ nonNull(m.track\_count),
  \ RDFLiteral(m.track\_count,\texttt{"track\_count"},\texttt{medium},v)
  \]

  The mapped literal datatype is `xsd:int`. Subject identity is conditional on `medium.id` being unique.

- **Relational Path**: None; local DTR attribute `medium.track_count`.

---

### 2.11 Track class

- **TriplesMap Identifier**: `lb:Track_psi_track_01`
- **Rule Identifier**: `\psi_track_01`
- **Rule Type**: CTR
- **Pivot Relation**: `track`
- **Formal TR Specification**:

  \[
  \psi_{\text{track\_01}}:
  \quad
  \texttt{mo:Track}(s)
  \leftarrow
  \texttt{track}(t),\ URI_{\texttt{track}}(t,s)
  \]

  Subject identity is conditional on `track.id` being unique and template instantiation being collision-free.

- **Relational Path**: None; this is a local pivot rule.

---

### 2.12 Track number

- **TriplesMap Identifier**: `lb:Track_psi_track_02`
- **Rule Identifier**: `\psi_track_02`
- **Rule Type**: Local DTR
- **Pivot Relation**: `track`
- **Formal TR Specification**:

  \[
  \begin{aligned}
  \psi_{\text{track\_02}}:
  \quad
  \texttt{mo:track\_number}(s,v)
  \leftarrow\;&
  \texttt{track}(t),\ URI_{\texttt{track}}(t,s),\\
  &\delta_{\text{track\_02}}(t),\
  \texttt{nonNull}(t.position),\\
  &\texttt{RDFLiteral}(t.position,\texttt{"position"},\texttt{track},v)
  \end{aligned}
  \]

  where:

  \[
  \delta_{\text{track\_02}}(t)
  \equiv
  t.position\ \texttt{IS NOT NULL}
  \]

  The mapped RDF datatype is `xsd:nonNegativeInteger`. The filter is apparently redundant given the supplied `INTEGER NOT NULL` metadata. The metadata does not establish that every `position` value is nonnegative, so conformance with the declared RDF datatype should be confirmed. Subject identity is conditional on `track.id` being unique.

- **Relational Path**: None; local DTR attribute `track.position`.