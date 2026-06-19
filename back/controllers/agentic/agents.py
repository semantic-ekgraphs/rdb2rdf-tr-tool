# from crewai_tools import DirectoryReadTool, FileReadTool
# from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
# from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from crewai import Agent, Task
from typing import List
from models.task_output import TriplesMapParsing, TriplesMapParsingList
from llms import llama3_groq

from typing import List, Optional
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool


#################################
### TRANSFORMATION RULES TEAM
#################################
r2rml_to_tr_agent = Agent(
   role="R2RML-to-TR Generation Agent",
   goal=(
      "Automatically generate formal Transformation Rules (TRs) from R2RML mappings files "
      "according to the framework following the 'transformation_rules_patterns' "
      "in our knowledge_sources. Ensure each generated rule is grounded in the "
      "relational schema, preserves mapping semantics, and satisfies entity-preserving "
      "assumptions whenever possible."
   ),
   backstory=(
      "As a world-class Knowledge Engineer with a decade of expertise in Semantic Technologies, "
      "Ontological Engineering, and Relational-to-RDF mapping lifecycles, you treat mapping "
      "transformation not as a simple code-generation task, but as a rigorous deductive reasoning process. "
      "You possess a deep, dual understanding of both relational database internals (including complex "
      "SQL joins and integrity constraints) and formal logic formalisms (CTR, Local-DTR, Path-DTR, OTR, or derived-pivot case). "
      "Your approach is deeply methodical: you systematically isolate the true identity pivot of a resource, "
      "audit entity-preservation conditions, and gracefully design derived views as pseudo-pivots when "
      "structural anomalies or implicit associative entities are found. You believe in mathematical "
      "precision, total traceability from R2RML syntax to formal rule bodies, and the necessity of "
      "collaborative human-in-the-loop validation to resolve complex modeling ambiguities before "
      "committing to a final, compilable semantic architecture."
    ),
   llm=llama3_groq,
   # tools=[ask_human_validation],
   verbose=True,
   # memory=True
)


# ==========================================
# 4. CONFIGURAÇÃO DAS TAREFAS (Com dependência sequencial)
# ==========================================


task_parsing_and_pivoting = Task(
   description="""
      Consider the R2RML mappings for the RDF view provided within <r2rml>:
      <r2rml>
         {r2rml_mapping}
      </r2rml>

      Consider the revised Transformation Rules Patterns and the examples in <tr_patterns>:
      <tr_patterns>
         {tr_patterns}
      </tr_patterns>
      
      For each TriplesMap in the <r2rml> extracts:
      - triples map name;
      - logical table;
      - pivot relation;
      - entity preserving;
      - name of transformation rule from each predicateObjectMap and from each subjectMap;
      - trasnformation rule type;
      - relational path
      """,
   expected_output=(
      """A JSON document with the main key 'parsings', whose content be a list of the 
      fields and its respective values as defined in the TriplesMapParsing model.
      """
   ),
   output_pydantic=TriplesMapParsingList,
   agent=r2rml_to_tr_agent
)


task_validation_of_generated_transformation_rules = Task(
   description="""
   For each item in the JSON document, check:
   - every relation exists;
   - every attribute exists;
   - every FK path is valid;
   - every subject URI has a pivot;
   - DTRs produce literals;
   - OTRs produce RDF resources;
   - derived entities have stable pseudo-pivots;
   - no R2RML semantics were lost.
   """,
   expected_output=(
      """A JSON document with the main key 'parsings', whose content be a list of the 
      fields and its respective values as defined in the TriplesMapParsing model, If all checks are met.
      Otherwise, the checks that were not met.
      """
   ),
   output_json=TriplesMapParsingList,
   context=[task_parsing_and_pivoting],
   agent=r2rml_to_tr_agent
)






#################################
### TRIGGERS TEAM
#################################





#################################
### QUESTION & ANSWER TEAM
#################################

tr_patterns_agent = Agent( 
   role="Analyst and expert in Transformation Rules Patterns", 
   goal="Answer questions about Transformation Rules Patterns (TRs) using the provided Transformation Rules Patterns content.", 
   backstory="""You have decades of experience in Transformation Rules Patterns and 
      know everything about mappings between relational databases and ontology.""", 
   verbose=True, 
   llm=llama3_groq
)

answer_task = Task( 
   description=(
      "Answer the question '{user_question}' using only the provided Transformaion Rules Patterns content.\n"
      "Inputs context:\n"
      "- Transformaion Rules Patterns:\n{tr_patterns_content}"
   ), 
   expected_output=""" 
      - A sentence that should not exceed 100 words. 
   """,
   agent=tr_patterns_agent
)










# tr_patterns_agent = Agent(
#    role="Oráculo que responde perguntas sobre os Transformation Rules Patterns (TRs)",
#    goal="Responder perguntas sobre os Transformation Rules Patterns (TRs) using only its 'knolwedge_sources'",
#    backstory="""You expert in Transformation Rules Patterns (TRs) 
#       that know everything about Transformation Rules Patterns (TRs) included in 'knolwedge_sources' 
#       into its owner Crew.""",
#    verbose=True,
#    llm=llama3_groq
# )
# answer_task = Task(
#    description="""
#       Responder a pergunta "{user_question} using only its 'knolwedge_sources'"
#       f"Inputs context:\n{answer_task_inputs_description}"
#    """,
#    expected_output="""
#       - Uma frase que não deve ter mais que 50 palavras.
#    """,
#    agent=tr_patterns_agent,
# )


# Tarefa 1: Parse, Grounding e Identificação de Pivô
# Consider the relational database schema provided within <rdb_schema>:
#       <rdb_schema>
#          {rdb_schema}
#       </rdb_schema>\n
#       Use the relational database schema to identify pivot relations, joins, foreign-key paths. 

# - logical table;
#       - SQL query;
#       - subject map;
#       - predicate-object maps;
#       - URI templates;
#       - columns;
#       - joins;
#       - transformations such as LOWER, REPLACE, LIKE, etc.
# 'sql_logical_table',
#       'pivot_relation',
#       'entity_preserving', and
#       'generated_trs' fields.
# Step 2 — Schema Grounding — Parse the provided R2RML mapping and 
#          matches all relations, attributes, keys, and foreign keys against the relational schema. 
#          It must reject or flag any rule that uses relations or attributes not present in the schema.
#          Put the class from in rr:class as class in the CTR formula.
#          Using property from rr:predicateObjectMap in the DTR and OTR formula.
#       Step 3 — Pivot Relation Identification — identify the pivot relation for each TriplesMap: 
#          The pivot relation as the relation whose tuple determines the subject URI and 
#          the identity of the RDF resource.
#          Mark join-derived subjects as derived-entity cases.
#       Guardrails:
#       - Do not use the Artist class, anywhere, use mo:MusicalArtist.
#       - Use only classes within the provided R2RML mapping <r2rml>. 
#       - Never invent or infer any other classes out of r2rml mapping.
#       - Do not include or create any field, properties or items that are not in Pydantic models defined into output_json.
#       - Do not add 'true', 'false', or 'δ(r)' in the last element of CTR formula.
#       - Do not include the symbol ψ in the formula.
#       - Generate transformation rules for all rr:predicateObjectMap.
# Aprimorando a análise e a pivotagem de tarefas. Evite usar o símbolo \Psi na fórmula e evite colocar "true" ou "false" no final da fórmula quando não houver uma cláusula WHERE na consulta SQL.

