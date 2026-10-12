# Test Generation and Synthetic Dataset Report

## 1. Overview
- **Target Database Relations**: The generated AFTER triggers implement local rules for `artist`, `medium`, and `track`. The scenarios also cover the transformation-rule path inputs `artist_annotation`, `annotation`, `gender`, `l_artist_url`, `link`, `link_type`, and `url`. The latter path relations are exercised in an isolated test harness because the supplied trigger implementation does not generate triggers for them and the supplied schema does not define enough information to validate their paths.
- **Test Scope**: The suite covers statement-level `INSERT`, `UPDATE`, and `DELETE` operations; checks trigger queue events, rule contributions, and per-rule insertion/deletion deltas against an independently written rematerialization oracle; and supplies path fixtures for annotation, gender, and the provisional DBpedia-link mapping. Each trigger test runs inside a transaction that ends with `ROLLBACK`, so the suite is repeatable. The core tests require the generated trigger functions and the `artist`, `medium`, and `track` tables to exist in the current database.

**Scope and interpretation constraints**

- The generated triggers cover only the local rules: `psi_artist_01`–`psi_artist_04`, `psi_medium_01`, `psi_medium_05`, `psi_medium_02`, `psi_track_01`, and `psi_track_02`.
- Queue deltas are statement-local and do not test global RDF support counts across other tuples or rules.
- The annotation, gender, and candidate `owl:sameAs` scenarios are path-oracle fixtures, **not** evidence that corresponding PostgreSQL triggers exist or have been runtime-validated.
- The candidate URL path uses an explicitly declared test-harness join convention. It does not resolve the reported ambiguity in the production mapping.
- The core fixture selects existing `release`, `recording`, and `artist_credit` rows to satisfy foreign keys. It raises an exception if those prerequisites are absent.

## 2. Representative Update Scenarios

### INSERT Scenarios

| Scenario | Relation(s) | Operation | Expected validation |
|---|---|---|---|
| I-A1 | `artist` | Insert two artists in one statement | One queue event; `A_plus` has both rows; the oracle finds class, GUID, name, and sort-label contributions; `delta_plus` equals the new local output set; `delta_minus` is empty. |
| I-M1 | `medium` | Insert two media in one statement | One queue event; each row contributes `mo:Record`, `dc:title`, and `mo:track_count`; oracle and queue agree. |
| I-T1 | `track` | Insert one track | One queue event; the track contributes `mo:Track` and `mo:track_number`; oracle and queue agree. |
| I-P1 | Path harness | Insert annotation association, gender association, and artist-to-URL path rows | Full-rematerialization path queries find the expected comment, lowercased gender, and selected/transformed candidate URL outputs. No generated path trigger is assumed. |

### DELETE Scenarios

| Scenario | Relation(s) | Operation | Expected validation |
|---|---|---|---|
| D-T1 | `track` | Delete the fixture track | `A_minus` contains the old track; all its local contributions appear in `delta_minus`; `delta_plus` is empty. |
| D-M1 | `medium` | Delete the two fixture media after deleting the track | Each old medium’s local contributions are deleted; oracle and queue agree. |
| D-A1 | `artist` | Delete the two fixture artists after removing the fixture association rows | Each old artist’s local contributions are deleted; oracle and queue agree. |
| D-P1 | Path harness | Delete annotation association, gender association, and URL-path association | Path rematerialization no longer returns the corresponding outputs. This tests the path oracle, not a generated trigger. |

### UPDATE Scenarios

| Scenario | Relation(s) | Operation | Expected validation |
|---|---|---|---|
| U-A1 | `artist` | Change `gid`, `name`, and `sort_name` for one fixture artist | Old-subject outputs absent from the new state are in `delta_minus`; new-subject outputs are in `delta_plus`; unchanged artist outputs are not reported as changes. |
| U-M1 | `medium` | Change `name` and `track_count` | The `mo:Record` class remains supported; old title/count literals are removed and new values are added. |
| U-T1 | `track` | Change `position`, `number`, and `medium` | The local track subject remains the same; the mapped number literal changes. The `medium` move is also represented in the captured row snapshots, although the generated track rules do not map that foreign key. |
| U-P1 | Path harness | Change annotation text, gender name, URL value, and URL-path endpoint | Full rematerialization reflects the new comment, `LOWER(gender.name)`, and transformed URL output; old path outputs disappear where their source path no longer matches. |

The test intentionally does **not** insert nulls into `artist.name`, `artist.sort_name`, `medium.name`, or other non-null constrained columns. Those conditions cannot be reached through valid rows in the supplied schema. It does validate that nullable values are filtered where the implemented rule permits them by checking the rule definitions and using normal valid rows. The track fixture uses a nonnegative position; negative `position` behavior is not tested as an RDF `xsd:nonNegativeInteger`, since the supplied relational schema does not constrain it to be nonnegative.

## 3. Synthetic Datasets & Complex Paths

### Complex Relational Paths

The path harness supplies deliberately small, inspectable examples:

1. **Artist-to-annotation path**: a fixture artist joins through `artist_annotation.artist` and `artist_annotation.annotation` to `ivm_test.annotation.id`. Two annotations for one artist make it possible to detect lost or duplicated path contributions. Deleting or changing an association or annotation changes the rematerialized `rdfs:comment` set.
2. **Artist-to-gender path**: `ivm_test.artist_gender.artist` joins to `ivm_test.gender.id`; the oracle applies `LOWER(gender.name)`. The isolated mapping avoids making unsupported assumptions about the production `gender` table’s schema.
3. **Candidate artist-to-URL path**: `ivm_test.l_artist_url` joins to `ivm_test.link`, then `ivm_test.link_type`, while `entity1` joins to `ivm_test.url.id`. The fixture includes one selected Wikipedia URL and one non-selected URL. The harness states its join convention explicitly; it is not a production-schema validation.

The main trigger fixture creates two artists, two media, and one track. It uses distinct artist GUIDs and separate medium positions, and selects existing referenced rows for foreign-key validity.

### Edge Cases & Boundary Conditions

- **Statement cardinality**: multi-row `artist` and `medium` inserts exercise transition tables with more than one row; single-row track operations exercise the one-row case.
- **Empty transition sides**: inserts have an empty old side, deletes have an empty new side, and updates have both sides populated.
- **Changed URI identity**: the artist update changes `gid`, testing removal of outputs under the old subject and insertion under the new subject.
- **Unchanged contributions**: the medium and track class contributions remain present across attribute updates; the expected delta should not include unchanged class triples.
- **Foreign-key movement**: the track update changes `medium`; the local track rules should still emit only the class and track-number outputs defined for `track`.
- **No-match path cases**: non-selected URL link types and URL values outside the intended Wikipedia pattern produce no candidate output in the path oracle.
- **Null and schema boundaries**: the dataset avoids violating `NOT NULL`, CHECK, uniqueness, and foreign-key constraints. The schema’s omitted annotation/gender/URL relation definitions are isolated from the core trigger tests.
- **Repeatability**: all core data and queue events are rolled back after validation. The fixture uses existing dependency IDs and computes unused medium/track positions from current table contents.

## 4. Reproducible SQL Test Scripts

Run the following as a single `psql` script after loading the relational schema and installing the generated PostgreSQL triggers. The core test fails early if required dependency rows or generated trigger functions are missing. It uses the generated queue contract from the trigger report.

```sql
\set ON_ERROR_STOP 1

BEGIN;

-- Fail early if the generated implementation or required dependency data
-- is unavailable. The fixture intentionally reuses valid referenced rows.
DO $$
BEGIN
    IF to_regclass('maintenance.rdf_ivm_queue') IS NULL THEN
        RAISE EXCEPTION 'maintenance.rdf_ivm_queue is missing; install the generated trigger implementation first';
    END IF;

    IF to_regprocedure('maintenance.ivm_local_rule_triples(text,jsonb)') IS NULL THEN
        RAISE EXCEPTION 'maintenance.ivm_local_rule_triples(text,jsonb) is missing';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM release) THEN
        RAISE EXCEPTION 'The test requires at least one existing release row';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM recording) THEN
        RAISE EXCEPTION 'The test requires at least one existing recording row';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM artist_credit) THEN
        RAISE EXCEPTION 'The test requires at least one existing artist_credit row';
    END IF;
END;
$$;

CREATE TEMP TABLE ivm_test_start (
    event_id bigint NOT NULL
) ON COMMIT DROP;

INSERT INTO ivm_test_start(event_id)
SELECT COALESCE(MAX(event_id), 0)
FROM maintenance.rdf_ivm_queue;

CREATE TEMP TABLE ivm_test_artist (
    label text PRIMARY KEY,
    id    integer NOT NULL,
    gid   uuid NOT NULL
) ON COMMIT DROP;

CREATE TEMP TABLE ivm_test_medium (
    label text PRIMARY KEY,
    id    integer NOT NULL
) ON COMMIT DROP;

CREATE TEMP TABLE ivm_test_track (
    id integer NOT NULL
) ON COMMIT DROP;

-- Independent, full-rematerialization oracle for the implemented local rules.
-- This function returns the same rule_id/triple envelope as the queue, but
-- reconstructs outputs directly from the captured row snapshots.
CREATE SCHEMA IF NOT EXISTS ivm_test;

CREATE OR REPLACE FUNCTION ivm_test.oracle_outputs(
    p_relation text,
    p_rows jsonb
)
RETURNS jsonb
LANGUAGE sql
IMMUTABLE
AS $oracle$
    WITH rows AS (
        SELECT e.value AS row_data
        FROM jsonb_array_elements(COALESCE(p_rows, '[]'::jsonb)) AS e(value)
    ),
    outputs(rule_id, triple) AS (
        -- Artist CTR
        SELECT
            'psi_artist_01'::text,
            jsonb_build_object(
                'subject', 'http://musicbrainz.org/artist/' ||
                           (r.row_data ->> 'gid') || '#_',
                'predicate', 'rdf:type',
                'object', 'mo:MusicArtist',
                'object_kind', 'iri'
            )
        FROM rows AS r
        WHERE p_relation = 'artist'
          AND r.row_data ->> 'gid' IS NOT NULL

        UNION ALL

        -- Artist local DTRs
        SELECT
            v.rule_id,
            jsonb_build_object(
                'subject', 'http://musicbrainz.org/artist/' ||
                           (r.row_data ->> 'gid') || '#_',
                'predicate', v.predicate,
                'object', r.row_data ->> v.attribute_name,
                'object_kind', 'literal',
                'datatype', 'xsd:string'
            )
        FROM rows AS r
        CROSS JOIN (
            VALUES
                ('psi_artist_02', 'mo:musicbrainz_guid', 'gid'),
                ('psi_artist_03', 'foaf:name',           'name'),
                ('psi_artist_04', 'ov:sortLabel',        'sort_name')
        ) AS v(rule_id, predicate, attribute_name)
        WHERE p_relation = 'artist'
          AND r.row_data ->> 'gid' IS NOT NULL
          AND r.row_data ->> v.attribute_name IS NOT NULL

        UNION ALL

        -- Medium CTR
        SELECT
            'psi_medium_01'::text,
            jsonb_build_object(
                'subject', 'http://musicbrainz.org/record/' ||
                           (r.row_data ->> 'id') || '#_',
                'predicate', 'rdf:type',
                'object', 'mo:Record',
                'object_kind', 'iri'
            )
        FROM rows AS r
        WHERE p_relation = 'medium'
          AND r.row_data ->> 'id' IS NOT NULL

        UNION ALL

        -- Medium local DTRs
        SELECT
            v.rule_id,
            jsonb_build_object(
                'subject', 'http://musicbrainz.org/record/' ||
                           (r.row_data ->> 'id') || '#_',
                'predicate', v.predicate,
                'object', r.row_data ->> v.attribute_name,
                'object_kind', 'literal',
                'datatype', v.datatype
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

        -- Track CTR
        SELECT
            'psi_track_01'::text,
            jsonb_build_object(
                'subject', 'http://musicbrainz.org/track/' ||
                           (r.row_data ->> 'id') || '#_',
                'predicate', 'rdf:type',
                'object', 'mo:Track',
                'object_kind', 'iri'
            )
        FROM rows AS r
        WHERE p_relation = 'track'
          AND r.row_data ->> 'id' IS NOT NULL

        UNION ALL

        -- Track local DTR
        SELECT
            'psi_track_02'::text,
            jsonb_build_object(
                'subject', 'http://musicbrainz.org/track/' ||
                           (r.row_data ->> 'id') || '#_',
                'predicate', 'mo:track_number',
                'object', r.row_data ->> 'position',
                'object_kind', 'literal',
                'datatype', 'xsd:nonNegativeInteger'
            )
        FROM rows AS r
        WHERE p_relation = 'track'
          AND r.row_data ->> 'id' IS NOT NULL
          AND r.row_data ->> 'position' IS NOT NULL
    )
    SELECT COALESCE(
        jsonb_agg(
            jsonb_build_object('rule_id', d.rule_id, 'triple', d.triple)
            ORDER BY d.rule_id, d.triple::text
        ),
        '[]'::jsonb
    )
    FROM (
        SELECT DISTINCT rule_id, triple
        FROM outputs
    ) AS d;
$oracle$;

-- Set difference over arrays of {rule_id, triple} objects.
CREATE OR REPLACE FUNCTION ivm_test.jsonb_set_difference(
    p_left jsonb,
    p_right jsonb
)
RETURNS jsonb
LANGUAGE sql
IMMUTABLE
AS $diff$
    SELECT COALESCE(
        jsonb_agg(x.item ORDER BY x.item::text),
        '[]'::jsonb
    )
    FROM jsonb_array_elements(COALESCE(p_left, '[]'::jsonb)) AS x(item)
    WHERE NOT EXISTS (
        SELECT 1
        FROM jsonb_array_elements(COALESCE(p_right, '[]'::jsonb)) AS y(item)
        WHERE y.item = x.item
    );
$diff$;

-- I-A1: multi-row artist INSERT.
WITH inserted AS (
    INSERT INTO artist (gid, name, sort_name)
    VALUES
        ('10000000-0000-4000-8000-000000000001', 'IVM Artist Alpha', 'Alpha, IVM'),
        ('10000000-0000-4000-8000-000000000002', 'IVM Artist Beta',  'Beta, IVM')
    RETURNING id, gid, name
)
INSERT INTO ivm_test_artist(label, id, gid)
SELECT
    CASE name
        WHEN 'IVM Artist Alpha' THEN 'alpha'
        ELSE 'beta'
    END,
    id,
    gid
FROM inserted;

-- I-M1: multi-row medium INSERT. Use unused positions for an existing release.
WITH release_choice AS (
    SELECT min(id) AS release_id
    FROM release
),
position_base AS (
    SELECT COALESCE(MAX(position), 0) + 10000 AS base_position
    FROM medium
    WHERE release = (SELECT release_id FROM release_choice)
),
inserted AS (
    INSERT INTO medium (release, position, name, track_count)
    SELECT
        rc.release_id,
        pb.base_position + v.offset,
        v.medium_name,
        v.track_count
    FROM release_choice AS rc
    CROSS JOIN position_base AS pb
    CROSS JOIN (
        VALUES
            (0, 'IVM Medium One', 2),
            (1, 'IVM Medium Two', 0)
    ) AS v(offset, medium_name, track_count)
    RETURNING id, position
)
INSERT INTO ivm_test_medium(label, id)
SELECT
    CASE position
        WHEN (SELECT base_position FROM position_base) THEN 'one'
        ELSE 'two'
    END,
    id
FROM inserted
CROSS JOIN position_base;

-- I-T1: track INSERT on the first fixture medium.
WITH dependency AS (
    SELECT
        (SELECT min(id) FROM recording) AS recording_id,
        (SELECT min(id) FROM artist_credit) AS artist_credit_id,
        (SELECT id FROM ivm_test_medium WHERE label = 'one') AS medium_id
),
position_base AS (
    SELECT COALESCE(MAX(position), 0) + 10000 AS base_position
    FROM track
    WHERE medium = (SELECT medium_id FROM dependency)
),
inserted AS (
    INSERT INTO track (
        gid, recording, medium, position, number, name, artist_credit
    )
    SELECT
        '20000000-0000-4000-8000-000000000001',
        d.recording_id,
        d.medium_id,
        pb.base_position,
        'IVM-1',
        'IVM Track Original',
        d.artist_credit_id
    FROM dependency AS d
    CROSS JOIN position_base AS pb
    RETURNING id
)
INSERT INTO ivm_test_track(id)
SELECT id
FROM inserted;

-- U-A1: change the URI identity as well as the two mapped string attributes.
UPDATE artist
SET gid       = '10000000-0000-4000-8000-000000000011',
    name      = 'IVM Artist Alpha Updated',
    sort_name = 'Updated, Alpha'
WHERE id = (SELECT id FROM ivm_test_artist WHERE label = 'alpha');

-- U-M1: change both medium local DTR values; the CTR remains unchanged.
UPDATE medium
SET name = 'IVM Medium One Updated',
    track_count = 7
WHERE id = (SELECT id FROM ivm_test_medium WHERE label = 'one');

-- U-T1: change the local mapped position and move the row to the second medium.
-- The second medium has no track fixture, so its position can use 10000.
UPDATE track
SET position = 10000,
    number = 'IVM-2',
    medium = (SELECT id FROM ivm_test_medium WHERE label = 'two')
WHERE id = (SELECT id FROM ivm_test_track);

-- -------------------------------------------------------------------------
-- Isolated path fixtures. These are deliberately not attached to the
-- production triggers: the supplied trigger implementation does not emit
-- triggers for these relations.
-- -------------------------------------------------------------------------

CREATE TABLE ivm_test.annotation (
    id   integer PRIMARY KEY,
    text text
);

CREATE TABLE ivm_test.gender (
    id   integer PRIMARY KEY,
    name text
);

CREATE TABLE ivm_test.artist_gender (
    artist integer NOT NULL,
    gender integer NOT NULL,
    PRIMARY KEY (artist, gender)
);

CREATE TABLE ivm_test.link_type (
    id  integer PRIMARY KEY,
    gid uuid NOT NULL
);

CREATE TABLE ivm_test.url (
    id  integer PRIMARY KEY,
    url text
);

CREATE TABLE ivm_test.link (
    id        integer PRIMARY KEY,
    link_type integer NOT NULL REFERENCES ivm_test.link_type(id)
);

CREATE TABLE ivm_test.l_artist_url (
    id       integer PRIMARY KEY,
    entity0  integer NOT NULL,
    link     integer NOT NULL REFERENCES ivm_test.link(id),
    entity1  integer NOT NULL REFERENCES ivm_test.url(id)
);

INSERT INTO ivm_test.annotation(id, text)
VALUES (9001, 'First synthetic annotation'),
       (9002, 'Second synthetic annotation');

-- The annotation relation is absent from the supplied schema excerpt.
-- artist_annotation itself is supplied and has no annotation-side FK here.
INSERT INTO artist_annotation(artist, annotation)
SELECT a.id, x.annotation_id
FROM ivm_test_artist AS a
CROSS JOIN (
    VALUES (9001), (9002)
) AS x(annotation_id)
WHERE a.label = 'alpha';

INSERT INTO ivm_test.gender(id, name)
VALUES (9101, 'FEMALE');

INSERT INTO ivm_test.artist_gender(artist, gender)
SELECT a.id, 9101
FROM ivm_test_artist AS a
WHERE a.label = 'alpha';

INSERT INTO ivm_test.link_type(id, gid)
VALUES (
    9201,
    '29651736-fa6d-48e4-aadc-a557c6add1cb'
);

INSERT INTO ivm_test.url(id, url)
VALUES
    (9301, 'http://en.wikipedia.org/wiki/IVM_Example'),
    (9302, 'https://example.org/not-a-wikipedia-link');

INSERT INTO ivm_test.link(id, link_type)
VALUES (9401, 9201);

INSERT INTO ivm_test.l_artist_url(id, entity0, link, entity1)
SELECT 9501, a.id, 9401, 9301
FROM ivm_test_artist AS a
WHERE a.label = 'alpha';

-- Full-rematerialization path checks for the synthetic rows.
-- Expected: two comments, one lowercased gender, and one transformed URL.
DO $$
DECLARE
    v_count integer;
BEGIN
    SELECT count(*)
    INTO v_count
    FROM artist AS a
    JOIN artist_annotation AS aa ON aa.artist = a.id
    JOIN ivm_test.annotation AS n ON n.id = aa.annotation
    WHERE a.id = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
      AND n.text IS NOT NULL;

    IF v_count <> 2 THEN
        RAISE EXCEPTION 'Annotation path oracle expected 2 rows, got %', v_count;
    END IF;

    SELECT count(*)
    INTO v_count
    FROM ivm_test.artist_gender AS ag
    JOIN ivm_test.gender AS g ON g.id = ag.gender
    WHERE ag.artist = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
      AND g.name IS NOT NULL
      AND lower(g.name) = 'female';

    IF v_count <> 1 THEN
        RAISE EXCEPTION 'Gender path oracle expected 1 row, got %', v_count;
    END IF;

    SELECT count(*)
    INTO v_count
    FROM ivm_test.l_artist_url AS lau
    JOIN ivm_test.link AS l ON l.id = lau.link
    JOIN ivm_test.link_type AS lt ON lt.id = l.link_type
    JOIN ivm_test.url AS u ON u.id = lau.entity1
    WHERE lau.entity0 = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
      AND lt.gid = '29651736-fa6d-48e4-aadc-a557c6add1cb'
      AND u.url SIMILAR TO
          'http://(de|el|en|es|ko|pl|pt).wikipedia.org/wiki/%';

    IF v_count <> 1 THEN
        RAISE EXCEPTION 'Candidate URL path oracle expected 1 row, got %', v_count;
    END IF;
END;
$$;

-- U-P1: path updates. These affect the isolated rematerialization inputs only.
UPDATE ivm_test.annotation
SET text = 'Updated synthetic annotation'
WHERE id = 9001;

UPDATE ivm_test.gender
SET name = 'FeMaLe'
WHERE id = 9101;

UPDATE ivm_test.url
SET url = 'http://en.wikipedia.org/wiki/IVM_Example_Updated'
WHERE id = 9301;

-- Confirm path rematerialization sees the changed source values.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM artist AS a
        JOIN artist_annotation AS aa ON aa.artist = a.id
        JOIN ivm_test.annotation AS n ON n.id = aa.annotation
        WHERE a.id = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
          AND n.text = 'Updated synthetic annotation'
    ) THEN
        RAISE EXCEPTION 'Updated annotation was not found by path oracle';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM ivm_test.artist_gender AS ag
        JOIN ivm_test.gender AS g ON g.id = ag.gender
        WHERE ag.artist = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
          AND lower(g.name) = 'female'
    ) THEN
        RAISE EXCEPTION 'Updated gender was not found by path oracle';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM ivm_test.l_artist_url AS lau
        JOIN ivm_test.link AS l ON l.id = lau.link
        JOIN ivm_test.link_type AS lt ON lt.id = l.link_type
        JOIN ivm_test.url AS u ON u.id = lau.entity1
        WHERE lau.entity0 = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
          AND lt.gid = '29651736-fa6d-48e4-aadc-a557c6add1cb'
          AND u.url =
              'http://en.wikipedia.org/wiki/IVM_Example_Updated'
    ) THEN
        RAISE EXCEPTION 'Updated candidate URL was not found by path oracle';
    END IF;
END;
$$;

-- D-P1: delete one association from each path and verify the rematerialized
-- path inputs lose the corresponding contribution.
DELETE FROM artist_annotation
WHERE artist = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
  AND annotation = 9002;

DELETE FROM ivm_test.artist_gender
WHERE artist = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
  AND gender = 9101;

DELETE FROM ivm_test.l_artist_url
WHERE id = 9501;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM artist AS a
        JOIN artist_annotation AS aa ON aa.artist = a.id
        JOIN ivm_test.annotation AS n ON n.id = aa.annotation
        WHERE a.id = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
          AND n.id = 9002
    ) THEN
        RAISE EXCEPTION 'Deleted annotation association still appears in path oracle';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM ivm_test.artist_gender AS ag
        JOIN ivm_test.gender AS g ON g.id = ag.gender
        WHERE ag.artist = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
    ) THEN
        RAISE EXCEPTION 'Deleted gender association still appears in path oracle';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM ivm_test.l_artist_url AS lau
        JOIN ivm_test.link AS l ON l.id = lau.link
        JOIN ivm_test.link_type AS lt ON lt.id = l.link_type
        JOIN ivm_test.url AS u ON u.id = lau.entity1
        WHERE lau.entity0 = (SELECT id FROM ivm_test_artist WHERE label = 'alpha')
    ) THEN
        RAISE EXCEPTION 'Deleted URL association still appears in path oracle';
    END IF;
END;
$$;

-- Validate every core trigger event against the independent oracle. The
-- expected state is fully rematerialized from each event's captured old/new
-- row arrays; differences are compared as sets of rule_id/triple objects.
DO $$
DECLARE
    q record;
    old_oracle jsonb;
    new_oracle jsonb;
    expected_plus jsonb;
    expected_minus jsonb;
BEGIN
    FOR q IN
        SELECT *
        FROM maintenance.rdf_ivm_queue
        WHERE event_id > (SELECT event_id FROM ivm_test_start)
          AND relation_name IN ('artist', 'medium', 'track')
        ORDER BY event_id
    LOOP
        old_oracle := ivm_test.oracle_outputs(
            q.relation_name,
            COALESCE(q.components -> 'A_minus', '[]'::jsonb)
        );

        new_oracle := ivm_test.oracle_outputs(
            q.relation_name,
            COALESCE(q.components -> 'A_plus', '[]'::jsonb)
        );

        IF q.components -> 'S2' IS DISTINCT FROM new_oracle THEN
            RAISE EXCEPTION
                'S2 mismatch for event %, relation %: queue %, oracle %',
                q.event_id, q.relation_name, q.components -> 'S2', new_oracle;
        END IF;

        expected_plus :=
            ivm_test.jsonb_set_difference(new_oracle, old_oracle);

        expected_minus :=
            ivm_test.jsonb_set_difference(old_oracle, new_oracle);

        IF q.delta_plus IS DISTINCT FROM expected_plus THEN
            RAISE EXCEPTION
                'delta_plus mismatch for event %, relation %: queue %, oracle %',
                q.event_id, q.relation_name, q.delta_plus, expected_plus;
        END IF;

        IF q.delta_minus IS DISTINCT FROM expected_minus THEN
            RAISE EXCEPTION
                'delta_minus mismatch for event %, relation %: queue %, oracle %',
                q.event_id, q.relation_name, q.delta_minus, expected_minus;
        END IF;

        IF jsonb_array_length(COALESCE(q.components -> 'A_minus', '[]'::jsonb)) = 0
           AND q.operation NOT IN ('INSERT') THEN
            RAISE EXCEPTION
                'Expected old transition rows for event % (% on %)',
                q.event_id, q.operation, q.relation_name;
        END IF;

        IF jsonb_array_length(COALESCE(q.components -> 'A_plus', '[]'::jsonb)) = 0
           AND q.operation NOT IN ('DELETE') THEN
            RAISE EXCEPTION
                'Expected new transition rows for event % (% on %)',
                q.event_id, q.operation, q.relation_name;
        END IF;
    END LOOP;

    IF NOT EXISTS (
        SELECT 1
        FROM maintenance.rdf_ivm_queue
        WHERE event_id > (SELECT event_id FROM ivm_test_start)
          AND relation_name = 'artist'
          AND operation = 'INSERT'
    ) THEN
        RAISE EXCEPTION 'Missing artist INSERT trigger event';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM maintenance.rdf_ivm_queue
        WHERE event_id > (SELECT event_id FROM ivm_test_start)
          AND relation_name = 'artist'
          AND operation = 'UPDATE'
    ) THEN
        RAISE EXCEPTION 'Missing artist UPDATE trigger event';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM maintenance.rdf_ivm_queue
        WHERE event_id > (SELECT event_id FROM ivm_test_start)
          AND relation_name = 'medium'
          AND operation = 'INSERT'
    ) THEN
        RAISE EXCEPTION 'Missing medium INSERT trigger event';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM maintenance.rdf_ivm_queue
        WHERE event_id > (SELECT event_id FROM ivm_test_start)
          AND relation_name = 'track'
          AND operation = 'UPDATE'
    ) THEN
        RAISE EXCEPTION 'Missing track UPDATE trigger event';
    END IF;
END;
$$;

-- D-T1: delete the track before its referenced media.
DELETE FROM track
WHERE id = (SELECT id FROM ivm_test_track);

-- D-M1: now the fixture media are no longer referenced by the fixture track.
DELETE FROM medium
WHERE id IN (SELECT id FROM ivm_test_medium);

-- Remove the fixture's association row before deleting the artists.
DELETE FROM artist_annotation
WHERE artist IN (SELECT id FROM ivm_test_artist);

-- D-A1: delete both fixture artists.
DELETE FROM artist
WHERE id IN (SELECT id FROM ivm_test_artist);

-- Validate the delete events as well, using the same oracle comparison.
DO $$
DECLARE
    q record;
    old_oracle jsonb;
    new_oracle jsonb;
    expected_plus jsonb;
    expected_minus jsonb;
BEGIN
    FOR q IN
        SELECT *
        FROM maintenance.rdf_ivm_queue
        WHERE event_id > (SELECT event_id FROM ivm_test_start)
          AND relation_name IN ('artist', 'medium', 'track')
          AND operation = 'DELETE'
        ORDER BY event_id
    LOOP
        old_oracle := ivm_test.oracle_outputs(
            q.relation_name,
            COALESCE(q.components -> 'A_minus', '[]'::jsonb)
        );

        new_oracle := ivm_test.oracle_outputs(
            q.relation_name,
            COALESCE(q.components -> 'A_plus', '[]'::jsonb)
        );

        expected_plus :=
            ivm_test.jsonb_set_difference(new_oracle, old_oracle);

        expected_minus :=
            ivm_test.jsonb_set_difference(old_oracle, new_oracle);

        IF q.components -> 'S2' IS DISTINCT FROM new_oracle
           OR q.delta_plus IS DISTINCT FROM expected_plus
           OR q.delta_minus IS DISTINCT FROM expected_minus THEN
            RAISE EXCEPTION
                'DELETE oracle mismatch for event %, relation %',
                q.event_id, q.relation_name;
        END IF;
    END LOOP;
END;
$$;

-- Inspect the complete event report before rollback. A successful run reaches
-- this query with all DO-block assertions satisfied.
SELECT
    event_id,
    relation_name,
    operation,
    jsonb_array_length(components -> 'A_minus') AS old_row_count,
    jsonb_array_length(components -> 'A_plus')  AS new_row_count,
    jsonb_array_length(components -> 'S2')      AS post_output_count,
    jsonb_array_length(delta_plus)              AS delta_plus_count,
    jsonb_array_length(delta_minus)             AS delta_minus_count
FROM maintenance.rdf_ivm_queue
WHERE event_id > (SELECT event_id FROM ivm_test_start)
ORDER BY event_id;

-- Keep the test repeatable: fixture rows, queue events, and test-only schema
-- changes made in this transaction are not retained.
ROLLBACK;
```