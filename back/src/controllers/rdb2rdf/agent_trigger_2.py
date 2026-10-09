from crewai import Agent, Task
from typing import List
from llms import llama3_groq

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
from crewai_tools import FileReadTool
# Initialize the tool with a specific file path, so the agent can only read the content of the specified file
file_read_tool = FileReadTool(file_path='.IVM_abril_21__Current_version_ (9).pdf')

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
      "algorithms (such as Algorithms 1 and 2 from the IVM_abril_21 document) with absolute, bug-free "
      "mathematical rigor, translating abstract graph updates into highly-performant relational queries."
   ),
   llm=llama3_groq,
   tools=[file_read_tool, validate_statement_trigger_syntax],
   verbose=True,
   memory=True
)


# =====================================================================
# 4. CONFIGURAÇÃO DAS TAREFAS E DEPENDÊNCIAS SEQUENCIAIS
# =====================================================================

# Contexto unificado que injeta os arquivos e especificações acadêmicas passadas no kickoff
inputs_context = """
[Especificações e Contrato Técnico]
- Documento de Referência Fundamental: {ivm_framework_document} (Contendo Seção 6, Algoritmos 1 e 2, Semântica Formal e Relevância)
- Tabela Alvo: {table}
- Operação: UPDATE (Statement-level)
- Função Mandatória: Compute_Changeset_{table}
"""

# Tarefa 1: Análise Semântica de Relevância (Passo Inicial)
task_semantic_relevance_analysis = Task(
   description=(
      "Step 1: Analyze the target relation R against the rules of the framework. "
      "Apply the 'Relevance definitions' from Section 6 of the provided document. "
      "Identify which Transformation Rules (TRs) are triggered or impacted by an UPDATE statement on R. "
      "Formulate the abstract formal semantics of these rules to isolate exactly which graph structures change.\n"
      f"{inputs_context}"
   ),
   expected_output=(
      "A structured breakdown mapping the relation R to all relevant TRs and their corresponding "
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
      "Generate the complete PostgreSQL PL/pgSQL function named exactly 'Compute_Changeset_{table}'. "
      "It MUST handle statement-level updates using 'REFERENCING OLD TABLE AS ... NEW TABLE AS ...'. "
      "Generate the corresponding 'CREATE TRIGGER ... AFTER UPDATE ON R FOR EACH STATEMENT' block.\n"
      "Finally, run the 'PostgreSQL Statement-Level Trigger Validator' tool on the generated SQL to verify "
      "that all statement-level constraints and syntax contracts are fully met."
   ),
   expected_output=(
      "The finalized compilation artifact: complete, syntactically verified PostgreSQL statement-level trigger "
      "definition and the Compute_Changeset_R function logic."
   ),
   agent=ivm_trigger_compiler_agent,
   context=[task_algorithmic_mapping],  # DEPENDÊNCIA EXPLÍCITA FINAL
   output_json=FinalTriggerPLpgSQLOutput
)


# =====================================================================
# 5. ORQUESTRAÇÃO DO FLUXO (Crew Execution)
# =====================================================================

ivm_trigger_crew_v2 = Crew(
   agents=[ivm_trigger_compiler_agent],
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