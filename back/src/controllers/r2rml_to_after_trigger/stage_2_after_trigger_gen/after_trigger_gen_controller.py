import json
from pathlib import Path
from datetime import datetime
from src.utils import console_log, read_txt_file, write_json_after_trigger_output_file
from src.constants import TEXTS
from .after_trigger_gen_agentic import after_trigger_gen_team

console = lambda x: console_log("RDB2RDF CONTROLLER", x)
parent_folders = "../../../"
parent_path = Path(__file__).parent / "../../../"
# outputs
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")




# Task 1 / Stage 2
async def plan_after_trigger() -> str:
   print(console('plan_after_trigger()'))
   
   generated_tr_file = parent_path /  f"{TEXTS.GENERATED_DATA_FOLDER}/transformation_rules.md"
   rdb_schema_file   = parent_path / "temp/mbz_schema_short.sql"
   
   generated_tr_content = read_txt_file(generated_tr_file)
   rdb_schema_content  = read_txt_file(rdb_schema_file)

   inputs = {
      'transformation_rules':  generated_tr_content,
      'rdb_schema':            rdb_schema_content,
   }

   answer = after_trigger_gen_team.kickoff(inputs)

   if answer:
      return answer
   else:
      return {'message': 'Fail!!'}





# Task 2 / Stage 2
# Essa task deverisa seu divida em duas
async def synthesizes_verifies_trigger() -> str:
   print(console('synthesizes_verifies_trigger()'))
   
   trigger_execution_plan_file = parent_path /  f"{TEXTS.GENERATED_DATA_FOLDER}/trigger_execution_plan.md"
   generated_tr_file           = parent_path /  f"{TEXTS.GENERATED_DATA_FOLDER}/transformation_rules.md"
   
   trigger_execution_plan_content = read_txt_file(trigger_execution_plan_file)
   generated_tr_content           = read_txt_file(generated_tr_file)

   inputs = {
      'trigger_execution_plan': trigger_execution_plan_content,
      'transformation_rules':   generated_tr_content,
   }

   answer = after_trigger_gen_team.kickoff(inputs)

   if answer:
      return answer
   else:
      return {'message': 'Fail!!'}