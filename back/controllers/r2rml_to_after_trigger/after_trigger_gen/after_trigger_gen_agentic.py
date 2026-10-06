from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_4o_mini_openai, gpt_6_luna_openai
# from knowledge import object_preserving_definition_knowledge_source
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Estou seguindo o documento do artigo: 
# https://docs.google.com/document/d/1FU7M8qcHQhQvPcYbidvnTS28UfEBj5H_lqayQ_pAc-s/edit?tab=t.0



### ==========================================
### AGENTS
### ==========================================

# Stage 2
agent_after_trigger_generation = Agent(
   role="Principal Knowledge Engineer and Formal Semantic Web Architect",
   goal=(
      "The objective of this stage is automatically synthesizes PostgreSQL AFTER triggers "
      "from the Transformation Rules defined in Stage 1."
   ),
   backstory=(
      "This stage automatically synthesizes PostgreSQL AFTER triggers from the "
      "Transformation Rules defined in Stage 1."
   ),
   verbose=True,
   memory=False,
   llm=gpt_6_luna_openai,
)




### ==========================================
### TASKS
### ==========================================

# Tasks 1 | Stage 2
task_trigger_planning = Task(
   description=(
      "Rather than immediately generating SQL code, the planning agent first determines "
      "the maintenance strategy required for each database relation."
      "For every updated relation (R), the agent computes the set (Relev(R)) of relevant Transformation Rules, "
      "classifies each rule as pivot-relevant or relation-relevant, "
      "determines whether multiple occurrences of the updated relation exist in the relational path, "
      "and identifies which maintenance components must be computed, including affected pivot tuples ((A^{-}) and (A^{+})), post-update contributions ((S2)), and deletion and insertion changesets."
      "Inputs:"
      "<Transformation Rules>{transformation_rules}</Transformation Rules>"
   ),
   expected_output=(
      "The output of this step is a declarative maintenance plan that guides trigger synthesis."
      "Trigger execution plan for each relation."
   ),
   output_file=f"temp/after_trigger_planning_{date_now}.md",
   agent=agent_after_trigger_generation
)

# Tasks 2 | Stage 2
task_trigger_synthesis_static_verification = Task(
   description=(
      "Based on the execution plan, a trigger synthesis agent generates PostgreSQL AFTER triggers "
      "implementing the incremental maintenance algorithm described in [XX]. "
      "The generated triggers use statement-level transition tables, compute the required maintenance structures, "
      "and populate the asynchronous maintenance queue." 
      "After generation, an independent critic agent performs static verification. "
      "Instead of executing the code, it checks whether the generated implementation conforms to the "
      "formal specification. The validation includes verification of:"
      "- correct identification of (Relev(R));"
      "- correct computation of (A^{-}), (A^{+}), (S2), (\Delta^{+}{pivot}), (\Delta^{+}{rel}), and (\Delta^{+});"
      "- correct URI construction functions and named graphs;"
      "- correct relational joins and predicates;"
      "- proper use of PostgreSQL transition tables; and"
      "- absence of hallucinated attributes, predicates, relations, or transformation rules."
      
      "When inconsistencies are detected, the synthesis agent receives structured feedback and regenerates only the affected components."
      
      "Input:"
      "<Transformation Rules>{transformation_rules}</Transformation Rules>"
   ),
   expected_output="Statistically verified PostgreSQL AFTER triggers.",
   context=[task_trigger_planning],
   agent=agent_after_trigger_generation
)



### ==========================================
### TEAM
### ==========================================
from crewai import Crew
after_trigger_gen_team = Crew(
   agents=[agent_after_trigger_generation],
   tasks=[
      task_trigger_planning
   ],
   process='sequential',
   # knowledge_sources=[transformation_rules_patterns], # Enable knowledge by adding the sources here
)