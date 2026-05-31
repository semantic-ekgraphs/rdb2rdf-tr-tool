# from crewai_tools import DirectoryReadTool, FileReadTool
# from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
# from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai import Agent, Task
from models.task_output import TriplesMapAnalysis
from llms import llama3_groq


#################################
### TRANSFORMATION RULES TEAM
#################################
r2rml_to_tr_agent = Agent(
   role="R2RML-to-TR Generation Agent",
   goal=(
      "Automatically generate formal Transformation Rules (TRs) from R2RML mappings files "
      "according to the framework following the 'transformation_rules_patterns_knowledge' "
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
   memory=True
)
# ==========================================
# 4. CONFIGURAÇÃO DAS TAREFAS (Com dependência sequencial)
# ==========================================
inputs_description = """
- R2RML Mapping File: {r2rml_mapping}
"""

# Tarefa 1: Parse, Grounding e Identificação de Pivô
task_parsing_and_pivoting = Task(
   description=(
      "Step 1 & 2: Parse the provided R2RML mapping file and match all relations, attributes, "
      "and foreign keys against the Relational Schema. Reject or flag any elements not present in the schema.\n"
      "Step 3: Identify the pivot relation for each TriplesMap (the relation whose tuple determines "
      "the subject URI and RDF resource identity). Mark join-derived subjects as derived-entity cases.\n"
      f"Inputs context:\n{inputs_description}"
   ),
   expected_output=(
      "A preliminary list of each TriplesMap containing: names, extracted logical tables/SQL joins, "
      "and identified pivot relations with technical justifications."
   ),
   output_json=TriplesMapAnalysis,
   agent=r2rml_to_tr_agent
)



#################################
### TRIGGERS TEAM
#################################













#################################
### QUESTION & ANSWER TEAM
#################################
answer_task_inputs_description = """
- Transformaion Rules Patterns File: {tr_patterns_file}
"""
tr_patterns_agent = Agent( 
   role="Analyst and expert in Transformation Rules Patterns", 
   goal="Answer questions about transformation rule patterns (TRs) using the provided transformation rule patterns file.", 
   backstory="""You have decades of experience in transformation rule patterns and 
      know everything about mappings between relational databases and ontology.""", 
   verbose=True, 
   llm=llama3_groq
)
answer_task = Task( 
   description=""" 
   Answer the question "{user_question} using only the provided Transformaion Rules Patterns File" 
   f"Inputs context:\n{answer_task_inputs_description}" 
   """, 
   expected_output=""" 
   - A sentence that should not exceed 50 words. 
   """,
   agent=tr_patterns_agent,
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