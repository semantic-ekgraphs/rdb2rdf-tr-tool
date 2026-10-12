from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_6_luna_openai
from src.utils import get_prompt_of_columns
from src.constants import TEXTS
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Aqui está seguindo o documento do artigo: 
# https://docs.google.com/document/d/1FU7M8qcHQhQvPcYbidvnTS28UfEBj5H_lqayQ_pAc-s/edit?tab=t.0


### ==========================================
### AGENTS OF STAGE 3
### ==========================================
trigger_validation_repair_agent = Agent(
   role="PostgreSQL IVM Runtime Validation, Test Orchestration & Automated Repair Specialist",
   goal=(
      "Orchestrate rigorous runtime validation and automated repair for generated PostgreSQL "
      "AFTER triggers. The agent must automatically generate representative test scenarios covering "
      "INSERT, DELETE, and UPDATE operations over relevant relations (including complex relational "
      "paths and edge cases), execute triggers against these tests, and compare outputs against a "
      "full-rematerialization oracle. It must validate Rule Contribution Correctness and Changeset "
      "Correctness, analyze execution logs upon detecting discrepancies, diagnose the root cause, "
      "propose targeted code repairs, and revalidate until all correctness criteria are fully satisfied."
   ),
   backstory=(
      "You are an elite Quality Assurance Engineer, Automated Reasoning Specialist, and Database "
      "Debugger with deep expertise in Incremental View Maintenance (IVM) systems and relational-to-RDF "
      "pipelines. You operate as the ultimate runtime safety net in the compilation architecture. "
      "Rather than relying solely on static inspection, you subject compiled PostgreSQL triggers to "
      "stress-testing through synthetic datasets and diverse update scenarios (INSERT, DELETE, UPDATE). "
      "You command advanced oracle-based verification techniques, comparing incremental changeset outputs "
      "against full-rematerialization states to guarantee mathematical equivalence. When discrepancies "
      "surface, you inspect execution logs with surgical precision, diagnose structural logic faults, "
      "and iteratively repair the trigger code until absolute runtime correctness is achieved."
   ),
   verbose=True,
   memory=False,
   llm=gpt_6_luna_openai,
)






### ==========================================
### TASKS 1 | STAGE 3
### ==========================================
test_generation_task = Task(
   description=(
      "Automatically create representative update scenarios and synthetic small datasets "
      "to rigorously test the synthesized PostgreSQL AFTER triggers.\n\n"
      "Input Context Required:\n"
      "- Relational Schema and Transformation Rules\n"
      "- Trigger Execution Plan and Generated PostgreSQL Triggers\n\n"
      "<Relational Schema>{rdb_schema}</Relational Schema>\n"
      "<Transformation Rules>{transformation_rules}</Transformation Rules>\n"
      "<Trigger Execution Plan>{trigger_execution_plan}</Trigger Execution Plan>\n"
      "<PostgreSQL AFTER triggers>{postgresql_after_triggers}</PostgreSQL AFTER triggers>\n"
      "Your task MUST execute the following steps:\n"
      "1. Automatically construct representative update scenarios covering INSERT, DELETE, and UPDATE "
      "operations across all relevant relations in the Transformation Rules.\n"
      "2. Generate specialized synthetic small datasets designed to exercise complex relational paths, multi-hop "
      "foreign-key traversals, and critical edge cases.\n"
      "3. Output a structured, reproducible test suite ready to be consumed by the runtime validation engine."
   ),
   expected_output="""
A structured Test Generation and Dataset Specification Report in Markdown format (.md).

The output MUST contain exclusively the Markdown report structure, without any extra conversational text or footnotes outside of it.

The report must follow this exact structure:

# Test Generation and Synthetic Dataset Report

## 1. Overview
- **Target Database Relations**: Summary of relations covered by the test suite.
- **Test Scope**: Overview of generated update scenarios designed to validate Incremental View Maintenance (IVM) triggers.

## 2. Representative Update Scenarios
Detailed specification of test operations:
- **INSERT Scenarios**: Description of test cases simulating new row insertions and assessing delta additions ($\Delta^+$).
- **DELETE Scenarios**: Description of test cases simulating row removals and assessing deletion deltas ($\Delta^-$).
- **UPDATE Scenarios**: Description of test cases modifying attributes and foreign-key references.

## 3. Synthetic Datasets & Complex Paths
- **Complex Relational Paths**: Description of synthetic data structures designed to exercise multi-hop foreign-key joins and chained dependencies.
- **Edge Cases & Boundary Conditions**: Coverage details for empty sets, null attributes, and boundary state transitions.

## 4. Reproducible SQL Test Scripts
- Complete SQL statements for populating synthetic datasets and executing the structured update scenarios.
""",
   agent=trigger_validation_repair_agent,  # The validation, test, and repair specialist agent
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/test_generation_report_{date_now}.md"
)






### ==========================================
### TASKS 2 | STAGE 3
### ==========================================
runtime_validation_task = Task(
   description=(
      "Execute the generated PostgreSQL AFTER triggers against the test scenarios and "
      "compare their outputs with an oracle obtained by full recomputation of the RDB2RDF view "
      "after each update operation.\n\n"
      "Input Context Required:\n"
      "- Generated PostgreSQL AFTER Triggers\n"
      "- Test Scenarios and Synthetic Datasets (from Test Generation task)\n"
      "- Transformation Rules and Relational Schema\n\n"
      "Your runtime validation MUST be performed at two complementary levels:\n"
      "1. Rule Contribution Correctness: Verify whether each Transformation Rule computes the expected maintenance contributions.\n"
      "2. Changeset Correctness: Verify whether applying the generated changesets to the previous RDF view state "
      "produces exactly the same RDF state obtained by complete rematerialization.\n\n"
      "Produce a comprehensive validation report outlining compliance status across both levels."
   ),
   expected_output="""
A structured Runtime Validation Report in Markdown format (.md).

The output MUST contain exclusively the Markdown report structure, without any extra conversational text or footnotes outside of it.

The report must follow this exact structure:

# Runtime Validation and Oracle Comparison Report

## 1. Executive Validation Summary
- **Execution Status**: `PASSED` (All Tests Verified) or `FAILED` (Discrepancies Detected).
- **Oracle Comparison Benchmark**: Summary of full recomputation vs. incremental output alignment.

## 2. Level 1: Rule Contribution Correctness
- **Evaluation Criteria**: Verification of whether each individual Transformation Rule computes its expected maintenance contributions.
- **Results Breakdown**: Detailed analysis per rule ($\psi$), checking contribution accuracy across test scenarios.

## 3. Level 2: Changeset Correctness
- **Evaluation Criteria**: Verification of whether applying generated changesets to the previous RDF view state produces precisely the identical RDF state obtained by complete rematerialization.
- **State Equivalence Check**: Verification of graph isomorphism and exact triple/quad matching ($\text{State}_{prev} + \Delta = \text{State}_{rematerialized}$).

## 4. Discrepancies & Execution Logs
*(Included only if failures are detected)*
- Detailed error logs, mismatched contributions, or state divergence points requiring repair.
""",
   agent=trigger_validation_repair_agent, 
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/runtime_validation_report_{date_now}.md"
)









### ==========================================
### TASKS 3 | STAGE 3
### ==========================================
automatic_diagnosis_repair_task = Task(
   description=(
      "Analyze execution logs whenever discrepancies are detected during runtime validation, "
      "identify the likely source of errors, and propose targeted corrections to the trigger implementation.\n\n"
      "Input Context Required:\n"
      "- Runtime Validation Execution Logs and Discrepancy Reports\n"
      "- Generated PostgreSQL AFTER Triggers\n"
      "- Transformation Rules and Relational Schema\n\n"
      "Your task MUST execute the following steps:\n"
      "1. Analyze execution logs to pinpoint exact points of state divergence or contribution mismatch.\n"
      "2. Perform root cause diagnosis to identify whether the error stems from changeset computations ($A^-$, $A^+$, $S2$, $\Delta^+$), "
      "relational join paths, or transition table usage.\n"
      "3. Propose targeted, precise corrections to the trigger implementation.\n"
      "4. Iteratively revalidate the corrected code until all correctness criteria are fully satisfied."
   ),
   expected_output="""
A structured Automatic Diagnosis and Repair Report in Markdown format (.md).

The output MUST contain exclusively the Markdown report structure, without any extra conversational text or footnotes outside of it.

The report must follow this exact structure:

# Automatic Diagnosis and Repair Report

## 1. Discrepancy Summary & Log Analysis
- **Execution Status**: Initial failure detected during runtime validation.
- **Log Analysis Overview**: Summary of anomalies, missing/extra tuples, or changeset state divergences found in execution logs.

## 2. Root Cause Diagnosis
- **Identified Source of Error**: Precise location and logical fault within the trigger implementation or maintenance component (e.g., $A^-$, $A^+$, $S2$, or $\Delta^+$ calculation).
- **Rule Association**: Specific Transformation Rule ($\psi$) responsible for the runtime divergence.

## 3. Targeted Code Corrections
- **Proposed SQL/PL-pgSQL Fixes**: Description and code diff/snippets of the targeted corrections applied to the trigger implementation.

## 4. Revalidation Status
- **Final Verification Result**: `PASSED` (All correctness criteria satisfied after repair) or `PENDING FURTHER REPAIR`.
- **Final Corrected Code**: The updated, fully revalidated PostgreSQL AFTER trigger implementation.
""",
   agent=trigger_validation_repair_agent,  # The validation and repair specialist agent
   output_file="automatic_repair_report.md"  # Output Markdown file path
)







### ==========================================
### TEAMS
### ==========================================
trigger_validation_repair_team_1 = Crew(
   agents=[
      trigger_validation_repair_agent,
   ],
   tasks=[
      test_generation_task,
   ],
   process='sequential'
)


trigger_validation_repair_team_2 = Crew(
   agents=[
      trigger_validation_repair_agent,
   ],
   tasks=[
      runtime_validation_task,
   ],
   process='sequential'
)


trigger_validation_repair_team_3 = Crew(
   agents=[
      trigger_validation_repair_agent,
   ],
   tasks=[
      automatic_diagnosis_repair_task,
   ],
   process='sequential'
)