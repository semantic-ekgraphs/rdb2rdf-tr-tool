import json
from pathlib import Path
from datetime import datetime
from utils import console_log, read_txt_file, write_json_after_trigger_output_file
from .after_trigger_gen_agentic import after_trigger_gen_team

console = lambda x: console_log("RDB2RDF CONTROLLER", x)
parent_folders = "../../../"
# outputs
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")




# Task 1 / Stage 2
async def transform_transformation_rules_into_after_trigger() -> str:
   print(console('transform_transformation_rules_into_after_trigger()'))

   
   generated_tr_file         = Path(__file__).parent / parent_folders / "temp/transformation_rules_2026-10-02_15-22-32.md"
   generated_tr_content = read_txt_file(generated_tr_file)

   # These keys must be the same in input of the Task
   inputs = {
      'transformation_rules':  generated_tr_content
   }

   answer = after_trigger_gen_team.kickoff(inputs)

   if answer:
      return answer
   else:
      return {'message': 'Fail!!'}