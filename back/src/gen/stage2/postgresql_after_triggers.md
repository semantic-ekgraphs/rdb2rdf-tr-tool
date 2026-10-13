# PostgreSQL AFTER Trigger Implementation Report

## 1. Synthesis Overview
- **Target Relation(s)**: `artist`, `medium`, and `track` are implemented for the local CTR/DTR rules whose attributes and URI templates are specified in the Transformation Rules.
- **Architecture Compliance**: The generated triggers are statement-level `AFTER` triggers and use PostgreSQL transition tables to capture old and new statement snapshots. They enqueue an event containing the captured components and the computed insertion and deletion changesets in an asynchronous maintenance queue.
- **Scope and validation limits**: This is not a complete implementation of every rule in the supplied maintenance plan. Triggers for `artist_annotation`, `annotation`, `gender`, `l_artist_url`, `link`, `link_type`, and `url` are intentionally not generated: required relations, attributes, foreign keys, or joins are absent or unresolved in the supplied schema information. The provisional `owl:sameAs` candidate is not treated as a verified OTR. The artist trigger consequently computes only the artist CTR and local DTR outputs; it does not maintain the annotation, gender, or candidate `owl:sameAs` rules. No named graph is inferred. URI identity guarantees remain conditional on the stated uniqueness and collision-free-template assumptions.

## 2. Trigger Execution & Component Computation

- **Snapshot Capture**: Separate `INSERT`, `UPDATE`, and `DELETE` statement triggers expose `new_rows`, `old_rows`, or both as transition tables. For an event, the trigger function serializes the available snapshots to JSONB arrays. A missing side of the event is represented by an empty array.
- **Affected Deletion Tuples ($A^-[\Psi](u)$)**: For the implemented pivot rules, the captured old pivot rows are recorded as `components.A_minus`. The trigger retains the entire statement’s old transition set; the queue consumer can identify each pivot tuple from its serialized attributes. This snapshot supports local-rule removal for `artist`, `medium`, and `track`.
- **Post-Update Contributions ($S2[\Psi](u)$)**: The implementation evaluates the local rule outputs of the new snapshot with the specified URI templates, non-null checks, predicates, and datatypes. Those post-event outputs are recorded as `components.S2`. For `DELETE`, the new snapshot and therefore local post-event contributions are empty. Path-rule contributions are not computed by this implementation.
- **Affected Insertion Tuples ($A^+[\Psi](u)$)**: The captured new pivot rows are recorded as `components.A_plus`. They represent inserted or post-update pivot tuples for the implemented local rules.
- **Changesets Computation ($\Delta^+(u)$ and $\Delta^-(u)$)**: The function derives the local rule outputs from both snapshots and computes per-rule JSONB set differences. `delta_plus` contains new `(rule_id, triple)` outputs absent from the old set; `delta_minus` contains old outputs absent from the new set. This is a statement-local difference for the implemented rules, not a global RDF support-count calculation across other rows or rules.

## 3. Asynchronous Maintenance Queue Integration

The SQL below defines `maintenance.rdf_ivm_queue` as the queue contract used by these triggers. Each statement inserts one queue event containing:

- `components.A_minus` and `components.A_plus`: serialized old and new pivot snapshots;
- `components.S2`: the implemented post-event local-rule outputs;
- `delta_plus` and `delta_minus`: per-rule statement-local changesets.

The queue stores compact predicates and class names exactly as supplied (for example, `mo:Track`) and does not invent namespace IRIs or a graph name. A downstream consumer must resolve the compact terms and apply the event to the configured RDF graph. Queue processing, retry policy, and global RDF support accounting are outside this trigger implementation.

## 4. Generated PostgreSQL AFTER Trigger Code

```sql
CREATE SCHEMA IF NOT EXISTS maintenance;

CREATE TABLE IF NOT EXISTS maintenance.rdf_ivm_queue (
    event_id      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    relation_name text        NOT NULL,
    operation     text        NOT NULL
                              CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE')),
    components    jsonb       NOT NULL,
    delta_plus    jsonb       NOT NULL,
    delta_minus   jsonb       NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT clock_timestamp()
);

-- Return local-rule RDF outputs for a JSONB array of pivot rows.
-- Triples retain compact terms from the supplied Transformation Rules.
CREATE OR REPLACE FUNCTION maintenance.ivm_local_rule_triples(
    p_relation text,
    p_rows     jsonb
)
RETURNS TABLE (rule_id text, triple jsonb)
LANGUAGE sql
IMMUTABLE
AS $function$
    WITH rows AS (
        SELECT e.value AS row_data
        FROM jsonb_array_elements(COALESCE(p_rows, '[]'::jsonb)) AS e(value)
    )
    -- artist CTR: mo:MusicArtist(s)
    SELECT
        'psi_artist_01'::text,
        jsonb_build_object(
            'subject',     'http://musicbrainz.org/artist/' ||
                           (row_data ->> 'gid') || '#_',
            'predicate',   'rdf:type',
            'object',      'mo:MusicArtist',
            'object_kind', 'iri'
        )
    FROM rows
    WHERE p_relation = 'artist'
      AND row_data ->> 'gid' IS NOT NULL

    UNION ALL

    -- artist local DTRs
    SELECT
        v.rule_id,
        jsonb_build_object(
            'subject',     'http://musicbrainz.org/artist/' ||
                           (r.row_data ->> 'gid') || '#_',
            'predicate',   v.predicate,
            'object',      r.row_data ->> v.attribute_name,
            'object_kind', 'literal',
            'datatype',    v.datatype
        )
    FROM rows AS r
    CROSS JOIN (
        VALUES
            ('psi_artist_02', 'mo:musicbrainz_guid', 'gid',       'xsd:string'),
            ('psi_artist_03', 'foaf:name',           'name',      'xsd:string'),
            ('psi_artist_04', 'ov:sortLabel',         'sort_name', 'xsd:string')
    ) AS v(rule_id, predicate, attribute_name, datatype)
    WHERE p_relation = 'artist'
      AND r.row_data ->> 'gid' IS NOT NULL
      AND r.row_data ->> v.attribute_name IS NOT NULL

    UNION ALL

    -- medium CTR: mo:Record(s)
    SELECT
        'psi_medium_01'::text,
        jsonb_build_object(
            'subject',     'http://musicbrainz.org/record/' ||
                           (row_data ->> 'id') || '#_',
            'predicate',   'rdf:type',
            'object',      'mo:Record',
            'object_kind', 'iri'
        )
    FROM rows
    WHERE p_relation = 'medium'
      AND row_data ->> 'id' IS NOT NULL

    UNION ALL

    -- medium local DTRs
    SELECT
        v.rule_id,
        jsonb_build_object(
            'subject',     'http://musicbrainz.org/record/' ||
                           (r.row_data ->> 'id') || '#_',
            'predicate',   v.predicate,
            'object',      r.row_data ->> v.attribute_name,
            'object_kind', 'literal',
            'datatype',    v.datatype
        )
    FROM rows AS r
    CROSS JOIN (
        VALUES
            ('psi_medium_05', 'dc:title',       'name',        'xsd:string'),
            ('psi_medium_02', 'mo:track_count', 'track_count', 'xsd:int')
    ) AS v(rule_id, predicate, attribute_name, datatype)
    WHERE p_relation = 'medium'
      AND r.row_data ->> 'id' IS NOT NULL
      AND r.row_data ->> v.attribute_name IS NOT NULL

    UNION ALL

    -- track CTR: mo:Track(s)
    SELECT
        'psi_track_01'::text,
        jsonb_build_object(
            'subject',     'http://musicbrainz.org/track/' ||
                           (row_data ->> 'id') || '#_',
            'predicate',   'rdf:type',
            'object',      'mo:Track',
            'object_kind', 'iri'
        )
    FROM rows
    WHERE p_relation = 'track'
      AND row_data ->> 'id' IS NOT NULL

    UNION ALL

    -- track local DTR; the mapping declares xsd:nonNegativeInteger.
    SELECT
        'psi_track_02'::text,
        jsonb_build_object(
            'subject',     'http://musicbrainz.org/track/' ||
                           (row_data ->> 'id') || '#_',
            'predicate',   'mo:track_number',
            'object',      row_data ->> 'position',
            'object_kind', 'literal',
            'datatype',    'xsd:nonNegativeInteger'
        )
    FROM rows
    WHERE p_relation = 'track'
      AND row_data ->> 'id' IS NOT NULL
      AND row_data ->> 'position' IS NOT NULL;
$function$;


-- Enqueue a statement event, its captured components, and local-rule set differences.
CREATE OR REPLACE FUNCTION maintenance.ivm_enqueue_local_event(
    p_relation text,
    p_operation text,
    p_old_rows jsonb,
    p_new_rows jsonb
)
RETURNS void
LANGUAGE plpgsql
AS $function$
DECLARE
    v_old_rows       jsonb := COALESCE(p_old_rows, '[]'::jsonb);
    v_new_rows       jsonb := COALESCE(p_new_rows, '[]'::jsonb);
    v_old_outputs    jsonb;
    v_new_outputs    jsonb;
    v_delta_plus     jsonb;
    v_delta_minus    jsonb;
BEGIN
    IF p_relation NOT IN ('artist', 'medium', 'track') THEN
        RAISE EXCEPTION
            'No verified local-rule implementation for relation %',
            p_relation;
    END IF;

    SELECT COALESCE(
               jsonb_agg(
                   jsonb_build_object('rule_id', t.rule_id, 'triple', t.triple)
                   ORDER BY t.rule_id, t.triple::text
               ),
               '[]'::jsonb
           )
      INTO v_old_outputs
      FROM maintenance.ivm_local_rule_triples(p_relation, v_old_rows) AS t;

    SELECT COALESCE(
               jsonb_agg(
                   jsonb_build_object('rule_id', t.rule_id, 'triple', t.triple)
                   ORDER BY t.rule_id, t.triple::text
               ),
               '[]'::jsonb
           )
      INTO v_new_outputs
      FROM maintenance.ivm_local_rule_triples(p_relation, v_new_rows) AS t;

    SELECT COALESCE(jsonb_agg(n.item ORDER BY n.item::text), '[]'::jsonb)
      INTO v_delta_plus
      FROM jsonb_array_elements(v_new_outputs) AS n(item)
     WHERE NOT EXISTS (
               SELECT 1
                 FROM jsonb_array_elements(v_old_outputs) AS o(item)
                WHERE o.item = n.item
           );

    SELECT COALESCE(jsonb_agg(o.item ORDER BY o.item::text), '[]'::jsonb)
      INTO v_delta_minus
      FROM jsonb_array_elements(v_old_outputs) AS o(item)
     WHERE NOT EXISTS (
               SELECT 1
                 FROM jsonb_array_elements(v_new_outputs) AS n(item)
                WHERE n.item = o.item
           );

    INSERT INTO maintenance.rdf_ivm_queue (
        relation_name,
        operation,
        components,
        delta_plus,
        delta_minus
    )
    VALUES (
        p_relation,
        p_operation,
        jsonb_build_object(
            'A_minus', v_old_rows,
            'A_plus',  v_new_rows,
            'S2',      v_new_outputs
        ),
        v_delta_plus,
        v_delta_minus
    );
END;
$function$;


-- Shared statement-level trigger function. Dynamic SQL is used so that each
-- event reads only the transition tables declared for that trigger.
CREATE OR REPLACE FUNCTION maintenance.ivm_capture_local_statement()
RETURNS trigger
LANGUAGE plpgsql
AS $function$
DECLARE
    v_old_rows jsonb := '[]'::jsonb;
    v_new_rows jsonb := '[]'::jsonb;
BEGIN
    IF TG_OP IN ('UPDATE', 'DELETE') THEN
        EXECUTE
            'SELECT COALESCE(jsonb_agg(to_jsonb(t)), ''[]''::jsonb)
               FROM old_rows AS t'
        INTO v_old_rows;
    END IF;

    IF TG_OP IN ('UPDATE', 'INSERT') THEN
        EXECUTE
            'SELECT COALESCE(jsonb_agg(to_jsonb(t)), ''[]''::jsonb)
               FROM new_rows AS t'
        INTO v_new_rows;
    END IF;

    PERFORM maintenance.ivm_enqueue_local_event(
        TG_TABLE_NAME,
        TG_OP,
        v_old_rows,
        v_new_rows
    );

    RETURN NULL;
END;
$function$;


-- artist: statement-level transition-table triggers
CREATE TRIGGER artist_ivm_local_insert
AFTER INSERT ON artist
REFERENCING NEW TABLE AS new_rows
FOR EACH STATEMENT
EXECUTE FUNCTION maintenance.ivm_capture_local_statement();

CREATE TRIGGER artist_ivm_local_update
AFTER UPDATE ON artist
REFERENCING OLD TABLE AS old_rows NEW TABLE AS new_rows
FOR EACH STATEMENT
EXECUTE FUNCTION maintenance.ivm_capture_local_statement();

CREATE TRIGGER artist_ivm_local_delete
AFTER DELETE ON artist
REFERENCING OLD TABLE AS old_rows
FOR EACH STATEMENT
EXECUTE FUNCTION maintenance.ivm_capture_local_statement();


-- medium: statement-level transition-table triggers
CREATE TRIGGER medium_ivm_local_insert
AFTER INSERT ON medium
REFERENCING NEW TABLE AS new_rows
FOR EACH STATEMENT
EXECUTE FUNCTION maintenance.ivm_capture_local_statement();

CREATE TRIGGER medium_ivm_local_update
AFTER UPDATE ON medium
REFERENCING OLD TABLE AS old_rows NEW TABLE AS new_rows
FOR EACH STATEMENT
EXECUTE FUNCTION maintenance.ivm_capture_local_statement();

CREATE TRIGGER medium_ivm_local_delete
AFTER DELETE ON medium
REFERENCING OLD TABLE AS old_rows
FOR EACH STATEMENT
EXECUTE FUNCTION maintenance.ivm_capture_local_statement();


-- track: statement-level transition-table triggers
CREATE TRIGGER track_ivm_local_insert
AFTER INSERT ON track
REFERENCING NEW TABLE AS new_rows
FOR EACH STATEMENT
EXECUTE FUNCTION maintenance.ivm_capture_local_statement();

CREATE TRIGGER track_ivm_local_update
AFTER UPDATE ON track
REFERENCING OLD TABLE AS old_rows NEW TABLE AS new_rows
FOR EACH STATEMENT
EXECUTE FUNCTION maintenance.ivm_capture_local_statement();

CREATE TRIGGER track_ivm_local_delete
AFTER DELETE ON track
REFERENCING OLD TABLE AS old_rows
FOR EACH STATEMENT
EXECUTE FUNCTION maintenance.ivm_capture_local_statement();
```

**Rules not emitted as triggers:** `artist_annotation`/`annotation` (`psi_artist_13`), `gender` (`psi_artist_07`), and the candidate `owl:sameAs` rule (`psi_artist_14`) require schema and path validation before executable joins can be synthesized. In particular, the annotation-side foreign key, the `gender` relation definition, and the candidate path joins—including the ambiguous `link_type` join—are not established by the supplied input.