from crewai import Crew
from .agents import generic_answer_agent, r2rml_to_tr_agent
from .agents import answer_task, task_parsing_and_pivoting

#################################
### TRANSFORMATION RULES TEAM
#################################
transformation_rules_team = Crew(
	agents=[
      r2rml_to_tr_agent
   ],
   tasks=[
      task_parsing_and_pivoting
   ],
	process='sequential'
)

#################################
### TRIGGERS TEAM
#################################


#################################
### ANSWER TEAM
#################################
answer_team = Crew(
	agents=[
      generic_answer_agent
   ],
   tasks=[
      answer_task
   ],
	process='sequential'
)