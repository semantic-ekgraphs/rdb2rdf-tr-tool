# from crewai_tools import DirectoryReadTool, FileReadTool
# from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
# from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from datetime import datetime
from pathlib import Path
from crewai import Agent, Task, TaskOutput
from typing import List, Tuple, Any
from models.task_output import TriplesMapParsing, TriplesMapParsingList
from typing import List, Optional
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from llms import llama3_groq, gpt_oss_20b_groq, gpt_oss_120b_groq
from llms import llama_3b_Ollama
from llms import gpt_4o_mini_openai
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

agent_vania_r2rml_to_tr = Agent(
   role="Principal Knowledge Engineer and Formal Semantic Web Architect",
   goal=(
      "Translate R2RML TriplesMaps into schema-grounded, mathematically rigorous "
      "Transformation Rules (TRs) by reconstructing the underlying semantic structure "
      "of the relational views, identifying precise pivot relations, determining object-preservation "
      "compliance, and isolating structural relational paths as the final term of rule bodies."
   ),
   backstory=(
      "You are a world-class authority on semantic data integration frameworks and the creator of "
      "advanced relational-to-RDF compilation formalisms. You possess an unparalleled mastery of both "
      "relational engine internals (DDL, foreign-key traversals, query graph dependencies) and formal "
      "logic representations of Linked Data (CTR, DTR, OTR patterns). You reject blind syntactic "
      "translation and single-shot code generation; instead, you treat mapping migration as a complex, "
      "multi-step deductive reasoning task. You excel at auditing schemas to isolate identity pivots, "
      "characterizing complex n-ary associations or events as non-object-preserving mappings, designing "
      "elegant relational views to act as pseudo-pivots, and mapping semantic connectivity precisely via "
      "ordered chains of schema-validated foreign keys."
   ),
   verbose=True,
   memory=False,
   llm=gpt_4o_mini_openai,
)


### ==========================================
### TASKS
### ==========================================
task_vania_r2rml_to_tr = Task(
   description="""Consider the relational database schema provided in the first attached file:
- Esquema MusicBrainz Completo: <rdb_schema>{rdb_schema}<rdb_schema>
Use the relational schema to identify pivot relations, joins, foreign-key paths. 

Consider the R2RML mappings for the LinkedBrainz RDF view provided in the second attached file:
- mapR2RML_MusicBrainz_completo: <r2rml>{r2rml_mapping}</r2rml>

Your task is to translate the R2RML TriplesMaps into transformation rules using the formalism proposed in the framework described in the third attached file:
- IVM_abril_21_Current_version

Use the revised Transformation rules Patterns defined in the fourth attached file: 
- TRANSFORMATION RULES PATTERNS: <tr_patterns>{tr_patterns}</tr_patterns>

------------------------------------------------------------
TASK:

For each R2RML TriplesMap, write the TRANSFORMATION RULE  in the framework formalism. 
Use the revised Transformation rules pattern and the examples in fourth attached file: TRANSFORMATION RULES PATTERNS. 

The goal is not merely to syntactically translate R2RML mappings,
but to reconstruct the semantic structure of the RDF view in terms
of pivot entities, relational paths, datatype dependencies,
and object relationships.

------------------------------------------------------------

OUTPUT FORMAT

For each TriplesMap, produce the following sections:

1. SQL Source
- Copy the SQL query from the R2RML logicalTable.

2. Pivot Relation
- Identify the pivot relation.
The pivot relation is the relation whose tuple:
- generates the subject URI;
- determines the identity of the RDF resource;
- corresponds to the domain entity of the mapping.


3. Object-Preserving Classification
- Object-preserving
- Non-object-preserving

A mapping is object-preserving when:
- the subject URI is generated from a tuple of a base pivot relation;
- datatype values are obtained from attributes of the pivot tuple or related tuples;
- object values are URIs of entities generated from other pivot tuples;
- the mapping does not create new RDF resources that do not correspond to base relational tuples.

A mapping is potentially non-object-preserving when:
- it creates a URI or blank node from a join result rather than from a base tuple;
- it creates an auxiliary resource such as a tagging event, release event, temporal interval, or compound relationship entity;
- the generated RDF resource corresponds to an n-ary relationship rather than to a base entity tuple;
- the subject or object URI is constructed from multiple tuples or from a derived SQL projection without a clear pivot tuple. 

Non-object-preserving mappings can often be normalized into
object-preserving mappings through the introduction of
derived associative entities represented as relational views. 

For each non-object-preserving mapping:
- identify the TriplesMap name;
- explain why it violates object preservation;
- if possible, introduce a derived relational view as a pseudo-pivot relation; Then create the transformation rule with the derived relational view as pivot relation.

 Mappings that associate existing pivot entities with external IRIs
(e.g., Wikipedia, DBpedia, Twitter, Discogs)
remain object-preserving if:
- the subject resource is generated from a base pivot tuple;
- no new auxiliary RDF resource is introduced.

The generated URI should explicitly indicate the tuple composition
used to construct the identity of the resource.

4. Transformation Rule Type
- CTR
- Local-DTR
- Path-DTR
- OTR
- Derived-Pivot Rule ( For Non-object-preserving)

A CTR MUST generate only rdf:type assertions.

A DTR MUST generate only datatype properties whose object is a literal.

An OTR MUST generate only object properties whose object is an RDF resource URI.

5. Transformation Rule Generation
- Write the formal rule generated using the revised Transformation rules pattern with some examples in attached file: TRANSFORMATION RULES PATTERNS.
- a Relational path is represented as an ordered list of foreign keys describing how tuples are connected semantically through the relational schema.
The relational path:
must be the final term in the rule body;
use the actual foreign key names from the schema;
must be represented as an ordered list of foreign keys;
must be inferred from the foreign keys used in the SQL joins, not from the textual 
order of joins in SQl.
preserve the traversal order induced by the SQL joins;
defines the semantic connectivity between tuples;
is evaluated according to the path semantics defined in the framework;
may traverse a foreign key in either direction as defined by the framework semantics. When inverse traversal is used, preserve the actual FK name.;
explicitly indicate inverse traversal when necessary;
must be derived from the actual joins used in the R2RML mapping.
never use relation names instead of foreign key names;
Do not simplify the relational semantics of the R2RML mappings.
All intermediate relations participating in joins must be reflected
in the relational path whenever they are required to preserve semantics.
The relational path should not be embedded inside intermediate literals of the rule body, since it represents a global semantic connection between the pivot tuple and the related tuple participating in the transformation rule.
Path Examples:
[fk_artist_credit_name_artist,
fk_artist_credit_name_artist_credit,
fk_release_group_artist_credit]

- TRs Examples

OTR examples:
psi_artist_11:
foaf:made(s,o) ← artist(a), URI_artist(a,s), track(o), URI_track(t,o),
[ artist_credit_name_fk_artist,
artist_credit_name_fk_artist_credit,
release_group_fk_artist_credit] 

psi_artist_12 
 foaf:gender(s,v) ← artist(a), URI_artist(a,s), gender(g), [fk_artist_gender](a,g), nonNull(g.name), RDFLiteral(g.name, “name”, “gender”, v), [fk_artist_gender](a,g)] .

6. RULE NAMING CONVENTION

Use the exact naming pattern:

psi_<pivotRelation>_<NN>

Examples:
psi_artist_01
psi_artist_02
psi_release_03

The numbering must:
- be sequential;
- unique;
- grouped by pivot relation.

7. Use the following global URI predicates, or equivalent predicates if needed.

------------------------------------------------------------
GLOBAL URI PREDICATES — B predicates
------------------------------------------------------------

URI_artist(a,x) :=
hasURI("http://musicbrainz.org/artist/", a.gid, x)

URI_area(ar,x) :=
hasURI("http://musicbrainz.org/area/", ar.gid, x)

URI_label(l,x) :=
hasURI("http://musicbrainz.org/label/", l.gid, x)

URI_medium(m,x) :=
hasURI("http://musicbrainz.org/record/", m.id, x)

URI_place(p,x) :=
hasURI("http://musicbrainz.org/place/", p.gid, x)

URI_recording(r,x) :=
hasURI("http://musicbrainz.org/recording/", r.gid, x)

URI_release(r,x) :=
hasURI("http://musicbrainz.org/release/", r.gid, x)

URI_releaseGroup(rg,x) :=
hasURI("http://musicbrainz.org/release-group/", rg.gid, x)

URI_signalGroup(rg,x) :=
hasURI("http://musicbrainz.org/signal-group/", rg.gid, x)

URI_track(t,x) :=
hasURI("http://musicbrainz.org/track/", t.id, x)

URI_tag(tg,x) :=
hasURI("http://musicbrainz.org/tag/", tg.name, x)

------------------------------------------------------------
8. AUXILIARY BUILT-INS
------------------------------------------------------------

IRIValue(u,y)
DBpediaURI(u,y)
lower(u,v)
like(u,pattern)
similarTo(u,pattern)
replace(u,old,new,v)
DateLiteral(y,m,d,v)
YearMonthLiteral(y,m,v)
YearLiteral(y,v)
RDFLiteral(u,A,R,v)
nonNull(v)

9  FINAL VALIDATION CHECKLIST

Before producing the final answer, verify that:

- every TriplesMap was translated;
- every relation exists in the schema;
- every attribute exists in the schema;
- every FK path corresponds to schema foreign keys;
- every DTR produces literals only;
- every OTR produces URI resources only;
- every CTR generates class instances only;
- every non-object-preserving mapping is explicitly classified;
- no SQL transformation semantics were lost.

========
IMPORTANT INSTRUCTIONS
------------------------------------------------------------

- Do not invent relations or attributes that are not present in the schema.
- use the foreign keys to define relational paths
- Use the actual SQL joins in the R2RML mappings.
- Preserve the semantics of the R2RML mapping..
- When a literal value is produced from a column, use RDFLiteral or an equivalent built-in.
- When a value is transformed, such as LOWER, REPLACE, LIKE, or SIMILAR TO, represent this using auxiliary built-ins.
- Clearly separate clean object-preserving mappings from mappings that require adaptation.
- Prefer concise formal rules, but include enough explanation to justify the pivot relation and object-preserving classification.
""",
   expected_output="""A CSV document whose content be a list of the 
   transformation rules.""",
   output_file=f"temp/mbz_trs_{date_now}.csv",
   agent=agent_vania_r2rml_to_tr
)







task_vania_analise_object_preserving = Task(
   description=""" 
Consider the R2RML mappings for the LinkedBrainz RDF view provided in the:
- mapR2RML_MusicBrainz_completo: <r2rml>{r2rml_mapping}</r2rml>.

Use the revised URI Predicates Definition defined in the: 
- URI Predicates Definition: <uri_predicates_definition>{uri_definition}</uri_predicates_definition>.

The compilation of R2RML mappings into Transformation Rules (TRs) consists of two phases:
Phase 1 – Object-Preservation Analysis
Analyze each R2RML mapping to determine whether it satisfies the entity-preserving property. If so, identify the pivot relation and derive the URI predicate responsible for generating the RDF resource identifiers. Mappings that do not satisfy the entity-preserving property are reported for manual analysis and are not automatically compiled.

Phase 1: Object-preserving R2RML Mappings
An R2RML mapping is object-preserving when each RDF resource representing an instance of a class corresponds to exactly one tuple of a designated relation in the source schema, called the pivot relation, and each pivot tuple generates at most one RDF resource. In other words, the mapping preserves the identity of relational entities in the RDF view.
This interpretation is particularly natural in the context of schema mappings between relational databases and RDF. The purpose of such mappings is to establish semantic correspondences between constructs of the relational schema and constructs of the RDF vocabulary:
entity relations are mapped to RDF classes;
relationships are mapped to object properties;
attributes are mapped to datatype properties.
Consequently, the mapping is expected to preserve the identity of the entities already represented in the relational schema, rather than creating new entities through aggregation, grouping, or other analytical transformations. Each RDF instance therefore represents an existing relational entity, identified by a single pivot tuple, even when some of the values required to construct its URI are obtained from related tuples.
Although the R2RML language allows arbitrary SQL queries in logical tables, including queries involving GROUP BY, DISTINCT, UNION, or aggregation, such mappings generally define derived analytical views rather than semantic correspondences between relational entities and RDF classes. Therefore, while such mappings are valid R2RML specifications, they fall outside the scope of entity-preserving RDB2RDF mappings, which are the focus of the proposed framework.
For this reason, the transformation-rule formalism adopted in this work deliberately assumes object-preserving mappings. This assumption establishes a one-to-one correspondence between pivot tuples and RDF resources, which is the fundamental property on which the incremental maintenance theory and its correctness proofs are built. 
Antes mesmo de gerar as TRs, a LLM (ou um analisador) verifica se o mapeamento R2RML é object preserving:
existe uma pivot relation?
cada recurso RDF corresponde a exatamente uma tupla pivot?
não há agregações, GROUP BY, DISTINCT, UNION ou outras construções que eliminem a correspondência 1:1?
a definição da URI é funcionalmente determinada pela tupla pivot (mesmo que utilize atributos alcançados por caminhos PK/FK)?
The proposed compilation process assumes that the input R2RML specification is entity-preserving. If this assumption is violated, the problem is not merely syntactic but conceptual. In such cases, there is no semantics-preserving compilation into Transformation Rules, since the correspondence between relational entities and RDF resources is no longer one-to-one. Therefore, such mappings should be detected and reported for human analysis rather than automatically transformed by the compiler.

Identificação da Pivot relation

Um mapeamento R2RML é object preserving se pode ser associado com uma pivot relation.  
Nesse caso deve ser identificado qual a “pivot relation” do R2RML,  para depois então gerar a TRs usando a pivot relation. 

A pergunta que se deve fazer é: 
considerando um mapeamento R2RML, Existe uma relação R tal que cada tupla de R gera exatamente um recurso RDF e vice-versa  ?
Se existe a relação R, então pode ser definida uma CTR Ψ that maps tuples of a pivot relation 𝑅 into RDF instances of a class 𝐶. It establishes a semantic correspondence between a pivot tuple 𝑟 and an RDF resource 𝑥, such that each pivot tuple is associated with at most one RDF instance, and distinct pivot tuples generate distinct RDF resources. Thus, the mapping preserves the identity of relational entities in the RDB2RDF view. 

Generating the Instances URI

Note que a URI das instancias geradas por um mapeamento R2RML (object preserving) são definidas com base na pivot relation como definido a seguir :
Uma mapeamento R2RML é object-preserving se existir uma pivot relation R e uma função
f: R→URI 
tal que
cada tupla de R produz exatamente uma URI;
cada URI corresponde exatamente a uma tupla de R. 
Essa função pode usar atributos da própria tupla e também atributos alcançados funcionalmente através de FKs, desde que isso preserve a correspondência 1:1.

OUTPUT FORMAT

------------------------------------------------------------
AUXILIARY BUILT-INS
------------------------------------------------------------

IRIValue(u,y)
DBpediaURI(u,y)
lower(u,v)
like(u,pattern)
similarTo(u,pattern)
replace(u,old,new,v)
DateLiteral(y,m,d,v)
YearMonthLiteral(y,m,v)
YearLiteral(y,v)
RDFLiteral(u,A,R,v)
nonNull(v)


========
IMPORTANT INSTRUCTIONS
------------------------------------------------------------

- Do not invent relations or attributes that are not present in the schema.
- use the foreign keys to define relational paths
- Use the actual SQL joins in the R2RML mappings.
- Preserve the semantics of the R2RML mapping..
- When a literal value is produced from a column, use RDFLiteral or an equivalent built-in.
- When a value is transformed, such as LOWER, REPLACE, LIKE, or SIMILAR TO, represent this using auxiliary built-ins.
- Clearly separate clean object-preserving mappings from mappings that require adaptation.
- Prefer concise formal rules, but include enough explanation to justify the pivot relation and object-preserving classification.
""",
   expected_output="""A CSV document whose content be a list of the 
   URIs.""",
   output_file=f"temp/uris_{date_now}.csv",
   agent=agent_vania_r2rml_to_tr
)




# Adaptado por mim
# Arquivos fonte passados dinamicamente no kickoff como strings/contexto
inputs_context_object_preserving = """
Input Thecnical Context:
- Transformation Rules Patterns: {tr_patterns}
- R2RML mappings: {r2rml_mapping}
- Relational Database Schema: {rdb_schema}
- URI Predicates Definition: {uri_definition}
"""
# - Consider the Relational Database Schema, delimited by <rdb_schema></rdb_schema>,
# to identify pivot relations, joins, foreign-key paths and more:
#    <rdb_schema>{rdb_schema}<rdb_schema>
   
# - Consider the R2RML mappings delimited by <r2rml>:
# <r2rml>{r2rml_mapping}</r2rml>.

# - Consider the revised URI Predicates Definition delimited by <uri_predicates_definition> tag: 
# <uri_predicates_definition>{uri_definition}</uri_predicates_definition>.


list_triples_map_task = Task(
   description="""
      Extract all 'rr:TriplesMap' instances from the R2RML mappings below. 
List only the resource names (e.g., subjects defined with 'a' or 'rdf:type rr:TriplesMap'). 
Exclude any statements lacking these properties.

Input:
<R2RML mappings>
{r2rml_mapping}
</R2RML mappings>
   """,
   expected_output=(
      "A list of all TriplesMap names found"
   ),
   output_file=f"temp/object_preserving_{date_now}.txt",
   agent=agent_vania_r2rml_to_tr
)


object_preserving_analysis_task = Task(
   description="""Analyze each R2RML mapping to determine whether it satisfies the entity-preserving property. 
If so, identify the pivot relation and derive the URI predicate responsible for generating 
the RDF resource identifiers. 


Phase 1: Object-preserving R2RML Mappings
An R2RML mapping is object-preserving when each RDF resource representing an instance of a class 
corresponds to exactly one tuple of a designated relation in the source schema, called the pivot relation, 
and each pivot tuple generates at most one RDF resource. In other words, the mapping preserves 
the identity of relational entities in the RDF view.

This interpretation is particularly natural in the context of schema mappings between 
relational databases and RDF. The purpose of such mappings is to establish semantic correspondences 
between constructs of the relational schema and constructs of the RDF vocabulary:
entity relations are mapped to RDF classes;
relationships are mapped to object properties;
attributes are mapped to datatype properties.

Consequently, the mapping is expected to preserve the identity of the entities already represented 
in the relational schema, rather than creating new entities through aggregation, grouping, or other 
analytical transformations. Each RDF instance therefore represents an existing relational entity, 
identified by a single pivot tuple, even when some of the values required to construct its URI 
are obtained from related tuples.

Although the R2RML language allows arbitrary SQL queries in logical tables, including queries involving 
GROUP BY, DISTINCT, UNION, or aggregation, such mappings generally define derived analytical views rather 
than semantic correspondences between relational entities and RDF classes. Therefore, while such mappings 
are valid R2RML specifications, they fall outside the scope of entity-preserving RDB2RDF mappings, which 
are the focus of the proposed framework.
For this reason, the transformation-rule formalism adopted in this work deliberately assumes 
object-preserving mappings. This assumption establishes a one-to-one correspondence between pivot tuples 
and RDF resources, which is the fundamental property on which the incremental maintenance theory and its 
correctness proofs are built. 

Antes mesmo de gerar as TRs, a LLM (ou um analisador) verifica se o mapeamento R2RML é object preserving:
existe uma pivot relation?
cada recurso RDF corresponde a exatamente uma tupla pivot?
não há agregações, GROUP BY, DISTINCT, UNION ou outras construções que eliminem a correspondência 1:1?
a definição da URI é funcionalmente determinada pela tupla pivot (mesmo que utilize atributos alcançados 
por caminhos PK/FK)?
The proposed compilation process assumes that the input R2RML specification is entity-preserving. 
If this assumption is violated, the problem is not merely syntactic but conceptual. In such cases, there 
is no semantics-preserving compilation into Transformation Rules, since the correspondence between 
relational entities and RDF resources is no longer one-to-one. Therefore, such mappings should be 
detected and reported for human analysis rather than automatically transformed by the compiler.

Identificação da Pivot relation

Um mapeamento R2RML é object preserving se pode ser associado com uma pivot relation.  
Nesse caso deve ser identificado qual a “pivot relation” do R2RML,  para depois então gerar a TRs usando 
a pivot relation. 

A pergunta que se deve fazer é: 
considerando um mapeamento R2RML, Existe uma relação R tal que cada tupla de R gera exatamente um recurso 
RDF e vice-versa?
Se existe a relação R, então pode ser definida uma CTR Ψ that maps tuples of a pivot relation 𝑅 into RDF 
instances of a class 𝐶. It establishes a semantic correspondence between a pivot tuple 𝑟 and an RDF 
resource 𝑥, such that each pivot tuple is associated with at most one RDF instance, and distinct pivot 
tuples generate distinct RDF resources. Thus, the mapping preserves the identity of relational entities 
in the RDB2RDF view. 
""",
   expected_output="""A CSV document whose content be a list of the 
   genereted URIs.   

   IMPORTANT INSTRUCTIONS:
- Do not invent relations or attributes that are not present in the R2RML.
- use the foreign keys to define relational paths
- Use the actual SQL joins in the R2RML mappings.
- Preserve the semantics of the R2RML mapping..
- When a literal value is produced from a column, use RDFLiteral or an equivalent built-in.
- When a value is transformed, such as LOWER, REPLACE, LIKE, or SIMILAR TO, represent this using auxiliary built-ins.
- Clearly separate clean object-preserving mappings from mappings that require adaptation.
- Prefer concise formal rules, but include enough explanation to justify the pivot relation and object-preserving classification.
""",
   output_file=f"temp/uris_{date_now}.csv",
   agent=agent_vania_r2rml_to_tr
)


mapping_analysis_task = Task(
   description=(
      "Analyze provided R2RML mapping in the <R2RML_mappings> to determine if each rr:TriplesMap is 'object-preserving'.\n\n"
      "Criteria for an object-preserving mapping:\n"
      "- A single 'pivot relation' must exist where each tuple generates exactly one RDF resource and vice versa.\n"
      "- The mapping must NOT contain aggregations (e.g., GROUP BY, DISTINCT, UNION) that break the 1:1 correspondence.\n"
      "- The URI generation must be functionally determined by the pivot tuple, even if attributes are retrieved via PK/FK paths.\n\n"
      "Instructions:\n"
      "0. Evaluate all rr:TriplesMap counted in the task output before.\n"
      "1. Evaluate if each rr:TriplesMap satisfies the above criteria.\n"
      "2. If it is NOT object-preserving, report it as a violation for human analysis.\n"
      "3. If it IS object-preserving, identify the pivot relation and the URI predicate responsible for resource identification.\n"
      "4. If it IS object-preserving, generate the URI predicates and hasURI following the URI Predicates Definition taking the included example 1 and example 2.\n\n"
      "5. Consider the Transformation Rules Patterns in the context input.\n\n"
      "Input Thecnical Context:\n"
      "<R2RML_mappings>"
      "{r2rml_mapping}" \
      "</R2RML_mappings>\n"
      "<Transformation Rules Patterns>"
      "{tr_patterns}" \
      "</Transformation Rules Patterns>\n"
      "<Relational Database Schema>"
      "{rdb_schema}" \
      "</Relational Database Schema>\n"
      "<URI Predicates Definition>"
      "{uri_definition}" \
      "</URI Predicates Definition>"
   ),
   expected_output=(
      "A structured analysis report containing for all rr:TriplesMap counted in the task output before:\n"
      "- Boolean status: Is the mapping object-preserving? (Yes/No)\n"
      "- Pivot Relation: [Name of the relation, or 'None']\n"
      "- URI Predicate: [URI term map or predicate used for identification]\n"
      "- hasURI: [function]\n"
      "- Justification: A concise explanation of why it passed or failed the criteria."
   ),
   output_file=f"temp/uris_{date_now}.txt",
   context=[list_triples_map_task],
   agent=agent_vania_r2rml_to_tr
)


extract_entity_preserving = Task(
   description="""Analyze each R2RML mappings below.
   Write the resource names (e.g., subjects defined with 'a' or 'rdf:type rr:TriplesMap') and 
   'Yes' next to the name of 'rr:TriplesMap' if the mapping preserves the tuple entity, or 'No' if it does not.
   Input:
<R2RML mappings>
{r2rml_mapping}
</R2RML mappings>
   
   If no TriplesMap is found, simply write 'Not Found'.
   """,
   expected_output=(
      "A structured analysis report containing for all 'rr:TriplesMap'\n"
      "- Boolean status: Is the mapping object-preserving? (Yes/No)\n"
      "- TriplesMap: name of TriplesMap\n"
      "- Justification: A concise explanation of whether or not it constitutes object preservation, according to the definition of object preservation found in the knowledge sources."
   ),
   output_file=f"temp/entity_preserving_analysis_{date_now}.txt",
   agent=agent_vania_r2rml_to_tr
)







### ==========================================
### TRANSFORMATION RULES TEAM
### ==========================================
object_preserving_team = Crew(
   agents=[
      agent_vania_r2rml_to_tr
   ],
   tasks=[
      # list_triples_map_task,
      extract_entity_preserving,
      # mapping_analysis_task
      # object_preserving_analysis_task,
   ],
   process='sequential',
   # knowledge_sources=[object_preserving_source]
)

transformation_rules_team = Crew(
   agents=[
      agent_vania_r2rml_to_tr
      # r2rml_to_tr_agent,
   ],
   tasks=[
      task_vania_r2rml_to_tr
      # task_parsing_and_pivoting_as_csv,
      # task_validation_of_generated_transformation_rules_csv
   ],
   process='sequential',
   # knowledge_sources=[transformation_rules_patterns], # Enable knowledge by adding the sources here
   # embedder=hf_embedder,
)
