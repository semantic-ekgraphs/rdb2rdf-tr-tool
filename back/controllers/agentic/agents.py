from crewai import Agent, Task
from llms import llama3_groq


#################################
### TRANSFORMATION RULES TEAM
#################################
r2rml_to_tr_agent = Agent(
   role="R2RML-to-TR Generation Agent",
   goal=(
      "Automatically generate formal Transformation Rules (TRs) from R2RML mappings files "
      "according to the framework following the 'transformation_rules_patterns_knowledge' "
      "in our knowledge_source. Ensure each generated rule is grounded in the "
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
   # knowledge_sources=[transformation_rules_patterns_knowledge],  # Agent-specific knowledge
   llm=llama3_groq,
   # tools=[ask_human_validation],
   verbose=True,
   memory=True
)
# ==========================================
# 4. CONFIGURAÇÃO DAS TAREFAS (Com dependência sequencial)
# ==========================================

# Contexto/Inputs que o Agent receberá na execução do Crew
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
   agent=r2rml_to_tr_agent
)



#################################
### TRIGGERS TEAM
#################################


#################################
### ANSWER TEAM
#################################
generic_answer_agent = Agent(
   role="Oráculo que responde perguntas de qualquer tipo",
   goal="Responder perguntas de usuários",
   backstory="""Tem mais de 1000 anos experiência em resposta a perguntas simples e complexas 
   em todas as áreas do conhecimento.""",
   verbose=True,
   llm=llama3_groq
)
answer_task = Task(
   description="""
      Responder a pergunta "{user_question}"
   """,
   expected_output="""
      - Uma frase em italiano
      - Essa frase deve ter 20 palavras
      - Essa frase não deve ter mais que 20 palavras e não deve ter menos que 20 palavras
      - Desconsidere vírgulas e pontos finais das contagem das palavras
   """,
   agent=generic_answer_agent,
)