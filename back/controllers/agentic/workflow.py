from crewai import Crew
from .agents import generic_answer_agent
from .agents import answer_task

#################################
### TRANSFORMATION RULES TEAM
#################################


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