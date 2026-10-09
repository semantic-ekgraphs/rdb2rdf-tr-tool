import os
from crewai import Crew, Agent, Task, LLM
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from llms import llama3_groq, gpt_oss_20b_groq, gpt_oss_120b_groq
from dotenv import load_dotenv
load_dotenv()
_GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
# _OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
# Configure sua chave de API
# os.environ["OPENAI_API_KEY"] = _OPENAI_API_KEY

# 1. Defina seus arquivos de conhecimento
# Exemplo: um relatório em PDF e um arquivo de texto de políticas
pdf_source = PDFKnowledgeSource(file_paths=["Infrastructure for the Maintenance Queue.pdf"])
txt_source = TextFileKnowledgeSource(file_paths=["renato-data.txt"])

# 2. Crie seus agentes com as instruções
agente_pesquisador = Agent(
   role="Analista de Dados",
   goal="Responder perguntas com base nos documentos fornecidos",
   backstory="Você é um analista especialista em ler documentos longos e extrair respostas precisas.",
   verbose=True,
   allow_delegation=False,
   llm=llama3_groq
)

tarefa_analise = Task(
   description="Leia os documentos de conhecimento e responda: {pergunta}?",
   expected_output="Um resumo detalhado da resposta",
   agent=agente_pesquisador
)

# 3. Monte a sua Crew passando os arquivos de conhecimento
file_crew = Crew(
   agents=[agente_pesquisador],
   tasks=[tarefa_analise],
   knowledge_sources=[pdf_source, txt_source], # <-- ChromaDB é criado e alimentado aqui
   verbose=True
)

