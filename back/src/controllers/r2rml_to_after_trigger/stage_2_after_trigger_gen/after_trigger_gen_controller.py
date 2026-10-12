import json
from pathlib import Path
from datetime import datetime
from src.utils import console_log, read_txt_file, write_json_after_trigger_output_file
from src.utils import get_path_of_generated_file, get_path_of_file_from_temp
from src.constants import TEXTS
from .after_trigger_gen_agentic import after_trigger_gen_team_1, after_trigger_gen_team_2, after_trigger_gen_team_3

console = lambda x: console_log("RDB2RDF CONTROLLER", x)
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")




### ==========================================
### TASK 1 | STAGE 2
### ==========================================
async def plan_after_trigger() -> str:
   print(console('plan_after_trigger()'))
   
   generated_tr_file = get_path_of_generated_file("transformation_rules.md")
   rdb_schema_file   = get_path_of_file_from_temp("mbz_schema_short.sql")
   
   generated_tr_content = read_txt_file(generated_tr_file)
   rdb_schema_content  = read_txt_file(rdb_schema_file)

   inputs = {
      'transformation_rules':  generated_tr_content,
      'rdb_schema':            rdb_schema_content,
   }

   answer = after_trigger_gen_team_1.kickoff(inputs)

   if answer:
      return answer
   else:
      return {'message': 'Fail!!'}





### ==========================================
### TASK 2 | STAGE 2
### ==========================================
# Essa task deveria ser divida em duas
async def synthesizes_verifies_trigger() -> str:
   print(console('synthesizes_verifies_trigger()'))
   
   trigger_execution_plan_file = get_path_of_generated_file("trigger_execution_plan.md")
   generated_tr_file           = get_path_of_generated_file("transformation_rules.md")
   
   trigger_execution_plan_content = read_txt_file(trigger_execution_plan_file)
   generated_tr_content           = read_txt_file(generated_tr_file)

   inputs = {
      'trigger_execution_plan': trigger_execution_plan_content,
      'transformation_rules':   generated_tr_content,
   }

   answer = after_trigger_gen_team_2.kickoff(inputs)

   if answer:
      return answer
   else:
      return {'message': 'Fail!!'}






### ==========================================
### TASK 3 | STAGE 2
### ==========================================
async def trigger_static_verification() -> str:
   print(console('trigger_static_verification()'))
   
   postgresql_after_triggers_file    = get_path_of_generated_file("postgresql_after_triggers.md")
   postgresql_after_triggers_content = read_txt_file(postgresql_after_triggers_file)

   inputs = {
      'postgresql_after_triggers': postgresql_after_triggers_content,
   }

   answer = after_trigger_gen_team_3.kickoff(inputs)

   if answer:
      return answer
   else:
      return {'message': 'Fail!!'}