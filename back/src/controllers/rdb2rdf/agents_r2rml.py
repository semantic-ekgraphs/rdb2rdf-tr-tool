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
date_now                         = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#################################
### TRANSFORMATION RULES TEAM
#################################
r2rml_to_tr_agent = Agent(
   role="Specialist in R2RML mapping analysis and creator of object-preserving transformation rules.",
   goal=(
      "Automatically generate formal object-preserving Transformation Rules (TR) from extract R2RML mappings metadata "
      "according to the Transformation Rules Patterns. "
      "Ensure each generated TR is grounded in the "
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
# Arquivos fonte passados dinamicamente no kickoff como strings/contexto
inputs_context = """
Contexto Técnico de Entrada:
- R2RML mappings: <r2rml>{r2rml_mapping}</r2rml>
- Transformation Rules Patterns: <tr_patterns>{tr_patterns}</tr_patterns>
- Relational Database Schema: <rdb_schema>{rdb_schema}<rdb_schema>
"""

task_parsing_r2rml_to_table = Task(
   description="""
   For each rr:TriplesMap in the <r2rml> extracts:
      - triples map name;
      - logical table;
      - pivot relation;
      - entity preserving;
      - name of transformation rule from each predicateObjectMap and from each subjectMap;
      - trasnformation rule type;
      - relational path
   Context: 
   - the R2RML mappings for the RDF view provided within <r2rml>:
   <r2rml>
      {r2rml_mapping}
   </r2rml>

   - the Transformation Rules Patterns and the examples in <tr_patterns>:
   <tr_patterns>
      {tr_patterns}
   </tr_patterns>
      
   """,
   expected_output="""A CSV document, whose content be a list of the 
      fields and its respective values as defined in the TriplesMapParsing model.
      """,
   output_pydantic=TriplesMapParsingList,
   agent=r2rml_to_tr_agent
)


task_validation_of_generated_transformation_rules = Task(
   description="""For each item in the JSON document, check:
   - opening and closing brackets are present;
   - every relation exists;
   - every attribute exists;
   - every FK path is valid;
   - every subject URI has a pivot;
   - DTRs produce literals;
   - OTRs produce RDF resources;
   - derived entities have stable pseudo-pivots;
   - no R2RML semantics were lost.
   """,
   expected_output="""A JSON document with the main key 'parsings', whose content be a list of the 
      fields and its respective values as defined in the TriplesMapParsing model, If all checks are met.
      Otherwise, the checks that were not met.
      """,
   output_json=TriplesMapParsingList,
   context=[task_parsing_and_pivoting],
   agent=r2rml_to_tr_agent
)

###--------------------------------------
###  csv
###--------------------------------------
task_parsing_and_pivoting_as_csv = Task(
   description="""Consider the R2RML mappings for the RDF view delimited by <r2rml></r2rml>:
   <r2rml>{r2rml_mapping}</r2rml>

   Consider the Relational Database Schema delimited by <rdb_schema></rdb_schema>:
   <rdb_schema>{rdb_schema}<rdb_schema>
   Use the relational schema to identify pivot relations, joins, foreign-key paths.
   
   Your task is to translate the R2RML TriplesMaps into transformation rules.
   Consider the Transformation Rules Patterns delimited by <tr_patterns></tr_patterns>:
   <tr_patterns>{tr_patterns}</tr_patterns>
   
   For each rr:TriplesMap in the R2RML mappings extracts:
   - triples map name;
   - logical table;
   - pivot relation;
   - entity preserving, set True or False; 
   - name of transformation rule from each rr:predicate and from each rr:subjectMap;
   - trasnformation rule type;
   - relational path

   Count the number of rr:TriplesMap in the R2RML mappings.""",
   expected_output = """
Um arquivo puramente no formato CSV (Valores Separados por Vírgula), utilizando a primeira linha como cabeçalho estrito com os nomes das colunas exatos listados abaixo. 

Como a estrutura de dados original possui um relacionamento de 1 para muitos (um 'TriplesMap' pode gerar múltiplas 'Transformation Rules'), você deve desanidá-la (flattening). Isso significa que cada regra de transformação gerada (`TransformationRuleModel`) deve ocupar uma linha própria no CSV, repetindo os dados do `TriplesMap` pai nas primeiras colunas.

O arquivo CSV gerado deve seguir as seguintes diretrizes sem exceções:
1. Delimitador: Utilize vírgulas (`,`) para separar os campos.
2. Codificação de Strings: Se qualquer campo (como SQL ou fórmulas lógicas) contiver vírgulas, quebras de linha ou aspas, envolva o campo obrigatoriamente por aspas duplas (`"`). Aspas duplas internas devem ser escapadas como `""`.
3. Sem texto explicativo: A saída deve conter única e exclusivamente o bloco de dados CSV. Não inclua Markdown (como ```csv), introduções ou notas de rodapé.

O cabeçalho do CSV deve conter exatamente as seguintes 8 colunas nesta ordem:
triples_map_name,logical_table,pivot_relation,entity_preserving,tr_name,tr_type,formula,relational_path

Especificação Semântica de cada Coluna:
- triples_map_name: O identificador/nome do TriplesMap analisado.
- logical_table: A tabela lógica ou a consulta SQL de origem extraída do mapeamento.
- pivot_relation: O nome da relação pivô identificada no banco de dados.
- entity_preserving: Valor booleano (TRUE ou FALSE) indicando se o mapeamento preserva a identidade da entidade.
- tr_name: O nome gerado para a regra de transformação específica seguindo estritamente o padrão 'tr_<pivot_relation>_<sequential_number>' (ex: tr_track_1).
- tr_type: O tipo formal da transformação (estritamente um destes valores: CTR, Local-DTR, Path-DTR, OTR, ou derived-pivot case).
- formula: A fórmula lógica/semântica completa da Transformation Rule (TR) correspondente ao seu tipo.
- relational_path: O caminho relacional ou condição de junção isolada que fica posicionada como o último termo no corpo da regra.

Exemplo do Formato de Saída Esperado:
triples_map_name,logical_table,pivot_relation,entity_preserving,tr_name,tr_type,formula,relational_path
lb:company_mapping,"SELECT id, name, industry FROM company",company,TRUE,tr_company_1,Local-DTR,"org:Company(s) <- company(c), ...",None
lb:company_mapping,"SELECT id, name, industry FROM company",company,TRUE,tr_company_2,Path-DTR,"org:industry(s, v) <- company(c), ...",[fk_company_industry](c, i)
""",
   output_file=f"temp/parsing_r2rml_{date_now}.csv",
   agent=r2rml_to_tr_agent
)




# task_validation_of_generated_transformation_rules_csv = Task(
#    description="""For each item in the CSV document, check:
#    - the number of items is the same of TriplesMap in the R2RML mapping;
#    - every relation exists;
#    - every attribute exists;
#    - every FK path is valid;
#    - every subject URI has a pivot;
#    - DTRs produce literals;
#    - OTRs produce RDF resources;
#    - derived entities have stable pseudo-pivots;
#    - no R2RML semantics were lost.
#    """,
#    expected_output="""A CSV document, whose content be a list of the 
#       fields and its respective values.
#       """,
#    context=[task_parsing_and_pivoting_as_csv],
#    agent=r2rml_to_tr_agent
# )




def validate_blog_content(result: TaskOutput) -> Tuple[bool, Any]:
   """Validate blog content meets requirements."""
   try:
      # Check word count
      word_count = len(result.raw.split())
      if word_count > 200:
         return (False, "Blog content exceeds 200 words")

      # Additional validation logic here
      return (True, result.raw.strip())
   except Exception as e:
      return (False, "Unexpected error during validation")
#################################
### TRIGGERS TEAM
#################################





#################################
### QUESTION & ANSWER TEAM
#################################

tr_patterns_agent = Agent( 
   role="Analyst and expert in Transformation Rules Patterns", 
   goal="Answer questions about Transformation Rules Patterns (TRs) using the provided Transformation Rules Patterns.", 
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

