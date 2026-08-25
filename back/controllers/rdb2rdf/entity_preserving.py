from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_4o_mini_openai
from .rdb2rdf_agentic import agent_vania_r2rml_to_tr
# from .rdb2rdf_knowledge import entity_preserving_definition_knowledge_source
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



### ==========================================
### TASKS
### ==========================================
task_vania_analizes_entity_preserving = Task(
   description="""
      You are given the following inputs:
         - the relational database schema: {rdb_schema}
         - the R2RML mappings defining the LinkedBrainz RDF view: {r2rml_mapping}
      ---
      Task
      Analyze every R2RML Triples Map independently.
      For each mapping, determine whether it satisfies the entity-preserving property.
      Only mappings satisfying this property are considered eligible for automatic compilation into Transformation Rules.
      Mappings that are not entity-preserving must be reported for manual analysis.
      ---
      Analysis Procedure
      For each Triples Map, perform the following steps.
      Step 1 — Verify the Entity-Preserving Property
      Determine whether the mapping satisfies all of the following conditions.
      1. A pivot relation exists.
      2. Every tuple of the pivot relation generates exactly one RDF resource.
      3. Every RDF resource corresponds to exactly one pivot tuple.
      4. The logical table does not contain analytical constructs that destroy the one-to-one correspondence, such as
         - GROUP BY
         - DISTINCT
         - UNION
         - aggregation
         - other derived analytical transformations.
      5. The subject URI is functionally determined by the pivot tuple.
      If any condition is violated, classify the mapping as Manual Analysis Required and explain why.
      Step 2 — Identify the Pivot Relation
      If the mapping is entity-preserving, identify the pivot relation and explain why this relation represents the identity of the RDF resource.
      Step 3 — Derive the URI Constructor
         URI_R(r,s) ≡ hasURI(template, <e1,...,en>, s)
      where
      -  template denotes the URI template extracted from the R2RML Subject Map, 
      - <e1,...,en> is the ordered sequence of pivot-rooted attribute expressions corresponding to the placeholders of the R2RML URI template;, and 
      - s is the URI associated with the pivot tuple r.
      Pivot-rooted attribute expressions have one of the following forms:
      ei ::= r.A
      ei ::= [FK(r,t)/t.A]
      where r.A denotes an attribute of the pivot tuple, and [FK(r,t)/t.A] denotes the value of attribute A obtained after following the foreign key FK from the pivot tuple r to tuple t.
      For every URI component,
      identify whether it is
      - a pivot attribute [r.A]
      or
      - an FK-path attribute expression [ [FK(r,t)/t.A].]
      The resulting URI constructor must preserve exactly the same placeholder order defined by the original R2RML template.
      Step 4 — Define the hasURI Predicate
      Derive the corresponding predicate
      hasURI(template, <e1,...,en>, s) iff
         s = instantiate(template, encode(eval(e1)), ..., encode(eval(en))).
      by specifying
         - the URI template;
         - every FK navigation required to obtain placeholder values;
         - the concatenation order used to construct the final URI.
      The instantiate function replaces each placeholder of the template with the encoded value obtained by evaluating the corresponding expression while preserving all constant fragments of the template.
      Evaluation rules:
      eval(r.A) = r[A]
      eval([FK(r,t)/t.A]) = t[A], provided that FK(r,t) holds.
      ---
      Important Requirements
      - Analyze each Triples Map independently.
      - Never infer URI templates that are not explicitly defined in the R2RML mapping.
      - Preserve the original placeholder order of the R2RML template.
      - Every URI component must be rooted at the pivot tuple.
      - Use FK-path attribute expressions whenever the value is obtained through a foreign-key navigation.
      - Be conservative. If the existence of a unique pivot relation cannot be established, classify the mapping as Manual Analysis Required.
      - Do not generate Transformation Rules in this phase. The objective is exclusively to determine whether the mapping is entity-preserving and, if so, identify the pivot relation and derive the URI constructor.
""",
   expected_output="""Output Format:
For each Triples Map, produce the following report.
Triples Map:

Entity-Preserving:  YES / NO

Justification:

Pivot Relation:

R2RML Subject Template:

URI Constructor:

URI_R(r,s)

URI Components:

hasURI Definition:

Example:  Uri constructor for pivot table artist_tag 

R2RML subject map:
rr:template "http://musicbrainz.org/artist/\{gid\}#tag/\{name\}"
Pivot relation: artist_tag
 URI predicate:
URI_artist_tag(r,s) ≡
hasURI(
  "http://musicbrainz.org/artist/\{gid\}#tag/\{name\}",
  <
    [artist_tag_fk_artist(r,a)/a.gid],
    [artist_tag_fk_tag(r,t)/t.name]
  >,
  s
)
Semantics:
s = instantiate(
      "http://musicbrainz.org/artist/\{gid\}#tag/\{name\}",
      encode(eval([artist_tag_fk_artist(r,a)/a.gid])),
      encode(eval([artist_tag_fk_tag(r,t)/t.name]))
	)
 
Assuming:
  a.gid = '8f3d4d52'
  t.name = 'Jazz'
the resulting URI is:
  http://musicbrainz.org/artist/8f3d4d52#tag/Jazz
This example illustrates that hasURI reproduces exactly the URI specified by the original R2RML template, while the values inserted into the placeholders are obtained through the pivot-rooted attribute expressions.
""",
   output_file=f"temp/entity_preserving_{date_now}.txt",
   agent=agent_vania_r2rml_to_tr
)


### ==========================================
### TRANSFORMATION RULES TEAM
### ==========================================
entity_preserving_team = Crew(
   agents  = [agent_vania_r2rml_to_tr],
   tasks   = [task_vania_analizes_entity_preserving],
   process = 'sequential',
   # knowledge_sources=[entity_preserving_definition_knowledge_source]
)