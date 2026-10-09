from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource 


knowledge_of_formal_entity_preserving_specification = PDFKnowledgeSource(
   file_paths=["formal-especification-of-entity-preserving.pdf"]
)

knowledge_source_transformation_rule_patterns = TextFileKnowledgeSource(
   file_paths=["tr_patterns_v2.txt"]
)



knowledge_source_transformation_rule_patterns_v2 = PDFKnowledgeSource(
   file_paths=["transformation-rules-patterns-rdb2rdf-views.pdf"]
)


transformation_rules_formalism = TextFileKnowledgeSource(
   file_paths=["tr_formalism.txt"]
)


knowledge_source_of_maintanance_queue_infrastructure = PDFKnowledgeSource(
   file_paths=["Infrastructure for the Maintenance Queue.pdf"]
)

knowledge_source_of_algorithm_1 = PDFKnowledgeSource(
   file_paths=["algorithm-1-compute-delta-r.pdf"]
)
