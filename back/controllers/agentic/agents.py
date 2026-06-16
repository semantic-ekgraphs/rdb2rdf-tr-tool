# from crewai_tools import DirectoryReadTool, FileReadTool
# from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
# from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai import Agent, Task
from models.task_output import TriplesMapParsingList
from llms import llama3_groq


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
      "SQL joins and integrity constraints) and formal logic formalisms (CTR, DTR, Path-DTR, and OTR patterns). "
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

# Tarefa 1: Parse, Grounding e Identificação de Pivô
task_parsing_and_pivoting = Task(
   description="""
      Consider the relational database schema provided within <rdb_schema>:
      <rdb_schema>
         {rdb_schema}
      </rdb_schema>\n
      Use the relational database schema to identify pivot relations, joins, foreign-key paths. 

      Consider the R2RML mappings for the RDF view provided within <r2rml>:
      <r2rml>
         {r2rml_mapping}
      </r2rml>

      Use the revised Transformation Rules Patterns and the examples in <trp>:\n 
      <trp>
         {tr_patterns}
      </trp>
Step 1 & 2: Parse the provided R2RML mapping and match all relations, attributes,
and foreign keys against the Relational Schema. Reject or flag any elements not present in the schema.
Step 3: Identify the pivot relation for each TriplesMap (the relation whose tuple determines
the subject URI and RDF resource identity). Mark join-derived subjects as derived-entity cases.
      """,
   expected_output=(
      """A JSON with a list of 'triples_map_name',
      'sql_logical_table',
      'pivot_relation',
      'entity_preserving', and
      'generated_trs' fields. 
      -Do not include or create any field, properties or items that are not in Pydantic models defined into output_json.
      -If in the logical table or extracted SQL query does not have a WHERE clause, do not add true, false, or δ(r) to the end of the formula.
      -Do not include the symbol ψ in the formula.
      """
   ),
   output_json=TriplesMapParsingList,
   # output_pydantic=TransformationRulesList,
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



