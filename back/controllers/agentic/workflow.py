import os
from pathlib import Path
from crewai import Crew
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from .agents import tr_patterns_agent, r2rml_to_tr_agent
from .agents import answer_task, task_parsing_and_pivoting
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY =         os.getenv("GROQ_API_KEY")
HUNGGINGFACE_API_KEY = os.getenv("HF_API_KEY")


### ==========================================
### KNOWLEDGE BASE
### ==========================================
transformation_rules_patterns: str
path_knowledge_tr_patterns = Path(__file__).parent / "../../knowledge/tr_patterns.txt"
# Create a knowledge source
with open(path_knowledge_tr_patterns, "r", encoding="utf-8") as file:
   tr_patterns_content = file.read()
   transformation_rules_patterns = StringKnowledgeSource(content=tr_patterns_content)
   # print(f'tr_patterns: {transformation_rules_patterns}')

### ==========================================
### TRANSFORMATION RULES TEAM
### ==========================================
transformation_rules_team = Crew(
	agents=[
      r2rml_to_tr_agent
   ],
   tasks=[
      task_parsing_and_pivoting
   ],
	process='sequential',
   knowledge_sources=[transformation_rules_patterns], # Enable knowledge by adding the sources here
   embedder={
      "provider": "huggingface",
      "config": {
         "api_key": HUNGGINGFACE_API_KEY,
         "model": "sentence-transformers/all-MiniLM-L6-v2",
      }
   },
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
	process='sequential'
)