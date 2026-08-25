from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

knowledge_source_transformation_rule_patterns = TextFileKnowledgeSource(
   file_paths=["tr_patterns_v2.txt"]
)

transformation_rules_formalism = TextFileKnowledgeSource(
   file_paths=["formal_espec_entity_preserving.txt"]
)

knowledge_of_transformation_rules = TextFileKnowledgeSource(
   file_paths=["formal_espec_entity_preserving.txt", "tr_patterns_v2.txt"]
)

# object_preserving_definition_knowledge_source = TextFileKnowledgeSource(
#    file_paths=["object_preserving_definition.txt"]
# )

# entity_preserving_definition_knowledge_source = TextFileKnowledgeSource(
#    file_paths=["entity_preserving_definition.txt"]
# )

# tr_patterns_knowledge_source_txt = TextFileKnowledgeSource(
#    file_paths=["tr_patterns_v2.txt"]
# )

# object_preserving_definition_knowledge_source = TextFileKnowledgeSource(
#    file_paths=["object_preserving_definition.txt"]
# )

# entity_preserving_definition_knowledge_source = TextFileKnowledgeSource(
#    file_paths=["entity_preserving_definition.txt"]
# )



# tr_patterns_knowledge_source_txt = TextFileKnowledgeSource(
#    file_paths=["tr_patterns_v2.txt"]
# )

# object_preserving_definition_knowledge_source = TextFileKnowledgeSource(
#    file_paths=["object_preserving_definition.txt"]
# )

# entity_preserving_definition_knowledge_source = TextFileKnowledgeSource(
#    file_paths=["entity_preserving_definition.txt"]
# )