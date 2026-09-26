from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_4o_mini_openai
# from knowledge import object_preserving_definition_knowledge_source
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Aqui está seguindo o documento do artigo: 
# https://docs.google.com/document/d/1FU7M8qcHQhQvPcYbidvnTS28UfEBj5H_lqayQ_pAc-s/edit?tab=t.0




### ==========================================
### AGENTS
### ==========================================
# Stage 1
agent_transformation_rule_generation = Agent(
   role="Principal Knowledge Engineer and Formal Semantic Web Architect",
   goal=(
      "The objective of this stage is to transform an R2RML specification into a set of "
      "formally defined Transformation Rules (TRs) that conform to the conceptual framework."
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
      "ordered chains of schema-validated foreign keys. "
      "Translate R2RML TriplesMaps into schema-grounded, mathematically rigorous "
      "Transformation Rules (TRs) by reconstructing the underlying semantic structure "
      "of the relational views, identifying precise pivot relations, determining object-preservation "
      "compliance, and isolating structural relational paths as the final term of rule bodies."
   ),
   verbose=True,
   memory=False,
   llm=gpt_4o_mini_openai,
)

# Stage 2
agent_after_trigger_generation = Agent(
   role="Principal Knowledge Engineer and Formal Semantic Web Architect",
   goal=(
      "The objective of this stage is automatically synthesizes PostgreSQL AFTER triggers from the Transformation Rules defined in Stage 1."
   ),
   backstory=(
      "This stage automatically synthesizes PostgreSQL AFTER triggers from the Transformation Rules defined in Stage 1."
   ),
   verbose=True,
   memory=False,
   llm=gpt_4o_mini_openai,
)

# Stage 3
agent_trigger_validation_and_repair = Agent(
   role="Trigger Validation and Repari",
   goal=(
      "The final stage validates the generated triggers through execution and automatically repairs detected errors."
   ),
   backstory=(
      "The final stage validates the generated triggers through execution and automatically repairs detected errors."
   ),
   verbose=True,
   memory=False,
   llm=gpt_4o_mini_openai,
)













### ==========================================
### TASKS
### ==========================================

# Tasks of the Stage 1
# Input: Relational schema, ontology, and R2RML mappings.
# Output: Structured metadata model describing the mappings.
task_metadata_extraction_and_normalization = Task(
   description="""1.1 Metadata Extraction and Normalization
   The first agent analyzes the relational schema, the target ontology, and the R2RML mappings to extract all relevant metadata, including logical tables, TriplesMaps, subject maps, predicate-object maps, URI templates, join conditions, datatype transformations, and foreign-key relationships.

""",
   expected_output="""A CSV document whose content be a list of the transformation rules.""",
   output_file=f"temp/metadata_{date_now}.csv",
   agent=agent_transformation_rule_generation
)






# Tasks of the Stage 1
task_entity_preservation_analysis = Task(
   description="""The second agent verifies whether the R2RML mappings satisfy the assumptions required by the incremental maintenance framework. In particular, it identifies pivot relations, validates URI construction functions, checks whether entity identities are preserved, analyzes relational paths, and detects constructs that violate the entity-preserving property. 
Input: Normalized metadata representation.
Output: Entity-preservation report and recommended corrections.
""",
   expected_output="""A CSV document whose content be a list of the 
   URIs.""",
   output_file=f"temp/entity_preservation__{date_now}.csv",
   agent=agent_transformation_rule_generation
)

# Tasks of the Stage 1
task_transformation_rule_generation and Validation = Task(
   description="""Using the validated metadata, the third agent compiles the R2RML mappings into Transformation Rules (TRs). For each mapping, the agent identifies whether it corresponds to a Class Transformation Rule (CTR), Object Property Transformation Rule (OTR), Local Datatype Transformation Rule (Local DTR), or Path Datatype Transformation Rule (Path DTR), and generates the corresponding formal specification.
   """,
   expected_output="""A CSV document whose content be a list of the 
   URIs.
   Input: Validated metadata and R2RML mappings.
   Output: Validated set of Transformation Rules.
   """,
   output_file=f"temp/transformation_rules_{date_now}.csv",
   agent=agent_transformation_rule_generation
)



#-----------------------------------------------------------------


# Tasks of the 2
task_trigger_planning = Task(
   description="""The second agent verifies whether the R2RML mappings satisfy the assumptions required by the incremental maintenance framework. In particular, it identifies pivot relations, validates URI construction functions, checks whether entity identities are preserved, analyzes relational paths, and detects constructs that violate the entity-preserving property. 
Input: Normalized metadata representation.
Output: Entity-preservation report and recommended corrections.
""",
   expected_output="""A CSV document whose content be a list of the 
   URIs.""",
   output_file=f"temp/trigger_plan_{date_now}.csv",
   agent=agent_after_trigger_generation
)

# Tasks of the Stage 2
task_trigger_synthesis_static_verification = Task(
   description="""The second agent verifies whether the R2RML mappings satisfy the assumptions required by the incremental maintenance framework. In particular, it identifies pivot relations, validates URI construction functions, checks whether entity identities are preserved, analyzes relational paths, and detects constructs that violate the entity-preserving property. 
Input: Normalized metadata representation.
Output: Entity-preservation report and recommended corrections.
""",
   expected_output="""A CSV document whose content be a list of the 
   URIs.""",
   output_file=f"temp/static_verification_{date_now}.csv",
   agent=agent_after_trigger_generation
)


#-----------------------------------------------------------------


# Tasks of the Stage 3
task_test_generation = Task(
   description="""
""",
   expected_output="""""",
   output_file=f"temp/test_scenarios_{date_now}.csv",
   agent=agent_trigger_validation_and_repair
)

task_runtime_validation = Task(
   description="""
""",
   expected_output="""""",
   output_file=f"temp/runtime_validation_{date_now}.csv",
   agent=agent_trigger_validation_and_repair
)

task_automatic_diagnostic_and_repair = Task(
   description="""
""",
   expected_output="""""",
   output_file=f"temp/repair_report_{date_now}.csv",
   agent=agent_trigger_validation_and_repair
)


# ---------------------------------------------------------
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


task_extract_entity_preserving = Task(
   description="""Analyze each R2RML mappings below.
Write the resource names (e.g., subjects defined with 'a' or 'rdf:type rr:TriplesMap') and 
'Yes' next to the name of 'rr:TriplesMap' if the mapping preserves the tuple entity, or 'No' if it does not.
Justify observing the definition of the object-preserving strictly based on provided knowlegde sources.
Input:
<R2RML mappings>
{r2rml_mapping}
</R2RML mappings>
   
Strict Guardrails:
   - If no TriplesMap is found, simply write 'Not Found'.
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
from crewai import Crew


object_preserving_team = Crew(
   agents=[
      agent_vania_r2rml_to_tr
   ],
   tasks=[
      # list_triples_map_task,
      task_extract_entity_preserving,
      # mapping_analysis_task
      # object_preserving_analysis_task,
   ],
   process='sequential',
   # knowledge_sources=[object_preserving_definition_knowledge_source]
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















### ==========================================
### Q&A TRANSFORMATION RULES PARTTERNS TEAM
### ==========================================
from knowledge.sources_of_knowledge import knowledge_source_transformation_rule_patterns_v2

tr_patterns_response_agent = Agent( 
   role="Senior analyst specializing in transformation rule patterns for RDB2RDF views.", 
   goal="Extract and report information strictly based on provided knowlegde sources.", 
   backstory="""You are an expert analyst. Your core principle is total fidelity 
   to knowledge sources material. You only process what is explicitly stated in the provided knowledge sources.
   You never use outside knowledge. You are incapable of hallucination, inference, or assumption.""", 
   verbose=True, 
   memory=False,
   llm=gpt_4o_mini_openai
)


task_answer_tr_patterns_question = Task( 
   description=(
      "1. Answer this specific question: '{user_question}'.\n"
      "2. Strict Guardrails:\n"
      "  - If the the knowledge sources does not contain the answer, you state 'Sorry...I don't know how to answer!'.\n"
      "  - Do not add conversational filler, polite greetings, or supplementary explanations.\n"
      "  - Do not infer transformation rules patterns not explicitly stated in the knowledge sources."
   ), 
   expected_output="A direct, concise sentence answering the question.", 
   agent=tr_patterns_response_agent
)


# person_knowledge_source = StringKnowledgeSource(
#    content="Renato é casado com Eliene. Ele tem os filhos Manuel Neto e Ravi."
# )

team_answer_questions_about_people_using_ks = Crew(
   agents=[tr_patterns_response_agent],
   tasks=[task_answer_tr_patterns_question],
   process='sequential',
   knowledge_sources=[knowledge_source_transformation_rule_patterns_v2]
)