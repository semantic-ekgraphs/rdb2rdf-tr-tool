import os
from pathlib import Path
from crewai import Crew, Process
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from .agents import tr_patterns_agent, r2rml_to_tr_agent
from .agents import answer_task, task_parsing_and_pivoting, task_validation_of_generated_transformation_rules
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY =         os.getenv("GROQ_API_KEY")
# HUNGGINGFACE_API_KEY = os.getenv("HF_API_KEY")

### NÃO ESTÁ FUNCIONANDO O KNOWLEDGE_SOURCES
# hf_embedder = {
#    "provider": "huggingface",
#    "config": {
#       "api_key": HUNGGINGFACE_API_KEY,
#       "model": "sentence-transformers/all-MiniLM-L6-v2",
#       "api_url": "https://api-inference.huggingface.co/models/sentence-transformers/all-mpnet-base-v2",
#       "headers": {"Authorization": f"Bearer {HUNGGINGFACE_API_KEY}"}
#    }
# }

### ==========================================
### KNOWLEDGE BASE
### ==========================================
# path_knowledge_tr_patterns = Path(__file__).parent / "../../knowledge/tr_patterns.txt"
# with open(path_knowledge_tr_patterns, "r", encoding="utf-8") as file:
#    tr_patterns_content = file.read()
#    transformation_rules_patterns = StringKnowledgeSource(content=tr_patterns_content)



### ==========================================
### TRANSFORMATION RULES TEAM
### ==========================================
transformation_rules_team = Crew(
   agents=[
      r2rml_to_tr_agent
   ],
   tasks=[
      task_parsing_and_pivoting,
      task_validation_of_generated_transformation_rules
   ],
   process='sequential',
   # knowledge_sources=[transformation_rules_patterns], # Enable knowledge by adding the sources here
   # embedder=hf_embedder,
)


### ==========================================
### AFTER TRIGGER TEAM
### ==========================================
from .agent_trigger import ivm_trigger_architect_agent
from .agent_trigger import task_differential_analysis, task_trigger_generation, task_contract_validation

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









### ==========================================
### TRIGGERS TEAM
### ==========================================












### ==========================================
### ANSWER TEAM
### ==========================================
answer_team = Crew(
   agents=[
      tr_patterns_agent
   ],
   tasks=[
      answer_task
   ],
   process='sequential',
   # knowledge_sources=[transformation_rules_patterns], # Enable knowledge by adding the sources here
   # embedder=hf_embedder,
)