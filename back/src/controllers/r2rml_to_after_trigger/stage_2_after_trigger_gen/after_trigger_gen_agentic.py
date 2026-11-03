from datetime import datetime
from crewai import Agent, Task, Crew
from src.llms import gpt_4o_mini_openai, gpt_6_luna_openai, local_GEMMA
from src.utils import get_prompt_of_a_pydantic_model, get_prompt_of_columns
from src.constants import TEXTS
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# from src.knowledge.sources_of_knowledge import knowledge_of_formal_entity_preserving_specification 
# from src.knowledge.sources_of_knowledge import knowledge_source_transformation_rule_patterns_v2
# from src.knowledge.sources_of_knowledge import knowledge_source_of_maintanance_queue_infrastructure
# from src.knowledge.sources_of_knowledge import knowledge_source_of_algorithm_1
# from src.knowledge.sources_of_knowledge import knowledge_source_of_algorithm_2
# from src.knowledge.sources_of_knowledge import knowledge_of_rdb2rdf_views
from src.knowledge.sources_of_knowledge import knowledge_stage_2
from src.knowledge.sources_of_knowledge import instruction_consult_knowledge_source

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
      
      f"{instruction_consult_knowledge_source(('RDB2RDF Views, Algorithm 2: Function Compute_Changeset_R, Algorithm 1: Compute_Delta_R, and Infrastructure for the Maintanance Queue'))}"
   ),
   backstory=(
      "You are an elite database engineer and formal methods expert specializing in "
      "relational-to-RDF incremental maintenance architectures. You approach trigger "
      "generation not through ad-hoc coding, but as a rigorous, two-stage compiler-like "
      "process: Planning and Synthesis. In the planning phase, you analyze the relational "
      "schema alongside Transformation Rules to map out exact tuple lifecycle "
      "dependencies and isolate rule relevance (Relev(R)). During synthesis, you translate "
      "these declarative execution plans into highly efficient PostgreSQL AFTER triggers "
      "that execute at the statement level, utilizing OLD TABLE and NEW TABLE transition "
      "tables. You are hyper-vigilant against hallucinated SQL elements, ensuring that "
      "all URI construction functions, named graphs, relational joins, and changeset "
      "deltas (A-, A+, S2, Delta+) match the formal specification with mathematical precision."
   ),
   knowledge_sources=[knowledge_stage_2],
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
   knowledge_sources=[knowledge_stage_2],
   verbose=True,
   memory=False,
   llm=gpt_6_luna_openai
)


### ==========================================
### TASK 1 | STAGE 2
### ==========================================
# provided relational schema and
# "1. Compute the set $Relev(R)$ of all relevant Transformation Rules.\n"
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
      "Analyze the set of Transformation Rules "
      "to determine the incremental maintenance strategy required for each database pivot relation $R$ present in the Transformation Rules "
      "without generating SQL code at this stage.\n\n"
      "For each pivot relation $R$ in Final Validated Set of Transformation Rules on <Transformation Rules>, you must do:\n"
       f"{get_prompt_of_a_pydantic_model(TriggerPlanRow)}\n\n"
      "Inputs:"
      "<Transformation Rules>{transformation_rules}</Transformation Rules>\n\n"
      "<Relational Schema>{rdb_schema}</Relational Schema>"
   ),
   expected_output=(
      "A structured report in Markdown format (.md), with the title 'Trigger Planning', containing the declarative trigger execution plan for each analyzed relation R. "
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
vania_description="""Specification-to-code compilation contract for an LLM.
Based on the provided trigger execution plan and Transformation Rules, 
generates the corresponding PostgreSQL statement-level AFTER triggers and PL/pgSQL functions for updates on a relation $R$, 
implementing the incremental maintenance Algorithm 2: Function Compute_Changeset_$R$ for the Asynchronous Architecture.
Input Context:
<trigger execution plan>{trigger_execution_plan}\n</trigger execution plan>
<Transformation Rules>{transformation_rules}\n</Transformation Rules>
Storing the Materialized RDF view 
- GraphDB stores the materialized RDF view as a dataset of quads:
(s, p, o, g), where g = URI(Ψ)
Each transformation rule Ψ corresponds to a named graph:
GRAPH <URI(Ψ)>
The RDF dataset is accessible via SPARQL endpoint:
The pre-update RDF state W₀ MUST be obtained from GraphDB via SPARQL 
Transformation Rule URI and Named Graph

Each Transformation Rule Ψ has a certified URI provided in the
`Rule URI` column of the consolidated Transformation Rules table.

The Trigger Compilation Agent MUST read this URI exactly as
provided. It MUST NOT construct, infer, normalize, modify, or
replace the Transformation Rule URI.

For every rule Ψ, the supplied Rule URI MUST be used consistently as:
1. the named-graph identifier of Ψ;
2. the graph component g of every quad (s, p, o, g) generated by Ψ;
3. the value of rdf_rule_contribution.rule_graph_uri.

If the Rule URI is missing, empty, malformed, or duplicated, the
compiler MUST report an input-validation error for the rule and MUST NOT generate a replacement URI.

Transformation Rules: 

-  The LinkedBrainz RDF View  is defined by a set of Entity-preserving Transformation Rules (TRs) in file: musicbrainz-transformation-rules-consolidadas

The file musicbrainz-transformation-rules-consolidadas is the single source of truth for the definition of the LinkedBrainz RDF View. Therefore it is the sole authoritative semantic specification of transformation rules for this compilation task.
Use only the Transformation Rules (TRs) explicitly defined in musicbrainz-transformation-rules-consolidadas.
Do not use, adapt, extrapolate, or complete rules from examples appearing in papers, documentation, conversations, or previous outputs.
Do not assume the existence of additional rules that are not present in musicbrainz-transformation-rules-consolidadas.
If a rule is not explicitly defined in musicbrainz-transformation-rules-consolidadas, treat it as non-existent.
All maintenance computations must be derived exclusively from the TRs in musicbrainz-transformation-rules-consolidadas.
Do not consult, reconstruct, correct, or complete any transformation rule from R2RML, ontology files, papers, examples, or prior knowledge.
The examples shown in the paper are provided only for explanatory purposes and do not represent the complete LinkedBrainz RDF View specification. Therefore, they must never be used as the basis for maintenance computations or code generation

TASK
Generate the PostgreSQL statement-level AFTER trigger for updates on a relation R. The  function Compute_Changeset_R  is responsible for computing RDF incremental maintenance information for updates on a relation R. 
The generated trigger function MUST implement Algorithm 2 in 2027_EDBT
Algorithm 1 MUST be used only as the formal basis for the definitions of relevance, affected pivot tuples, S1, S2, and the per-rule insertion and deletion contributions.
The trigger MUST NOT implement the operations assigned by Algorithm 2 to the asynchronous worker.
The After Trigger has the form:
CREATE TRIGGER ...
AFTER UPDATE ON ...
REFERENCING
  OLD TABLE AS deleted_R
  NEW TABLE AS inserted_R
FOR EACH STATEMENT
EXECUTE FUNCTION ...;

Asynchronous architecture for incremental maintenance of a materialized RDB2RDF view.

The incremental maintenance of a materialized RDB2RDF view. will be executed in a PostgreSQL trigger-based architecture using transition tables and an asynchronous RDF maintenance queue as described in  [ Infrastructure for the Maintenance Queue]. 
The asynchronous architecture is composed of:
1. PostgreSQL statement-level AFTER triggers;
2. A maintenance queue (rdf_maintenance_queue);
3. An external worker that processes events and interacts with GraphDB.

The AFTER trigger operates exclusively on PostgreSQL data.
For each relevant rule Ψ, it computes and publishes:
- A−[Ψ](u);
- A+[Ψ](u);
- S2[Ψ](u);
- Δ+[Ψ](u).

The external asynchronous worker:
- retrieves S1[Ψ](u) and Δ−pivot[Ψ](u) from W0 in GraphDB;
- computes the final deletion contribution Δ−[Ψ](u);
- applies Δ−[Ψ](u) and Δ+[Ψ](u) to GraphDB.

No SPARQL or GraphDB operation is part of the generated trigger.
INPUT ASSUMPTIONS
Assume:
u = (D, I) is an update over relation R
D = deleted_R
I = inserted_R
where:
deleted_R is the transition table containing deleted/pre-update tuples
inserted_R is the transition table containing inserted/post-update tuples
============

Relevance of Transformation Rules: 
Before generating the function Compute_Changeset_R, the LLM MUST first identify the set of transformation rules relevant to updates on relation R, according to the formal relevance definitions provided in 2027_EDBT
– Ψ is pivot-relevant iff  pivot(Ψ) = R
– Ψ is relation-relevant to updates on relation R iff R occurs in the body of Ψ in an occurrence other than the pivot occurrence. Equivalently, R participates in the relational path of Ψ as an intermediate or target relation, rather than as the initial relation corresponding to pivot(Ψ).
Formally, a transformation rule Ψ is relevant to relation R iff:  Ψ is pivot-relevant or Ψ is relation-relevant.
A transformation rule may be:
- pivot-relevant only
- relation-relevant only
- both pivot-relevant and relation-relevant.
============================== 
Function Compute_Changeset_R 
The function Compute_Changeset_R consists of two main STEPS as follows (see Algorithm 2 in 2027_EDBT)
For each transformation rule: Ψ relevant to  R the function MUST compute:
Step 1: Incremental Maintenance Computation
Δ+pivot[Ψ](u) := ∅
Δ+rel[Ψ](u) := ∅
1. If Ψ is pivot-relevant compute: 
Δ+pivot[Ψ](u):  consists of the quads generated by applying Ψ to inserted pivot tuple, evaluated over the post-update database state 𝜎1
2. if  Ψ is relation-relevant,  compute:
the affected tuples for deletion:
 𝐴Ψ−(u): the set of pivot tuples in the relevant relation that are  affected by the deleted tuple in R
the affected tuples for insertion: 
𝐴Ψ+(u):  the set of pivot tuples in the relevant relation that are  affected by the inserted tuple in R. 
the post-update RDF contributions: 
𝑆2 [Ψ]: all quads created by Ψ from tuples in 𝐴Ψ-(u)  in the post-update database state
the relation-relevant insertion changeset: 
Δ+rel[Ψ](u): The the set of quads generated by Ψ for  tuples in 𝐴Ψ+, in the post-update state
3. Compute the insertion changeset  Δ+[Ψ](u) = Δ+pivot[Ψ](u) ∪ Δ+rel[Ψ](u)
The two relevance conditions are independent and MUST be evaluated separately. If both conditions hold, both computations MUST be executed.
The computations MUST follow the formal semantics and Definitions in 2027_EDBT.
- S2[Ψ](u) is the post-update RDF contribution used by the asynchronous worker to compute:
- Δ−rel[Ψ](u) = S1[Ψ](u) \ S2[Ψ](u) where S1[Ψ](u) is obtained from W0.
The rule contributions of each rule should be stored in JSON format, and should follow the templates presented in   [ Infrastructure for the Maintenance Queue] :  
CTR → class_quad_template
DTR → datatype_quad_template
OTR → object_quad_template
STEP 2: Insertion of events in the Maintenance Queue 
The computed maintenance information  MUST insert in infrastructure with 2 tables as described in  [ Infrastructure for the Maintenance Queue] .

– rdf_maintenance_queue ( 1 row for event) 

– rdf_rule_contribution:  ( 1 row for event by rule Ψ) 
 
The tables have the following schema and semantics. 
Queue Table: rdf_maintenance_queue
Each row represents one statement-level relational update event over a source relation.
The queue preserves the commit order of maintenance events and serves as the communication interface between:
PostgreSQL AFTER triggers
the asynchronous RDF maintenance worker
Schema of  rdf_maintenance_queue 

CREATE TABLE rdf_maintenance_queue (
    event_id        BIGSERIAL PRIMARY KEY,
    relation_name   TEXT NOT NULL,
    operation_type  TEXT NOT NULL,
    deleted_tuples  JSONB NOT NULL,
    inserted_tuples JSONB NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMP NOT NULL DEFAULT now(),
    processed_at    TIMESTAMP,
    error_message   TEXT
);
Schema of rdf_rule_contribution

CREATE TABLE rdf_rule_contribution (
    event_id          BIGINT NOT NULL REFERENCES rdf_maintenance_queue(event_id),
    rule_id           TEXT NOT NULL,
    rule_graph_uri    TEXT NOT NULL,
    relevance_type    TEXT NOT NULL,
    pivot_relation    TEXT NOT NULL,
    path              JSONB NOT NULL,
    rule_contribution JSONB NOT NULL,
    PRIMARY KEY (event_id, rule_id)
);
Each row in rdf_rule_contribution represents the maintenance information computed for a single transformation rule.
The rule contributions of each rule should be stored in JSON format, and should follow the templates presented in   [ Infrastructure for the Maintenance Queue] :  
CTR → class_quad_template
DTR ( Local-DTR or Path-DTR)  → datatype_quad_template
OTR → object_quad_template

The rules computes only the information  required by its template (CTR, DTR or OTR).   
Rule contribution for a CTR:  DeltaPlusPivot and DeltaPlus 
Rule contribution for a OTR: A−, A+, DeltaPlusPivot, S2, DeltaPlusRel and DeltaPlus
Rule contribution for a DTR: A−, A+, DeltaPlusPivot, S2, DeltaPlusRel and DeltaPlus
The JSON format MUST follow what is defined in the template. Do not change the structure. 
The rule contribution MUST preserve the semantics and provenance of the corresponding transformation rule Ψ, including its associated named graph:
"""

vania_output="""OUTPUT FORMAT
A) Analytical Table (MANDATORY)
Provide one row per Ψ ∈ Relev(R):
| Ψ | pivot(Ψ) | path(Ψ) | Type (pivot/relation) | Affected tuples | Justification |
Requirements:
Use the formal definition of relevance
Clearly explain how R appears in path(Ψ)
For each relation-relevant rule, explain where R occurs in the body of Ψ and identify its occurrence in path(Ψ).
For each pivot-relevant-only rule, state that pivot(Ψ) = R. In this case, R does not need to occur as a non-pivot relation in path(Ψ).
 If Ψ is both pivot-relevant and relation-relevant, explain the pivot occurrence and the non-pivot occurrence separately
The relevance_type field MUST contain exactly one of:
- "pivot"
- "relation"
- "both"
Use "both" when Ψ is simultaneously pivot-relevant and relation-relevant to R.


B) PostgreSQL Function Compute_Changeset_R (MANDATORY)
The function MUST follow the algorithm  2  and definitions in   2027_EDBT.
The function MUST:
Use transition tables:
deleted_R
inserted_R
Use SQL to compute:
the affected tuples for deletion A−[Ψ ](u), 
the affected tuples for insertion A+[Ψ ](u),
the post-update contribution S2[Ψ](u), which is  published for use by the asynchronous worker in the  computation of Δ−rel[Ψ](u),  and 
the insertion changeset ∆+(u). 
Store the computed information in the maintenance queue (rdf_maintenance_queue).
Represent RDF quads explicitly:
(s, p, o, g)
insert exactly one event row into rdf_maintenance_queue;
obtain the generated event_id;
 insert exactly one row into rdf_rule_contribution for each
   Ψ ∈ Relev(R), linked to that event_id;
return NULL, as required for an AFTER FOR EACH STATEMENT
   trigger function.
Include:
Clear step-by-step comments
Separation of pivot and relation contributions
No redundant operations
No speculative logic

C) PostgreSQL Trigger (MANDATORY)
The AFTER trigger  to be executable in a PostgreSQL trigger-based environment using the proposed architecture. 
Use the queue tables defined in Infrastructure for the Maintenance Queue  to store the output.
"""



renato_description=(
      "Based on the provided trigger execution plan, the Transformation Rules, and <validated metadata>, "
      "generates the corresponding PostgreSQL statement-level AFTER triggers and PL/pgSQL functions for updates on a relation $R$, " 
      "implementing the incremental maintenance Algorithm 2: Function Compute_Changeset_$R$ for the Asynchronous Architecture.\n\n"
      "Input Context:\n"
         "<trigger execution plan>{trigger_execution_plan}\n</trigger execution plan>\n"
         "<Transformation Rules>{transformation_rules}\n</Transformation Rules>\n\n"
         "<validated metadata>{extracted_metadata}</validated metadata>\n\n"
      "The function Compute_Changeset_$R$ is responsible for computing RDF incremental maintenance information for updates on a relation $R$."
      "The generated trigger function MUST implement Algorithm 2, included in the agent knowledge sources.\n"
      "Algorithm 1 MUST be used only as the formal basis for the definitions of relevance, affected pivot tuples, S1, S2, and the per-rule insertion and deletion contributions."
      "The trigger MUST NOT implement the operations assigned by Algorithm 2 to the asynchronous worker."
      "The After Trigger has the form:\n"
      "CREATE TRIGGER ...\n"
      "AFTER UPDATE ON ...\n"
      "REFERENCING\n"
      "  OLD TABLE AS deleted_$R$\n"
      "  NEW TABLE AS inserted_$R$\n"
      "FOR EACH STATEMENT\n"
      "EXECUTE FUNCTION ...;\n\n"

      "The incremental maintenance of a materialized RDB2RDF view will be executed in a PostgreSQL trigger-based architecture using transition tables and an asynchronous RDF maintenance queue as described in 'Infrastructure for the Maintenance Queue'. \n"
      "The asynchronous architecture is composed of:\n"
      "1. PostgreSQL statement-level AFTER triggers;\n"
      "2. A maintenance queue (rdf_maintenance_queue);\n"
      "3. An external worker that processes events and interacts with GraphDB.\n"
      "\n"
      "The AFTER trigger operates exclusively on PostgreSQL data.\n"
      "For each relevant rule Ψ, it computes and publishes:\n"
      "- A−[Ψ](u);\n"
      "- A+[Ψ](u);\n"
      "- S2[Ψ](u);\n"
      "- Δ+[Ψ](u).\n"
      "\n"
      "The external asynchronous worker:\n"
      "- retrieves S1[Ψ](u) and Δ−pivot[Ψ](u) from W0 in GraphDB;\n"
      "- computes the final deletion contribution Δ−[Ψ](u);\n"
      "- applies Δ−[Ψ](u) and Δ+[Ψ](u) to GraphDB.\n"
      "\n"
      "No SPARQL or GraphDB operation is part of the generated trigger.\n"

      "INPUT ASSUMPTIONS\n"
      "Assume:\n"
      " - u = (D, I) is an update over relation R\n"
      " - D = deleted_R\n"
      " - I = inserted_R\n"
      "where:\n"
      " - deleted_$R$ is the transition table containing deleted/pre-update tuples\n"
      " - inserted_$R$ is the transition table containing inserted/post-update tuples\n"

      
      "Your synthesis of AFTER triggers PL/pgSQL must implement the following architectural requirements:\n"
      "1. Utilize statement-level transition tables (`REFERENCING OLD TABLE AS OLD_$R$ NEW TABLE AS NEW_$R$`) "
      "to capture snapshots of update events over relation $R$ ($\Delta^-$ and $\Delta^+$).\n"
      "2. Compute the affected tuples for removal ($A^-[\Psi](u)$).\n"
      "3. Compute the affected tuples for insertion ($A^+[\Psi](u)$).\n"
      "4. Compute the post-update contributions ($S2[\Psi](u)$) for each relevant rule $\Psi$.\n"
      "5. Compute the final insertion ($\Delta^+(u)$) and deletion changesets.\n"
      "6. Construct clean, production-ready SQL statements that populate the asynchronous maintenance queue according 'Infrastructure for the Maintenance Queue'\n"
      "7. The rule contributions of each rule should be stored follow the schema of rdf_maintenance_queue, all complete schema of rdf_rule_contribution table, using the JSON schemas to CTR, DTR and OTR defined in 'Infrastructure for the Maintenance Queue' knowledge sources.\n" \
      
      f"{instruction_consult_knowledge_source(('rdb2rdf views, algorithm 2, algorithm 1, and infrastructure of the maintanance queue'))}"
   )
renato_output="""
A structured PostgreSQL Trigger Implementation Report in Markdown format (.md).

The output MUST contain exclusively the Markdown report structure, without any extra conversational text or footnotes.

The report must follow this exact structure:

# PostgreSQL AFTER Trigger Implementation Report

## 1. Synthesis Overview
- **Target Relation(s)**: List of database relation(s) processed (e.g., Relation R).
- **Architecture Compliance**: Confirmation of statement-level transition table usage (`REFERENCING OLD TABLE / NEW TABLE`) and asynchronous maintenance queue population according 'Infrastructure for the Maintenance Queue'.

## 4. Generated PostgreSQL AFTER Trigger Code
- Complete, syntactically correct SQL/PL-pgSQL code blocks for the statement-level AFTER triggers and associated functions.
"""


trigger_synthesis_task = Task(
   description=renato_description + f"{instruction_consult_knowledge_source(('rdb2rdf views, algorithm 2, algorithm 1, and infrastructure of the maintanance queue'))}" +
   """FiNAL REQUIREMENTS
The function Compute Changeset_R MUST insert the computed event and rule-level contributions into rdf_maintenance_queue and rdf_rule_contribution, respectively

Because it is an AFTER FOR EACH STATEMENT trigger function,
it MUST be declared RETURNS trigger and terminate with
RETURN NULL. The trigger return value is not used; the
function output consists of the rows inserted into the
maintenance tables.

The generated solution MUST:
- be fully executable
""", 
   expected_output=renato_output,
   output_file=f"{TEXTS.GENERATED_DATA_FOLDER}/stage2/postgresql_after_triggers_{date_now}.md",
   agent=trigger_generation_agent
)


# ## 2. Trigger Execution & Component Computation
# Detailed breakdown of the implemented logic for the generated SQL code:
# - **Snapshot Capture**: Description of how transition tables ($\Delta^-$ and $\Delta^+$) capture update event snapshots.
# - **Affected Deletion Tuples ($A^-[\Psi](u)$)**: Implementation logic isolating affected pivot tuples for deletion.
# - **Affected Insertion Tuples ($A^+[\Psi](u)$)**: Implementation logic isolating affected pivot tuples for insertion.
# - **Post-Update Contributions ($S2[\Psi](u)$)**: Implementation logic computing post-update RDF states for rule $\Psi$.
# - **Changesets Computation ($\Delta^+(u)$ and $\Delta^-(u)$)**: Final aggregation logic for insertion and deletion changesets.


# ##3. Asynchronous Maintenance Queue Integration
# - Explanation of how computed components are serialized and loaded into the maintenance queue infrastructure.

# "8. The named graph is a URI resulting concatening 'http://example.com/resource/tr/' and respective <transformation_rule_id>"

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


after_trigger_gen_team_1 = Crew(
   agents=[
      trigger_generation_agent,
   ],
   tasks=[
      task_trigger_planning,
   ],
   process='sequential'
)


after_trigger_gen_team_2 = Crew(
   agents=[
      trigger_generation_agent,
   ],
   tasks=[
      trigger_synthesis_task,
   ],
   process='sequential'
)


after_trigger_gen_team_3 = Crew(
   agents=[
      ivm_critic_agent,
   ],
   tasks=[
      trigger_static_verification_task,
   ],
   process='sequential'
)