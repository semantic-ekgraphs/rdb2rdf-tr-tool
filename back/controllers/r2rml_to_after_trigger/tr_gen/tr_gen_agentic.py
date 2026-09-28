from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_4o_mini_openai
from .model import TriplesMapParsing
# from knowledge import object_preserving_definition_knowledge_source
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Aqui está seguindo o documento do artigo: 
# https://docs.google.com/document/d/1FU7M8qcHQhQvPcYbidvnTS28UfEBj5H_lqayQ_pAc-s/edit?tab=t.0

CSV_RULE = """
Prefer a CSV artifact as the primary structured output.
Return a header row and one record per logical item.
Use RFC 4180 escaping. Empty values must remain empty.
Do not wrap CSV in Markdown fences. 
The output must be formatted according to the following specifications:
- Delimiter: Use semicolon (`;`) to separate values;
- Quoting & Escaping: Any field containing commas, line breaks, or quotation marks (such as SQL queries or transformation functions) MUST be wrapped entirely in double quotes (`"`). Internal double quotes must be escaped as `""`.
- Raw Output Only: The output must contain ONLY the raw CSV content. Do NOT wrap the output in Markdown code blocks (e.g., ```csv), and do NOT include introductory text, explanations, or metadata footnotes.
Always put a row for the R2RML mapping of type subjectMap:
- For subjectMap, the mapped rdf predicate is always 'rdf:type' and mapped object is 'None'.
Put rows for all predicateObjectMap.
"""


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




### ==========================================
### TASKS
### ==========================================


# Tasks 1 of the Stage 1
task_metadata_extraction_and_normalization = Task(
   name="Metadata Extraction and Normalization",
   description="""
Analyze the Relational Schema and R2RML mappings.
For each TriplesMap in the R2RML mappings extracts:
- identifier of the TriplesMap;
- table name or SQL query in the logical table (rr:logicalTable);
- all datatype transformation functions (like UPPER, LOWER, REPLACE, SUBSTRING, etc) applied to attributes in the logical table. For example, from the `rr:logicalTable [ rr:sqlQuery \"\"\"SELECT empresa.id, UPPER(empregado.nome) AS nome FROM empresa INNER JOIN empregado ON empresa.empregado = empregado.id\"\"\" ] ;`, the transformation functions to be extracted is 'UPPER(empregado.nome)' — function and parameters. Repete the data extract for row with same triples_map_id;
- selection conditions in an SQL query used to filter rows in a database table, employing operators such as equal to (=), not equal to (!= or <>), greater than/less than (< >), BETWEEN, IN, LIKE, IS NULL, IS NOT NULL, SIMILAR TO and all selection conditions operators known in SQL and relational database literature, as well as possible combinations thereof. Repete the data extract for row with same triples_map_id;
- the class and template of subjecMap. If the class is not explicit included in the subjecMap, use the subjectMap class that has the same template. Example:
   A subjectMap without an explicit class as 
   ```rr:subjectMap lb:sm_person .
      lb:sm_person rr:template "http://example.com/person/id" .
   ```
   use the class foaf:Person from the subjectMap 
   ```rr:subjectMap [rr:class foaf:Person ;
                    rr:template "http://example.com/person/id"] ;
   ```, as they share the same URI rr:template "http://example.com/person/id";
- all predicateObjectMap: the predicate, column and datatype of objectMap. The column and datatype from objectMap as string format: \"column, datatype\";
- the foreign keys names in the Relational Schema, acording SQL join present in logical table.

Important Requirements:
- Analyze each TriplesMap independently.
- Do not parse commented-out TriplesMap. Comments in R2RML start with #.

Inputs: 
- Relational Schema: {{rdb_schema}}
- Transformation Rules Patterns: {{tr_patterns}}
- R2RML mappings: {{r2rml_mapping}}
""",
   expected_output=CSV_RULE + f"""Normalized metadata representation in CSV. Expected columns:
{";".join(list(TriplesMapParsing.model_fields.keys()))}
""",
   output_file=f"temp/metadata_{date_now}.csv",
   agent=agent_transformation_rule_generation
)
# task_metadata_extraction_and_normalization = Task(
#    name="Metadata Extraction and Normalization",
#    description="""
# Analyze the relational schema and R2RML mappings.
# - Extract TriplesMaps, logical tables, subject maps, predicate-object maps, URI templates, join conditions, datatype transformations, selection condition and foreign-key paths.
# - Extract all SQL transformation functions (like as UPPER, LOWER, REPLACE, SUBSTRING, etc) applied in the logical tables. For example, from the `rr:logicalTable [ rr:sqlQuery \"\"\"SELECT empresa.id, UPPER(empregado.nome) AS nome FROM empresa INNER JOIN empregado ON empresa.empregado = empregado.id\"\"\" ] ;`, the transformation functions to be extracted is 'UPPER(empregado.nome)' — function and parameters. Repete the data extract for row with same triples_map.
# - Repete the subject class in the row of the respective of predicate.
# - For source R2MRL of type rr:subjectMap, the mapped rdf predicate is always 'rdf:type' and mapped object source is 'None'.
# Inputs:
# - Relational schema: {{rdb_schema}}
# - Transformation Rules Patterns: {{tr_patterns}}
# - R2RML mappings: {{r2rml_mapping}}
# """,
#    expected_output=CSV_RULE + f"""Normalized metadata representation in CSV. Expected columns:
# {";".join(list(TriplesMapParsing.model_fields.keys()))}
# """,
#    output_file=f"temp/metadata_{date_now}.csv",
#    agent=agent_transformation_rule_generation
# )





# Tasks 2 of the Stage 1
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





# Tasks 3 of the Stage 1
task_transformation_rule_generation_validation = Task(
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
   agent=agent_transformation_rule_generation
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
   agent=agent_transformation_rule_generation
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
   agent=agent_transformation_rule_generation
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
   agent=agent_transformation_rule_generation
)



### ==========================================
### TRANSFORMATION RULES TEAM
### ==========================================
from crewai import Crew


object_preserving_team = Crew(
   agents=[
      agent_transformation_rule_generation
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
      agent_transformation_rule_generation
      # r2rml_to_tr_agent,
   ],
   tasks=[
      task_metadata_extraction_and_normalization
      # task_parsing_and_pivoting_as_csv,
      # task_validation_of_generated_transformation_rules_csv
   ],
   process='sequential',
   # knowledge_sources=[transformation_rules_patterns], # Enable knowledge by adding the sources here
   # embedder=hf_embedder,
)