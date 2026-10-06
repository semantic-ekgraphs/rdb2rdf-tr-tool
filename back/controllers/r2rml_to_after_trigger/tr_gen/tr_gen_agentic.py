from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_6_luna_openai
from models.stage1 import MetadataParsing
from utils import get_prompt_of_a_pydantic_model, get_prompt_of_columns
from constants import TEXTS
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# Estou seguindo o documento do artigo: 
# https://docs.google.com/document/d/1FU7M8qcHQhQvPcYbidvnTS28UfEBj5H_lqayQ_pAc-s/edit?tab=t.0


### ==========================================
### AGENTS
### ==========================================
# Stage 1
agent_transformation_rule_generation = Agent(
   role="Principal Knowledge Engineer and Formal Semantic Web Architect",
   goal=(
      "The objective of this stage is to transform an R2RML specification into a set of "
      "formally defined Transformation Rules (TRs) that conform to the conceptual framework."
   ),
   backstory=(
      "You are a world-class authority on semantic data integration frameworks and the creator of "
      "advanced relational-to-RDF compilation formalisms. You possess an unparalleled mastery of both "
      "relational engine internals (DDL, foreign-key traversals, query graph dependencies) and formal "
      "logic representations of Linked Data (CTR, DTR, OTR patterns). You reject blind syntactic "
      "translation and single-shot code generation; instead, you treat mapping migration as a complex, "
      "multi-step deductive reasoning task. You excel at auditing schemas to isolate identity pivots, "
      "characterizing complex n-ary associations or events as non-object-preserving mappings, designing "
      "elegant relational views to act as pseudo-pivots, and mapping semantic connectivity precisely via "
      "ordered chains of schema-validated foreign keys. "
      "Translate R2RML TriplesMaps into schema-grounded, mathematically rigorous "
      "Transformation Rules (TRs) by reconstructing the underlying semantic structure "
      "of the relational views, identifying precise pivot relations, determining object-preservation "
      "compliance, and isolating structural relational paths as the final term of rule bodies."
   ),
   verbose=True,
   memory=False,
   llm=gpt_6_luna_openai,
)





### ==========================================
### TASKS
### ==========================================
# Tasks 1 / Stage 1
# No documento não está incluso o "selection condition"
from .model import TriplesMapParsing
task_metadata_extraction_and_normalization = Task(
   name="Metadata Extraction and Normalization",
   description=(
   "Analyze the R2RML mappings and the Relational Schema inputs.\n"
   "For each rr:TriplesMap, extract:\n"
   f"{get_prompt_of_a_pydantic_model(TriplesMapParsing)}\n\n"
   "Important Requirements:\n"
   "- Analyze each rr:TriplesMap independently;\n"
   "- Do not parse commented-out R2RML mappings. Comments in R2RML start with #.\n"
   "- Never invent or create CONSTRAINT names.\n"
   "- Remove any invented or created CONSTRAINT name.\n\n"
   "Inputs: \n"
   "<R2RML mappings>{r2rml_mapping}</R2RML mappings>\n\n"
   "<Relational Schema>{rdb_schema}</Relational Schema>\n"
   ),
   expected_output=(
      "R2RML metadata report organized in the following columns:"
      f"{' '.join(list(TriplesMapParsing.model_fields.keys()))}"
      "Concatenate the CONSTRAINT names, separated by ' / '."
   ),
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/extracted_metadata.md",
   agent=agent_transformation_rule_generation
)




# Tasks 2 / Stage 1
from .model import EntityPreservationRow
task_entity_preservation_analysis = Task(
   description=(
"Verifies whether the R2RML mappings, in <Extracted Metadada> input, satisfy the assumptions required by "
"the formal entity-preserving specification. "
"In particular, it identifies:"
"- pivot relations,\n"
"- checks whether entity identities are preserved,\n"
"- validates URI construction functions,\n"
"- analyzes relational paths, and\n"
"- detects constructs that violate the entity-preserving property.\n"
"- recommended correction.\n\n"

"Inputs: "
"<Extracted Metadada>{extracted_metadata}</Extracted Metadada>\n"
),
   expected_output=(
      "Entity-preservation report and recommended corrections in the following columns:"
      f"{' '.join(list(EntityPreservationRow.model_fields.keys()))}"
   ),
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/entity_preservation_analysis.md",
   agent=agent_transformation_rule_generation
)





# Tasks 3 / Stage 1
from .model import TransformationRuleRow
task_transformation_rule_generation_validation = Task(
   description=(
   "Using the validated metadata, compiles the R2RML mappings into Transformation Rules (TRs). "
   "For each mapping, the agent identifies whether it corresponds to a Class Transformation Rule (CTR), "
   "Object Property Transformation Rule (OTR), Local Datatype Transformation Rule (Local DTR), or "
   "Path Datatype Transformation Rule (Path DTR), and generates the corresponding formal specification."
   "Independently validates the generated TRs, checking their semantic consistency with the original "
   "R2RML mappings, including pivot relations, relational paths, URI construction functions, "
   "predicates, and selection conditions."

   "Inputs: "
   "<validated metadata>{validated_metadata}</validated metadata>\n\n"
   "<R2RML mappings>{r2rml_mapping}</R2RML mappings>\n\n"
   "<entity_preservation_analysis>{entity_preservation_analysis}<entity_preservation_analysis>"
   ),
   expected_output=(
      "Validated set of Transformation Rules in the following columns:"
      f"{get_prompt_of_columns(TransformationRuleRow)}"
   ),
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/transformation_rules.md",
   agent=agent_transformation_rule_generation
)





### ==========================================
### TRANSFORMATION RULES TEAM
### ==========================================
from crewai import Crew


object_preserving_team = Crew(
   agents=[
      agent_transformation_rule_generation
   ],
   tasks=[
      # list_triples_map_task,
      # task_extract_entity_preserving,
      # mapping_analysis_task
      # object_preserving_analysis_task,
   ],
   process='sequential',
   # knowledge_sources=[object_preserving_definition_knowledge_source]
)

from knowledge.sources_of_knowledge import knowledge_of_formal_entity_preserving_specification 
from knowledge.sources_of_knowledge import knowledge_source_transformation_rule_patterns_v2
transformation_rules_team = Crew(
   agents=[
      agent_transformation_rule_generation
      # r2rml_to_tr_agent,
   ],
   tasks=[
      # task_metadata_extraction_and_normalization
      # task_entity_preservation_analysis,
      task_transformation_rule_generation_validation,
   ],
   process='sequential',
   knowledge_sources=[
      knowledge_of_formal_entity_preserving_specification,
      knowledge_source_transformation_rule_patterns_v2], # Enable knowledge by adding the sources here
   # embedder=hf_embedder,
)