from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_4o_mini_openai, gpt_6_luna_openai
from src.utils import get_prompt_of_a_pydantic_model, get_prompt_of_columns
from src.constants import TEXTS
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Estou seguindo o documento do artigo: https://docs.google.com/document/d/1FU7M8qcHQhQvPcYbidvnTS28UfEBj5H_lqayQ_pAc-s/edit?tab=t.0



### ==========================================
### AGENTS of STAGE 2
### ==========================================

trigger_generation_agent = Agent(
   role="PostgreSQL IVM Trigger Planning and Synthesis Specialist",
   goal=(
      "Synthesize production-grade, statically verified PostgreSQL AFTER triggers "
      "that automate Incremental View Maintenance (IVM) for RDF graphs based on formal "
      "Transformation Rules. The agent must first compute a declarative maintenance "
      "plan for each updated relation R by determining Relev(R), classifying rules as "
      "pivot-relevant or relation-relevant, detecting multiple relation occurrences in "
      "relational paths, and identifying required components (A-, A+, S2, Delta+ pivot, "
      "Delta+ rel, and Delta+). Then, it must generate statement-level triggers using "
      "PostgreSQL transition tables to populate the asynchronous maintenance queue "
      "without hallucinating attributes, predicates, or schema joins, adhering strictly "
      "to feedback from static verification."
   ),
   backstory=(
      "You are an elite database engineer and formal methods expert specializing in "
      "relational-to-RDF incremental maintenance architectures. You approach trigger "
      "generation not through ad-hoc coding, but as a rigorous, two-stage compiler-like "
      "process: Planning and Synthesis. In the planning phase, you analyze the relational "
      "schema alongside Stage 1 Transformation Rules to map out exact tuple lifecycle "
      "dependencies and isolate rule relevance (Relev(R)). During synthesis, you translate "
      "these declarative execution plans into highly efficient PostgreSQL AFTER triggers "
      "that execute at the statement level, utilizing OLD TABLE and NEW TABLE transition "
      "tables. You are hyper-vigilant against hallucinated SQL elements, ensuring that "
      "all URI construction functions, named graphs, relational joins, and changeset "
      "deltas (A-, A+, S2, Delta+) match the formal specification with mathematical precision."
   ),
   verbose=True,
   memory=False,
   llm=gpt_6_luna_openai
)


ivm_critic_agent = Agent(
   role="PostgreSQL IVM Static Verification & Code Auditor Agent",
   goal=(
      "Perform rigorous static verification on generated PostgreSQL AFTER triggers to ensure "
      "absolute compliance with formal Incremental View Maintenance (IVM) specifications "
      "without executing the code. Validate the accurate identification of Relev(R), precise "
      "computation of changeset algebraic components (A-, A+, S2, Delta+ pivot, Delta+ rel, Delta+), "
      "correct URI construction functions, named graphs, relational joins, predicates, and proper "
      "use of PostgreSQL statement-level transition tables. Detect any hallucinated schema elements "
      "or rules and provide structured feedback to trigger re-synthesis when inconsistencies are found."
   ),
   backstory=(
      "You are an elite Static Code Verification and Formal Methods Auditor specializing in "
      "database system triggers and relational-to-RDF incremental maintenance architectures. "
      "Rather than relying on runtime execution, you perform deep deterministic static analysis "
      "on synthesized SQL/PL-pgSQL code. You operate as an uncompromising quality gate, auditing "
      "triggers against strict mathematical specifications. You check whether every relational join, "
      "foreign-key path, predicate, and URI constructor matches the underlying schema and ontology "
      "with absolute precision. You inspect the usage of PostgreSQL transition tables (REFERENCING OLD "
      "TABLE / NEW TABLE) to guarantee that statement-level delta structures are computed correctly. "
      "Whenever a hallucinated attribute, invalid join, or miscalculated changeset contribution is "
      "detected, you construct granular, actionable feedback to guide the synthesis agent in regenerating "
      "only the affected components."
   ),
   verbose=True,
   memory=False,
   llm=gpt_6_luna_openai
)


### ==========================================
### TASK 1 | STAGE 2
### ==========================================
# provided relational schema and
"1. Compute the set $Relev(R)$ of all relevant Transformation Rules.\n"
# "2. Classify each rule in the set as 'pivot-relevant' or 'relation-relevant'.\n"
# "3. Identify whether multiple occurrences of relation $R$ exist in the rule's relational path.\n"
# "4. Map and specify which formal maintenance components must be computed by the trigger, "
# "including: affected pivot tuples for deletion ($A^-$), affected pivot tuples for insertion ($A^+$), "
# "post-update contributions ($S2$), and final insertion ($\Delta^+$) and deletion ($\Delta^-$) changesets.\n\n"
# "Consolidate all analyses into a declarative execution plan that will directly guide the trigger synthesis agent."
#---
# "The response MUST contain exclusively the Markdown structure, with no introductory text or footnotes outside the report.\n\n"
      # "For each relation $R$ in the relational schema, the output must present the following structure:\n"
      # "# Declarative Trigger Maintenance Plan for Relation: [Relation Name R]\n"
      # "## 1. Relevant Rules Mapping ($Relev(R)$)\n"
      # "List of all Transformation Rules (TRs) affected by updates on relation R. For each rule:\n"
      # "- **Rule ID**: Rule identifier (e.g., $\psi\_track\_01$).\n"
      # "- **Relevance Classification**: Strictly classify as `pivot-relevant` (if R is the pivot relation) or `relation-relevant` (if R participates in the relational path).\n"
      # "- **Relational Path Occurrences**: Indicate whether relation R appears once or multiple times in the rule's relational path.\n\n"
      # "## 2. Maintenance Components to Be Computed\n"
      # "Declarative specification of the algebraic structures required for incremental maintenance:\n"
      # "- **Affected Pivot Tuples for Deletion ($A^-$)**: Definition of the query/expression to isolate removed pivot tuples.\n"
      # "- **Affected Pivot Tuples for Insertion ($A^+$)**: Definition of the query/expression to isolate new pivot tuples.\n"
      # "- **Post-Update Contributions ($S2$)**: Mapping of the post-update state V2 to validate stability and resource support.\n"
      # "- **Deletion and Insertion Changesets ($\Delta^-$ and $\Delta^+$)**: Definition of the final RDF triples/quads deltas to be recorded in the queue.\n"
from .model import TriggerPlanRow
task_trigger_planning = Task(
   description=(
      "Analyze the set of transformation rules "
      "to determine the incremental maintenance strategy required for each database pivot relation $R$ present in the Transformation Rules "
      "without generating SQL code at this stage.\n\n"
      "For each pivot relation $R$ in <Transformation Rules>, you must:\n"
       f"{get_prompt_of_a_pydantic_model(TriggerPlanRow)}\n\n"
      "Inputs:"
      "<Transformation Rules>{transformation_rules}</Transformation Rules>\n\n"
      "<Relational Schema>{rdb_schema}</Relational Schema>"
   ),
   expected_output=(
      "A structured report in Markdown format (.md) containing the declarative trigger execution plan for each analyzed relation R. "
      "---"
      "*(Repeat for all relations R present in the transformation rules, following the columns:"
      f"{get_prompt_of_columns(TriggerPlanRow)})*"
   ),
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/stage2/trigger_execution_plan_{date_now}.md",
   agent=trigger_generation_agent
)



### ==========================================
### TASK 2 | STAGE 2
### ==========================================
from .model import StaticVerificationRow
trigger_synthesis_task = Task(
   description=(
      "Based on the provided trigger execution plan and Transformation Rules, "
      "generates the corresponding PostgreSQL AFTER triggers and PL/pgSQL functions, " 
      "implementing the incremental maintenance Algorithm 1.\n\n"
      "Input Context:\n"
      "<trigger execution plan>{trigger_execution_plan}\n</trigger execution plan>\n\n"
      "<Transformation Rules>{transformation_rules}\n</Transformation Rules>"
      "Your synthesis of AFTER triggers PL/pgSQL must implement the following architectural requirements:\n"
      "1. Utilize statement-level transition tables (`REFERENCING OLD TABLE AS OLD_R NEW TABLE AS NEW_R`) "
      "to capture snapshots of update events over relation R ($\Delta^-$ and $\Delta^+$).\n"
      "2. Compute the affected tuples for removal ($A^-[\Psi](u)$).\n"
      "3. Compute the affected tuples for insertion ($A^+[\Psi](u)$).\n"
      "4. Compute the post-update contributions ($S2[\Psi](u)$) for each relevant rule $\Psi$.\n"
      "5. Compute the final insertion ($\Delta^+(u)$) and deletion changesets.\n"
      "6. Construct clean, production-ready SQL statements that populate the asynchronous maintenance queue."
   ),
   expected_output="""
A structured PostgreSQL Trigger Implementation Report in Markdown format (.md).

The output MUST contain exclusively the Markdown report structure, without any extra conversational text or footnotes.

The report must follow this exact structure:

# PostgreSQL AFTER Trigger Implementation Report

## 1. Synthesis Overview
- **Target Relation(s)**: List of database relation(s) processed (e.g., Relation R).
- **Architecture Compliance**: Confirmation of statement-level transition table usage (`REFERENCING OLD TABLE / NEW TABLE`) and asynchronous maintenance queue population.

## 2. Trigger Execution & Component Computation
Detailed breakdown of the implemented logic for the generated SQL code:
- **Snapshot Capture**: Description of how transition tables ($\Delta^-$ and $\Delta^+$) capture update event snapshots.
- **Affected Deletion Tuples ($A^-[\Psi](u)$)**: Implementation logic isolating affected pivot tuples for deletion.
- **Affected Insertion Tuples ($A^+[\Psi](u)$)**: Implementation logic isolating affected pivot tuples for insertion.
- **Post-Update Contributions ($S2[\Psi](u)$)**: Implementation logic computing post-update RDF states for rule $\Psi$.
- **Changesets Computation ($\Delta^+(u)$ and $\Delta^-(u)$)**: Final aggregation logic for insertion and deletion changesets.

## 3. Asynchronous Maintenance Queue Integration
- Explanation of how computed components are serialized and loaded into the maintenance queue infrastructure.

## 4. Generated PostgreSQL AFTER Trigger Code
- Complete, syntactically correct SQL/PL-pgSQL code blocks for the statement-level AFTER triggers and associated functions.
""",
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/stage2/postgresql_after_triggers_{date_now}.md",
   agent=trigger_generation_agent
)



### ==========================================
### TASK 3 | STAGE 2
### ==========================================
trigger_static_verification_task = Task(
   description=(
      "Perform rigorous static verification of the generated PostgreSQL AFTER triggers, "
      "without executing the code, to attest to their complete conformance with the formal specification.\n\n"
      "Input Context:\n"
      "<generated PostgreSQL AFTER triggers>{postgresql_after_triggers}\n</generated PostgreSQL AFTER triggers>\n\n"
      "Your validation audit MUST exhaustively verify:\n"
      "1. The correct identification of the set of relevant rules Relev(R).\n"
      "2. The precision in computing A-, A+, S2, Δ+pivot, Δ+rel, and Δ+.\n"
      "3. The correctness of URI constructors and named graphs.\n"
      "4. The accuracy of relational joins and logical predicates.\n"
      "5. The proper employment of PostgreSQL transition tables (REFERENCING OLD TABLE / NEW TABLE).\n"
      "6. The total absence of hallucinated attributes, predicates, relations, or rules.\n\n"
      "If any inconsistencies are detected, produce structured and actionable feedback "
      "so that the synthesis agent can proceed with regeneration restricted solely to the affected components."
   ),
   expected_output="""
A structured Static Verification Report in Markdown format (.md).

The output MUST contain exclusively the Markdown report structure, without any extra conversational text or footnotes outside of it.

The report must follow this exact structure:

# Static Verification Report: PostgreSQL AFTER Triggers

## 1. Executive Validation Summary
- **Verification Status**: `PASSED` (Statistically Verified) or `FAILED` (Inconsistencies Found).
- **Scope**: PostgreSQL AFTER triggers submitted for auditing.

## 2. Detailed Compliance Checklist
Detailed evaluation for each dimension required by the formal specification:
- **Identification of Relev(R)**: [PASSED / FAILED] - Verification of the accuracy of associated relevant rules.
- **Algebraic Components Computation**: [PASSED / FAILED] - Audit of calculations for $A^-$, $A^+$, $S2$, $\Delta^+_\{pivot\}$, $\Delta^+_\{rel\}$, and $\Delta^+$.
- **URI Constructors and Named Graphs**: [PASSED / FAILED] - Validation of URI functions and named graph declarations.
- **Relational Joins and Predicates**: [PASSED / FAILED] - Check of foreign key paths and logical conditions.
- **PostgreSQL Transition Tables**: [PASSED / FAILED] - Validation of correct statement-level usage of `REFERENCING OLD TABLE / NEW TABLE`.
- **Hallucination Audit**: [PASSED / FAILED] - Confirmation of the absolute absence of non-existent attributes, predicates, relations, or rules.

## 3. Detected Inconsistencies and Structured Feedback
*(Filled out only if the status is FAILED)*
For each defect found, provide clear guidance for selective regeneration:
- **Affected Component / Rule**: Identification of the element with a deviation.
- **Specific Defect**: Explanation of the divergence from the formal specification.
- **Actionable Correction**: Precise instruction to regenerate only the affected part.

## 4. Final Approved Code
*(Included only if the status is PASSED)*
- The complete and strictly validated SQL/PL-pgSQL code of the AFTER triggers.
""",
   agent=ivm_critic_agent,  # Independent critic agent responsible for auditing
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/stage2/triggers_static_verification_report_{date_now}.md",
)












### ==========================================
### TEAM
### ==========================================
from crewai import Crew
from knowledge.sources_of_knowledge import knowledge_of_formal_entity_preserving_specification 
from knowledge.sources_of_knowledge import knowledge_source_transformation_rule_patterns_v2
from knowledge.sources_of_knowledge import knowledge_source_of_maintanance_queue_infrastructure
from knowledge.sources_of_knowledge import knowledge_source_of_algorithm_1
from knowledge.sources_of_knowledge import knowledge_of_rdb2rdf_views

after_trigger_gen_team_1 = Crew(
   agents=[
      trigger_generation_agent,
   ],
   tasks=[
      task_trigger_planning,
   ],
   process='sequential',
   knowledge_sources=[
         knowledge_of_rdb2rdf_views,
         knowledge_source_of_algorithm_1,
         knowledge_source_of_maintanance_queue_infrastructure,
      ], 
)


after_trigger_gen_team_2 = Crew(
   agents=[
      trigger_generation_agent,
   ],
   tasks=[
      trigger_synthesis_task,
   ],
   process='sequential',
   knowledge_sources=[
      knowledge_of_rdb2rdf_views,
      knowledge_source_of_algorithm_1,
      knowledge_source_of_maintanance_queue_infrastructure,
   ],
)


after_trigger_gen_team_3 = Crew(
   agents=[
      ivm_critic_agent,
   ],
   tasks=[
      trigger_static_verification_task,
   ],
   process='sequential',
   knowledge_sources=[
      knowledge_of_rdb2rdf_views,
      knowledge_source_of_maintanance_queue_infrastructure,
      knowledge_source_of_algorithm_1
   ],
)