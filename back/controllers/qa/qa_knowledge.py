from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

person_knowledge_source_str = StringKnowledgeSource(
   content="Renan Freitas é casado com Mara Kelly. Eles tem a Maria."
)

person_knowledge_source_txt = TextFileKnowledgeSource(
   file_paths=["renato-data.txt"]
)
