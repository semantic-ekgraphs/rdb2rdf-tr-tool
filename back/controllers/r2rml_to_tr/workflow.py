from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

object_preserving_source = TextFileKnowledgeSource(
   file_paths=["object_preserving_definition.txt"]
)












### ==========================================
### AFTER TRIGGER TEAM
### ==========================================
# from .agent_trigger import ivm_trigger_architect_agent
# from .agent_trigger import task_differential_analysis, task_trigger_generation, task_contract_validation

# ivm_compilation_crew = Crew(
#    agents=[ivm_trigger_architect_agent],
#    tasks=[
#       task_differential_analysis,
#       task_trigger_generation,
#       task_contract_validation
#    ],
#    process=Process.sequential,  # Fluxo controlado por etapas analíticas e dependentes
#    verbose=True
# )









### ==========================================
### TRIGGERS TEAM
### ==========================================










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

# No crew knowledge needed
# from agents.queue import queue_agent, queue_task
# queue_crew = Crew(agents=[queue_agent], tasks=[queue_task])