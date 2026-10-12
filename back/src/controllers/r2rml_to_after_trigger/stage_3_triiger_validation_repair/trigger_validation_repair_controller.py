import json
from pathlib import Path
from datetime import datetime
from src.utils import console_log, read_txt_file, write_json_after_trigger_output_file
from src.utils import get_path_of_generated_file, get_path_of_file_from_temp
from src.constants import TEXTS
from .trigger_validation_repair_agentic import trigger_validation_repair_team_1, trigger_validation_repair_team_3

console = lambda x: console_log("RDB2RDF CONTROLLER", x)
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")




### ==========================================
### TASK 1 | STAGE 3
### ==========================================
async def test_generation() -> str:
   print(console('test_generation()'))
   
   rdb_schema_file   = get_path_of_file_from_temp("mbz_schema_short.sql")
   generated_tr_file = get_path_of_generated_file("transformation_rules.md")
   trigger_execution_plan_file = get_path_of_generated_file("trigger_execution_plan.md")
   postgresql_after_triggers_file    = get_path_of_generated_file("postgresql_after_triggers.md")
   
   rdb_schema_content  = read_txt_file(rdb_schema_file)
   generated_tr_content = read_txt_file(generated_tr_file)
   trigger_execution_plan_content = read_txt_file(trigger_execution_plan_file)
   postgresql_after_triggers_content = read_txt_file(postgresql_after_triggers_file)

   inputs = {
      'rdb_schema':                rdb_schema_content,
      'transformation_rules':      generated_tr_content,
      'trigger_execution_plan':    trigger_execution_plan_content,
      'postgresql_after_triggers': postgresql_after_triggers_content,
   }

   answer = trigger_validation_repair_team_1.kickoff(inputs)

   if answer:
      return answer
   else:
      return {'message': 'Fail!!'}





### ==========================================
### TASK 2 | STAGE 3
### ==========================================
async def runtime_validation() -> str:
   print(console('runtime_validation()'))
   
   # Aqui entra em cena o Worker do Narciso.
   answer = "Narciso.Worker(*)"
   
   return answer if answer else {'message': 'Fail!!'}





### ==========================================
### TASK 3 | STAGE 3
### ==========================================
async def automatic_diagnosis_repair():
   print(console('automatic_diagnosis_repair()'))

   # Aqui entra os logs do Narciso.Worker()
   inputs = {}
   answer = trigger_validation_repair_team_3.kickoff(inputs)
   
   return answer if answer else {'message': 'Fail!!'}