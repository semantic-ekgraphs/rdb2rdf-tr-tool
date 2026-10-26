from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource 


# https://www.youtube.com/watch?v=05BZmeTbsrg

def instruction_consult_knowledge_source(sources:str):
   return (
      f"You have direct access to the of {sources} through its integrated knowledge base (knowledge sources). "
      "Always consult this base before providing any response."
      "You should prioritize information from your integrated knowledge, or, in other words, "
      "your primary source of truth is the knowledge you have available."
   )


knowledge_stage_1 = PDFKnowledgeSource(
   file_paths=[
      "rdb2rdf-views.pdf",
      "formal-especification-of-entity-preserving.pdf",
      "transformation-rules-patterns-rdb2rdf-views.pdf"
   ]
)


knowledge_stage_2 = PDFKnowledgeSource(
   file_paths=[
      "rdb2rdf-views.pdf",
      "transformation-rules-patterns-rdb2rdf-views.pdf",
      "algorithm-2-compute-changeset-r.pdf",
      "algorithm-1-compute-delta-r.pdf",
      "Maintenance-Queue-Infrastructure.pdf"
   ]
)