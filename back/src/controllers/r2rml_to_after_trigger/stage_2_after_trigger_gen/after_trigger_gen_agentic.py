from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_4o_mini_openai, gpt_6_luna_openai
from src.utils import get_prompt_of_columns
from src.constants import TEXTS
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Estou seguindo o documento do artigo: https://docs.google.com/document/d/1FU7M8qcHQhQvPcYbidvnTS28UfEBj5H_lqayQ_pAc-s/edit?tab=t.0



### ==========================================
### AGENTS of STAGE 2
### ==========================================

after_trigger_generation_agent = Agent(
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


agent_ivm_critic = Agent(
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
### TASKS of STAGE 2
### ==========================================

# Tasks 1 / Stage 2
# provided relational schema and
from .model import TriggerPlanRow
task_trigger_planning = Task(
   description=(
      "Analyze the set of Transformation Rules inputed "
      "to determine the required incremental maintenance strategy for each database relation $R$, "
      "without generating SQL code at this stage.\n\n"
      "For each updated relation $R$, you must:\n"
      "1. Compute the set $Relev(R)$ of all relevant Transformation Rules.\n"
      "2. Classify each rule in the set as 'pivot-relevant' or 'relation-relevant'.\n"
      "3. Identify whether multiple occurrences of relation $R$ exist in the rule's relational path.\n"
      "4. Map and specify which formal maintenance components must be computed by the trigger, "
      "including: affected pivot tuples for deletion ($A^-$), affected pivot tuples for insertion ($A^+$), "
      "post-update contributions ($S2$), and final insertion ($\Delta^+$) and deletion ($\Delta^-$) changesets.\n\n"
      "Consolidate all analyses into a declarative execution plan that will directly guide the trigger synthesis agent."
      "Inputs:"
      "<Transformation Rules>{transformation_rules}</Transformation Rules>\n\n"
      "<Relational Schema>{rdb_schema}</Relational Schema>"
   ),
   expected_output=(
      "A structured report in Markdown format (.md) containing the declarative trigger execution plan for each analyzed relation R. "
      "The response MUST contain exclusively the Markdown structure, with no introductory text or footnotes outside the report.\n\n"
      "For each relation $R$ in the relational schema, the output must present the following structure:\n"
      "# Declarative Trigger Maintenance Plan for Relation: [Relation Name R]\n"
      "## 1. Relevant Rules Mapping ($Relev(R)$)\n"
      "List of all Transformation Rules (TRs) affected by updates on relation R. For each rule:\n"
      "- **Rule ID**: Rule identifier (e.g., $\psi\_track\_01$).\n"
      "- **Relevance Classification**: Strictly classify as `pivot-relevant` (if R is the pivot relation) or `relation-relevant` (if R participates in the relational path).\n"
      "- **Relational Path Occurrences**: Indicate whether relation R appears once or multiple times in the rule's relational path.\n\n"
      "## 2. Maintenance Components to Be Computed\n"
      "Declarative specification of the algebraic structures required for incremental maintenance:\n"
      "- **Affected Pivot Tuples for Deletion ($A^-$)**: Definition of the query/expression to isolate removed pivot tuples.\n"
      "- **Affected Pivot Tuples for Insertion ($A^+$)**: Definition of the query/expression to isolate new pivot tuples.\n"
      "- **Post-Update Contributions ($S2$)**: Mapping of the post-update state V2 to validate stability and resource support.\n"
      "- **Deletion and Insertion Changesets ($\Delta^-$ and $\Delta^+$)**: Definition of the final RDF triples/quads deltas to be recorded in the queue.\n"
      "---"
      "*(Repeat the structure above for all relations R present in the relational schema in the following columns:"
      f"{get_prompt_of_columns(TriggerPlanRow)})*"
   ),
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/trigger_execution_plan_{date_now}.md",
   agent=after_trigger_generation_agent
)



# Tasks 2 | Stage 2
from .model import StaticVerificationRow
task_trigger_synthesis = Task(
   description=(
      "Based on the trigger execution plan, generates PostgreSQL AFTER triggers "
      "implementing the incremental maintenance algorithm described in Algorithm 1. "
      "The generated triggers use statement-level transition tables, compute the required maintenance structures, "
      "and populate the asynchronous maintenance queue.\n\n" 

      "Input:\n"
      "<trigger execution plan>{trigger_execution_plan}\n</trigger execution plan>\n\n"
      "<Transformation Rules>{transformation_rules}\n</Transformation Rules>"
   ),
   expected_output=(
      "Statistically verified PostgreSQL AFTER triggers"
   ),
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/after_trigger_{date_now}.md",
   # context=[task_trigger_planning],
   agent=after_trigger_generation_agent
)



# Tasks 3 | Stage 2
from .model import StaticVerificationRow
# task_trigger_static_verification = Task(
#    description=(
#       "After generation, performs static verification. "
#       "Instead of executing the code, it checks whether the generated implementation conforms to the "
#       "formal specification. The validation includes verification of:"
#       "- correct identification of (Relev(R));"
#       "- correct computation of (A^{-}), (A^{+}), (S2), (\Delta^{+}{pivot}), (\Delta^{+}{rel}), and (\Delta^{+});"
#       "- correct URI construction functions and named graphs;"
#       "- correct relational joins and predicates;"
#       "- proper use of PostgreSQL transition tables; and"
#       "- absence of hallucinated attributes, predicates, relations, or transformation rules."
      
#       "When inconsistencies are detected, the synthesis agent receives structured feedback and regenerates only the affected components."
      
#       "Input:"
#       "<trigger execution plan>{trigger_execution_plan}</trigger execution plan>\n\n"
#       "<Transformation Rules>{transformation_rules}</Transformation Rules>"
#    ),
#    expected_output=(
#       "Statistically verified PostgreSQL AFTER triggers in the following columns:"
#       f"{get_prompt_of_columns(StaticVerificationRow)})*"
#    ),
#    output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/after_trigger_{date_now}.md",
#    # context=[task_trigger_planning],
#    agent=agent_ivm_critic
# )





task_trigger_static_verification = Task(
   description=(
      "Perform a thorough static verification on the generated PostgreSQL AFTER triggers "
      "to ensure strict conformance with the formal IVM specification without executing the code.\n\n"
      "Input Context Required:\n"
      "- Trigger Execution Plan (from Stage 2.1)\n"
      "- Transformation Rules and Relational Schema (from Stage 1)\n"
      "- Generated SQL/PL-pgSQL Trigger Code\n\n"
      "Your validation MUST rigorously check the following criteria:\n"
      "1. Correct identification of the relevant transformation rules set ($Relev(R)$).\n"
      "2. Accurate algebraic computation of all changeset components: affected deletion pivot tuples ($A^-$), "
      "affected insertion pivot tuples ($A^+$), post-update contributions ($S2$), insertion deltas ($\Delta^+_\{pivot\}$ and $\Delta^+_\{rel\}$), "
      "and the overall insertion changeset ($\Delta^+$).\n"
      "3. Correct implementation of URI construction functions, URI templates, and named graph specifications.\n"
      "4. Precise relational joins, foreign key paths, and database predicates.\n"
      "5. Proper usage of PostgreSQL statement-level transition tables (e.g., `REFERENCING OLD TABLE AS ... NEW TABLE AS ...`).\n"
      "6. Complete absence of hallucinated attributes, predicates, relations, or non-existent transformation rules.\n\n"
      "If any inconsistency or defect is found, generate structured, actionable feedback specifying exactly "
      "which component failed so the synthesis agent can regenerate only the affected parts."
   ),
   expected_output="""
A structured Static Verification and Audit Report in Markdown format (.md)

The output MUST contain exclusively the Markdown report structure, without any extra conversational text or footnotes.

The report must follow this exact structure:

# Static Verification Report: PostgreSQL AFTER Triggers Audit

## 1. Executive Verification Summary
- **Verification Status**: `PASSED` (Statistically Verified) or `FAILED` (Action Required).
- **Target Relation(s)**: List of database relation(s) audited.
- **Overall Compliance Score**: Summary of conformance against formal IVM specifications.

## 2. Checklist Verification Details
Detailed evaluation for each audit dimension:
- **Relevance Identification ($Relev(R)$)**: [PASS/FAIL] - Verification of whether all relevant transformation rules were correctly identified.
- **Algebraic Changeset Computations**: [PASS/FAIL] - Verification of $A^-$, $A^+$, $S2$, $\Delta^+_\{pivot\}$, $\Delta^+_\{rel\}$, and $\Delta^+$.
- **URI Construction & Named Graphs**: [PASS/FAIL] - Verification of URI functions, templates, and named graph declarations.
- **Relational Joins & Predicates**: [PASS/FAIL] - Verification of schema join paths, foreign keys, and predicate alignment.
- **PostgreSQL Transition Tables**: [PASS/FAIL] - Verification of `REFERENCING OLD TABLE / NEW TABLE` statement-level syntax.
- **Hallucination Audit**: [PASS/FAIL] - Confirmation of the absence of non-existent attributes, predicates, relations, or transformation rules.

## 3. Detected Inconsistencies & Structured Feedback
*(Only if Status is FAILED or requires regeneration)*
For each detected issue, provide structured feedback to guide the synthesis agent:
- **Affected Component/Rule**: [Name/ID of the affected component or rule]
- **Specific Defect**: Clear explanation of the discrepancy between generated SQL code and formal specifications.
- **Actionable Correction**: Precise guidance on how to regenerate only the affected component.

## 4. Final Verified Code Output
*(Only included if Verification Status is PASSED)*
The complete, statically verified PostgreSQL AFTER trigger SQL statements and PL/pgSQL function code.
""",
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/after_trigger_{date_now}.md",
   context=[task_trigger_planning],
   agent=agent_ivm_critic,  # The critic/auditor agent
)




















### ==========================================
### TEAM
### ==========================================
from crewai import Crew
from knowledge.sources_of_knowledge import knowledge_of_formal_entity_preserving_specification 
from knowledge.sources_of_knowledge import knowledge_source_transformation_rule_patterns_v2
from knowledge.sources_of_knowledge import knowledge_source_of_maintanance_queue_infrastructure
from knowledge.sources_of_knowledge import knowledge_source_of_algorithm_1

after_trigger_gen_team = Crew(
   agents=[
      after_trigger_generation_agent,
      # agent_ivm_critic
   ],
   tasks=[
      # task_trigger_planning,
      task_trigger_synthesis,
      # task_trigger_static_verification
   ],
   process='sequential',
   knowledge_sources=[
         knowledge_of_formal_entity_preserving_specification,
         knowledge_source_transformation_rule_patterns_v2,
         knowledge_source_of_maintanance_queue_infrastructure,
         knowledge_source_of_algorithm_1
      ], # Enable knowledge by adding the sources here
)