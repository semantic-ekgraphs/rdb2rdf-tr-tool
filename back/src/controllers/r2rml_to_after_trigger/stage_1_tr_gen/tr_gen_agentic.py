from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_6_luna_openai
from models.stage1 import MetadataParsing
from src.utils import get_prompt_of_a_pydantic_model, get_prompt_of_columns
from src.constants import TEXTS
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# Estou seguindo o documento do artigo: 
# https://docs.google.com/document/d/1FU7M8qcHQhQvPcYbidvnTS28UfEBj5H_lqayQ_pAc-s/edit?tab=t.0


### ==========================================
### AGENTS | STAGE 1
### ==========================================
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


tr_reviewer_agent = Agent(
   role="Transformation Rules Semantic Validation & Review Specialist",
   goal=(
      "Independently audit and validate generated Transformation Rules (TRs) to guarantee "
      "their complete semantic consistency with original R2RML mappings and validated metadata. "
      "Rigorously verify pivot relations, foreign-key relational paths, URI construction functions, "
      "RDF predicates, and SQL selection conditions, ensuring the compiled TR set is fully "
      "accurate, semantically equivalent, and ready for deployment."
   ),
   backstory=(
      "You are an expert Semantic Web Quality Assurance Specialist and Formal Logic Auditor "
      "with deep expertise in relational database schemas, R2RML mapping specifications, "
      "and RDB2RDF view formalisms. You serve as an independent reviewer in the compilation pipeline. "
      "Your mission is to perform meticulous peer reviews on compiled Transformation Rules (CTRs, OTRs, "
      "Local DTRs, and Path DTRs) generated from R2RML mappings. You cross-examine every formal TR "
      "against the source metadata to ensure that no relational join paths are distorted, no selection "
      "conditions are omitted, and all URI templates and RDF predicates maintain absolute semantic "
      "fidelity to the original specification."
   ),
   verbose=True,
   memory=False
)



### ==========================================
### TASK 1 | STAGE 1
### ==========================================
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
   "- Always include the rdf:type for rdf_predicate column if a rr:subjectMap has rr:class property;\n"
   "- Do not parse commented-out R2RML mappings. Comments in R2RML start with #;\n"
   "- Never invent or create CONSTRAINT names;\n"
   "- Remove any invented or created CONSTRAINT name.\n\n"
   "Inputs: \n"
   "<R2RML mappings>{r2rml_mapping}</R2RML mappings>\n\n"
   "<Relational Schema>{rdb_schema}</Relational Schema>\n"
   ),
   expected_output=(
      "R2RML metadata report organized in the following columns:"
      f"{get_prompt_of_columns(TriplesMapParsing)}"
      "Concatenate the CONSTRAINT names, separated by ' | '."
   ),
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/extracted_metadata_{date_now}.md",
   agent=agent_transformation_rule_generation
)







### ==========================================
### TASK 2 | STAGE 1
### ==========================================
from .model import EntityPreservationRow
task_entity_preservation_analysis = Task(
   description=(
"Verifies whether the R2RML mappings, in <Extracted Metadada> input, satisfy the assumptions required by "
"the formal entity-preserving specification. "
"In particular, it identifies:"
"- relation;\n"
"- pivot relations;\n"
"- checks whether entity identities are preserved;\n"
"- generates and validates URI construction functions;\n"
"- analyzes relational paths; and\n"
"- detects constructs that violate the entity-preserving property;\n"
"- correction recommended.\n\n"
"Important Requirements:\n"
"- In the relational schema, consider SERIAL as the primary key and UUID as the unique key.\n"
"Inputs: "
"<Extracted Metadada>{extracted_metadata}</Extracted Metadada>\n"
),
   expected_output=(
      "Entity-preservation report with the title 'Entity-Preservation Analisys', besides the following columns:"
      f"{get_prompt_of_columns(EntityPreservationRow)}"
      ""
   ),
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/entity_preservation_analysis_{date_now}.md",
   agent=agent_transformation_rule_generation
)









### ==========================================
### TASK 3 | STAGE 1
### ==========================================
from .model import TransformationRuleRow
task_transformation_rule_generation = Task(
   description=(
   "Using the <validated metadata> and <entity_preservation_analysis>, compile each R2RML mapping "
   "into a formal Transformation Rule (TR) specification.\n\n"
   "Inputs: "
   "<validated metadata>{validated_metadata}</validated metadata>\n\n"
   "<R2RML mappings>{r2rml_mapping}</R2RML mappings>\n\n"
   "<entity_preservation_analysis>{entity_preservation_analysis}<entity_preservation_analysis>\n\n"
   "For each mapping, you MUST:\n"
   "- Analyze the mapping logic and classify it precisely into one of the four formal categories: "
   "  - Class Transformation Rule (CTR);\n"
   "  - Object Property Transformation Rule (OTR);\n"
   "  - Local Datatype Transformation Rule (Local DTR); or\n "
   "  - Path Datatype Transformation Rule (Path DTR).\n"
   "- Identify the pivot relation that determines resource identity and subject URI generation.\n"
   "- Construct the formal TR specification using the appropriate Global URI Predicates and auxiliary built-ins.\n"
   "- Isolate relational join paths and position them as the final term in the rule body when required."
   ),
   expected_output="""
A structured report in Markdown format (.md) containing the compiled Transformation Rules (TRs).

The report MUST strictly follow this Markdown structure:

# Generated Transformation Rules Report

## 1. Overview
Summary of the total number of compiled R2RML mappings and their assigned transformation rule categories.

## 2. Compiled Transformation Rules
For each processed R2RML mapping:
- **TriplesMap Identifier**: Name or ID of the source R2RML TriplesMap.
- **Rule Identifier**: Assigned TR name (e.g., `\psi_artist_01`).
- **Rule Type**: Strictly categorized as `CTR` (Class Transformation Rule), `OTR` (Object Property Transformation Rule), `Local DTR` (Local Datatype Transformation Rule), or `Path DTR` (Path Datatype Transformation Rule).
- **Pivot Relation**: Identified base or derived relation acting as the identity pivot.
- **Formal TR Specification**: The complete formal logic formula representing the rule.
- **Relational Path**: Positioned as the final term in the rule body (if applicable).

---
*(Repeat for all generated rules)*
""",
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/transformation_rules_{date_now}.md",
   agent=agent_transformation_rule_generation
)



task_transformation_rule_validation = Task(
   description=(
   "Independently audit and validate the generated Transformation Rules produced in the previous task "
   "against the original input data (validated metadata and R2RML mappings).\n\n"
   "Input Data Context:\n"
   "- Compiled Transformation Rules (Output of Task 1)\n"
   "- Validated metadata\n"
   "- Original R2RML mappings\n\n"
   "Your verification MUST independently check for semantic consistency across all generated TRs, verifying:\n"
   "1. Correct identification of pivot relations.\n"
   "2. Accuracy of relational paths and foreign-key join traversals.\n"
   "3. Correct implementation of URI construction functions and namespaces.\n"
   "4. Precise alignment of RDF predicates and SQL selection conditions with the original R2RML definitions.\n"
   "5. Complete preservation of original mapping semantics without loss or unauthorized modifications."
   ),
   expected_output="""
A structured Validation Report in Markdown format (.md) verifying the compiled Transformation Rules.

The report MUST strictly follow this Markdown structure:

# Transformation Rules Validation Report

## 1. Validation Summary
- **Overall Status**: `PASSED` (Fully Validated) or `FAILED` (Inconsistencies Found).
- **Total Rules Evaluated**: Total count of audited TRs.
- **Compliance Rate**: Percentage of rules fully matching semantic specifications.

## 2. Audit Checklist & Consistency Analysis
For each compiled Transformation Rule:
- **Rule Identifier**: The audited rule name (e.g., `\psi_artist_01`).
- **Pivot Relation Audit**: [PASS/FAIL] - Verification against source metadata.
- **Relational Path Audit**: [PASS/FAIL] - Verification of foreign key join paths.
- **URI Construction Functions**: [PASS/FAIL] - Verification of URI templates and namespace predicates.
- **Predicates & Selection Conditions**: [PASS/FAIL] - Verification that SQL selection logic and RDF predicates match the original mapping.
- **Semantic Consistency Status**: [PASS/FAIL] - Final verification against original R2RML semantics.

## 3. Discrepancies & Feedback
*(Include details for any failed rule)*
- **Rule ID**: [ID]
- **Detected Issue**: Description of the semantic deviation from original R2RML mappings.
- **Required Correction**: Recommended adjustment to achieve full semantic equivalence.

## 4. Final Validated Set of Transformation Rules
*(Included when overall status is PASSED)*
The finalized, fully verified set of formal Transformation Rules ready for downstream deployment.
""",
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/validated_transformation_rules_{date_now}.md",
   context=[task_transformation_rule_generation],  # Explicit dependency on Task 1
   agent=tr_reviewer_agent
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
transformation_rules_team_task_1 = Crew(
   agents=[
      agent_transformation_rule_generation
   ],
   tasks=[
      task_metadata_extraction_and_normalization
   ],
   process='sequential',
   knowledge_sources=[ # Enable knowledge by adding the sources here
      knowledge_source_transformation_rule_patterns_v2
   ], 
)


transformation_rules_team_task_2 = Crew(
   agents=[
      agent_transformation_rule_generation
   ],
   tasks=[
      task_entity_preservation_analysis
   ],
   process='sequential',
   knowledge_sources=[
      knowledge_of_formal_entity_preserving_specification
   ], 
)


transformation_rules_team_task_3 = Crew(
   agents=[
      agent_transformation_rule_generation
   ],
   tasks=[
      task_transformation_rule_generation,
      task_transformation_rule_validation
   ],
   process='sequential',
   knowledge_sources=[
      knowledge_of_formal_entity_preserving_specification,
      knowledge_source_transformation_rule_patterns_v2
   ], 
)