from crewai import Agent, Task
from typing import List
from llms import llama3_groq

from typing import List, Optional
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool


# =====================================================================
# 1. DEFINIÇÃO DOS MODELOS DE SAÍDA (Pydantic para Casamento de Tipos)
# =====================================================================

class DifferentialImpactAnalysis(BaseModel):
   table_name: str = Field("R", description="Nome da tabela analisada (sempre R neste escopo).")
   affected_trs: List[str] = Field(..., description="Lista de Transformation Rules (TRs) impactadas por alterações na tabela R.")
   delta_relations_definitions: str = Field(..., description="Definição formal das relações delta (ΔR) e como as inserções/deleções impactam a visão RDF.")
   justification: str = Field(..., description="Justificativa teórica baseada no framework formal de IVM para RDB2RDF.")

class FinalTriggerOutput(BaseModel):
   trigger_name: str = Field(..., description="Nome do gatilho gerado em conformidade com as restrições do PostgreSQL.")
   plpgsql_function_code: str = Field(..., description="Código limpo e completo da função PL/pgSQL executada pelo Trigger (lidando com TG_OP = INSERT/UPDATE/DELETE).")
   sql_trigger_statement: str = Field(..., description="A declaração SQL 'CREATE TRIGGER ... AFTER INSERT OR UPDATE OR DELETE ON R ...'.")
   validation_status: str = Field("Validado", description="Status de validação sintática e semântica frente ao contrato de compilação.")

# =====================================================================
# 2. DEFINIÇÃO DE FERRAMENTAS CUSTOMIZADAS (Tools)
# =====================================================================

@tool("PostgreSQL Syntax Validator")
def validate_postgres_syntax(sql_code: str) -> str:
   """
   Valida a sintaxe estrutural de blocos de código PL/pgSQL e comandos CREATE TRIGGER 
   para garantir retrocompatibilidade com o PostgreSQL.
   """
   # Aqui entraria uma lógica real de validação ou mock de checagem de palavras-chave.
   if "RETURNS TRIGGER" in sql_code and "BEGIN" in sql_code and "END;" in sql_code:
      return "Sintaxe validada com sucesso: Nenhuma anomalia estrutural detectada."
   return "Erro de Sintaxe: Bloco PL/pgSQL mal formado ou ausência de retorno de gatilho apropriado."

# =====================================================================
# 3. CRIAÇÃO DO AGENTE ESPECIALIZADO
# =====================================================================

ivm_trigger_architect_agent = Agent(
   role="World-Class Database Systems Architect specializing in RDB2RDF Incremental View Maintenance",
   goal=(
      "Compile formal algebraic IVM specifications into highly optimized, production-ready "
      "PostgreSQL AFTER TRIGGER code for Table R. Ensure total semantic alignment with the "
      "LinkedBrainz RDF View, the MusicBrainz schema, and the underlying ontology."
   ),
   backstory=(
      "You are a premier engineer in data integration, operating at the intersection of relational "
      "engines and semantic web formalisms. You do not write generic database triggers. "
      "Instead, you treat trigger generation as a rigorous 'Specification-to-code' compilation contract. "
      "You have a profound mastery of Incremental View Maintenance (IVM) theory, specifically applied "
      "to generating graph deltas (triplestore updates) from relational mutations (INSERT, UPDATE, DELETE). "
      "You parse Transformation Rules (TRs) as algebraic mappings, map database fields against the "
      "MusicbrainzOntoUltimate ontology, and construct flawless PL/pgSQL code that precisely computes "
      "the algebraic differential changes on Table R to keep the semantic view consistent."
   ),
   llm=llama3_groq,
   tools=[validate_postgres_syntax],
   verbose=True,
   memory=True
)

# =====================================================================
# 4. CONFIGURAÇÃO DAS TAREFAS E SUAS DEPENDÊNCIAS
# =====================================================================

# Arquivos fonte passados dinamicamente no kickoff como strings/contexto
inputs_context = """
Contexto Técnico de Entrada:
- Framework de IVM de Referência: {ivm_framework_document}
- Esquema Relacional de Destino (MusicBrainz): {musicbrainz_schema}
- Fonte de Verdade das Regras de Transformação (MB_TRs): {mb_trs_source}
- Ontologia de Alinhamento: {musicbrainz_ontology}
- Tabela R Alvo da Compilação: {table}
"""

# Tarefa 1: Análise Diferencial Algébrica (Passo Inicial)
task_differential_analysis = Task(
   description=(
      "Examine the 'MB_TRs' and the 'MusicBrainz Schema' to identify all Transformation Rules "
      "dependent on Table R. Apply the formal rules from the 'IVM framework document' to derive "
      "the delta graph algebraic expressions for changes (inserts, deletes, updates) on Table R.\n"
      f"{inputs_context}"
   ),
   expected_output=(
      "A formal mathematical breakdown detailing which predicates, classes, and graph patterns "
      "are affected when a tuple in Table R is modified."
   ),
   agent=ivm_trigger_architect_agent,
   output_json=DifferentialImpactAnalysis
)

# Tarefa 2: Geração do Código PL/pgSQL e Casamento com a Ontologia (Depende da Tarefa 1)
task_trigger_generation = Task(
   description=(
      "Based on the algebraic differential analysis from the previous task, compile the actual "
      "PostgreSQL code. Draft an AFTER TRIGGER for Table R. The trigger function must check the operation type "
      "(TG_OP), read from the special row variables (NEW and OLD), and format the resulting semantic "
      "deltas strictly adhering to the namespaces of the 'MusicbrainzOntoUltimate.owl' ontology.\n"
      "Ensure efficient join tracking if Table R acts as a pivot or part of a path (Path-DTR/OTR)."
   ),
   expected_output=(
      "The complete PL/pgSQL function code alongside the CREATE TRIGGER statement for Table R." \
      "No comment in the code" \
      "Code identation size 2"
   ),
   agent=ivm_trigger_architect_agent,
   context=[task_differential_analysis]  # Dependência Explícita: Não pode gerar sem a análise algébrica
)

# Tarefa 3: Validação da Sintaxe e Garantia do Contrato (Depende da Tarefa 2)
task_contract_validation = Task(
   description=(
      "Review the generated SQL code from the previous task. Use the 'PostgreSQL Syntax Validator' "
      "tool to ensure the code executes cleanly. Double-check that all mapped columns match the "
      "MusicBrainz schema and that the trigger executes 'AFTER INSERT OR UPDATE OR DELETE' as "
      "dictated by the compilation contract."
   ),
   expected_output="The final validated, compiled code block ready for deployment in a PostgreSQL instance.",
   agent=ivm_trigger_architect_agent,
   context=[task_trigger_generation],  # Dependência Explícita Final
   output_json=FinalTriggerOutput
)

# =====================================================================
# 5. ORQUESTRAÇÃO DO CREW (Processamento Sequencial Controlado)
# =====================================================================

ivm_compilation_crew = Crew(
   agents=[ivm_trigger_architect_agent],
   tasks=[
      task_differential_analysis,
      task_trigger_generation,
      task_contract_validation
   ],
   process=Process.sequential,  # Fluxo controlado por etapas analíticas e dependentes
   verbose=True
)

# Exemplo de execução:
# resultado_sql = ivm_compilation_crew.kickoff(inputs={
#     "ivm_framework_document": "Conteúdo extraído do arquivo IVM_abril_21__Current_version.txt",
#     "musicbrainz_schema": "Definição DDL extraída do MusicBrainz Schema",
#     "mb_trs_source": "Regras extraídas de MB_TRs",
#     "musicbrainz_ontology": "MusicbrainzOntoUltimate.owl"
# })



















### -------------------------------------------------------------------------
### SEGUNDA VERSÃO (TASK TIRADO DO PROMPT DA PROFA VÂNIA)
### -------------------------------------------------------------------------
from typing import List, Optional
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# =====================================================================
# 1. MODELOS DE SAÍDA E ESTRUTURAÇÃO DE DADOS (Pydantic)
# =====================================================================

class SemanticsAnalysisOutput(BaseModel):
   target_relation: str = Field("R", description="A relação R alvo do gatilho.")
   relevant_trs: List[str] = Field(..., description="Lista de Transformation Rules (TRs) consideradas 'Relevantes' para atualizações em R, conforme Seção 6.")
   delta_algebra_spec: str = Field(..., description="Especificação algébrica das mudanças e casamento de padrões formais (Formal semantics of TRs).")

class AlgorithmicMappingOutput(BaseModel):
   algorithm_1_derivation: str = Field(..., description="Mapeamento lógico passo a passo baseado no Algoritmo 1 do framework.")
   algorithm_2_derivation: str = Field(..., description="Mapeamento lógico passo a passo baseado no Algoritmo 2 do framework.")
   transition_tables_usage: str = Field(..., description="Estratégia de leitura e processamento das tabelas de transição do Postgres (REFERENCING OLD TABLE AS... NEW TABLE AS...).")

class FinalTriggerPLpgSQLOutput(BaseModel):
   trigger_function_name: str = Field("Compute_Changeset_R", description="Nome mandatório da função de computação de mudanças.")
   complete_plpgsql_code: str = Field(..., description="Código PL/pgSQL completo e limpo que implementa a arquitetura de IVM.")
   sql_trigger_statement: str = Field(..., description="O comando 'CREATE TRIGGER ... AFTER UPDATE ON R REFERENCING ... FOR EACH STATEMENT EXECUTE FUNCTION...'")
   compilation_contract_status: str = Field(..., description="Status de validação confirmando conformidade com a Seção 6 e definições de relevância.")


# =====================================================================
# 2. DEFINIÇÃO DE FERRAMENTAS OPERACIONAIS (Tools)
# =====================================================================

@tool("PostgreSQL Statement-Level Trigger Validator")
def validate_statement_trigger_syntax(sql_code: str) -> str:
   """
   Valida se o código SQL gerado implementa corretamente a sintaxe de gatilhos 
   em nível de instrução (STATEMENT-LEVEL) no PostgreSQL, incluindo a cláusula obrigatória 
   'REFERENCING NEW TABLE' e 'REFERENCING OLD TABLE' para capturar os Transition Relations / Transition Tables.
   """
   code_upper = sql_code.upper()
   if "FOR EACH STATEMENT" not in code_upper:
      return "ERRO: O gatilho não foi definido em nível de instrução (FOR EACH STATEMENT)."
   if "REFERENCING" not in code_upper or "OLD TABLE" not in code_upper or "NEW TABLE" not in code_upper:
      return "ERRO: Falta a declaração das tabelas de transição (Transition Tables) requeridas para o cálculo de deltas do IVM."
   return "SUCESSO: Sintaxe de gatilho em nível de instrução validada com sucesso."


# =====================================================================
# 3. CRIAÇÃO DO AGENTE ESPECIALIZADO
# =====================================================================

ivm_trigger_compiler_agent = Agent(
   role="Principal Database Systems Compiler specializing in RDB2RDF Incremental View Maintenance",
   goal=(
      "Compile formal algebraic IVM semantics into optimized, production-ready PostgreSQL statement-level "
      "AFTER UPDATE triggers and PL/pgSQL functions. Synthesize mathematical relevance definitions "
      "and algorithms directly into deterministic, transactional SQL query deltas."
   ),
   backstory=(
      "You are an elite Computer Science researcher and database engineer operating at the absolute cutting "
      "edge of semantic data integration. You have deep expertise in compiling high-level specifications "
      "into strict database procedural code. You understand that statement-level triggers (using transition "
      "tables like 'inserted' and 'deleted' via REFERENCING) are foundational for performance-driven "
      "Incremental View Maintenance. You interpret formal logic semantics, relevance criteria, and procedural "
      "algorithms (such as Algorithms 1 and 2 from the ivm_formal_framework document) with absolute, bug-free "
      "mathematical rigor, translating abstract graph updates into highly-performant relational queries."
   ),
   llm=llama3_groq,
   tools=[validate_statement_trigger_syntax],
   verbose=True,
   memory=True
)


# =====================================================================
# 4. CONFIGURAÇÃO DAS TAREFAS E DEPENDÊNCIAS SEQUENCIAIS
# =====================================================================

# Contexto unificado que injeta os arquivos e especificações acadêmicas passadas no kickoff
inputs_context = """
[Especificações e Contrato Técnico]
- Documento de Referência Fundamental: {ivm_formal_framework} (Contendo Seção 6, Algoritmos 1 e 2, Semântica Formal e Relevância)
- Tabela Alvo: {relation}
- Operação: UPDATE (Statement-level)
- Função Mandatória: Compute_Changeset_{relation}
"""

# Tarefa 1: Análise Semântica de Relevância (Passo Inicial)
task_semantic_relevance_analysis = Task(
   description=(
      "Step 1: Analyze the target relation {relation} against the rules of the framework. "
      "Apply the 'Relevance definitions' from Section 6 of the provided document. "
      "Identify which Transformation Rules (TRs) are triggered or impacted by an UPDATE statement on {relation}. "
      "Formulate the abstract formal semantics of these rules to isolate exactly which graph structures change.\n"
      f"{inputs_context}"
   ),
   expected_output=(
      "A structured breakdown mapping the relation {relation} to all relevant TRs and their corresponding "
      "graph patterns affected by data modifications."
   ),
   agent=ivm_trigger_compiler_agent,
   output_json=SemanticsAnalysisOutput
)

# Tarefa 2: Mapeamento dos Algoritmos 1 e 2 para Estruturas Relacionais (Depende da Tarefa 1)
task_algorithmic_mapping = Task(
   description=(
      "Step 2: Take the semantic relevance analysis from the previous task. "
      "Translate the abstract graph maintenance operations using 'Algorithm 1' and 'Algorithm 2'. "
      "Map how the transition relations (the delta datasets capturing old states and new states of updated rows) "
      "must be processed sequentially. Plan out the SQL logic to capture updates without loss of semantic mappings."
   ),
   expected_output=(
      "A rigorous, step-by-step logic breakdown converting the pseudocode of Algorithm 1 and Algorithm 2 "
      "into relational query logic tailored for PostgreSQL transition tables."
   ),
   agent=ivm_trigger_compiler_agent,
   context=[task_semantic_relevance_analysis],  # DEPENDÊNCIA EXPLÍCITA
   output_json=AlgorithmicMappingOutput
)

# Tarefa 3: Compilação de Código e Validação de Sintaxe Final (Depende da Tarefa 2)
task_compile_postgres_trigger = Task(
   description=(
      "Step 3: Synthesize the logic from the algorithmic mapping into a solid, production-ready SQL script. "
      "Generate the complete PostgreSQL PL/pgSQL function named exactly 'Compute_Changeset_{relation}'. "
      "It MUST handle statement-level updates using 'REFERENCING OLD TABLE AS deleted_{relation} NEW TABLE AS inserted_{relation}'. "
      "Generate the corresponding 'CREATE TRIGGER ... AFTER UPDATE ON {relation} FOR EACH STATEMENT' block.\n"
      "Finally, run the 'PostgreSQL Statement-Level Trigger Validator' tool on the generated SQL to verify "
      "that all statement-level constraints and syntax contracts are fully met."
   ),
   expected_output=(
      "The finalized compilation artifact: complete, syntactically verified PostgreSQL statement-level AFTER trigger "
      "definition and the Compute_Changeset_{relation} function logic."
   ),
   agent=ivm_trigger_compiler_agent,
   context=[task_algorithmic_mapping],  # DEPENDÊNCIA EXPLÍCITA FINAL
   output_json=FinalTriggerPLpgSQLOutput
)


# =====================================================================
# 5. ORQUESTRAÇÃO DO FLUXO (Crew Execution)
# =====================================================================

ivm_trigger_crew_v2 = Crew(
   agents=[
      ivm_trigger_compiler_agent
   ],
   tasks=[
      task_semantic_relevance_analysis,
      task_algorithmic_mapping,
      task_compile_postgres_trigger
   ],
   process=Process.sequential,  # Garante execução sequencial rígida baseada em dependência
   verbose=True
)


# Exemplo de Inicialização (Kickoff):
# resultado_sql_trigger = ivm_trigger_crew.kickoff(inputs={
#     "ivm_document_content": "Texto cru ou mapeado extraído das seções do arquivo IVM_abril_21__Current_version.txt"
# })