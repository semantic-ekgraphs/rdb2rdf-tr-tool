from constants import TXT_TEN_DASHES
from uuid import uuid4
from pathlib import Path
from utils import filter_by_language, console_log, print_json_idented, info
from .workflow import transformation_rules_team

console = lambda x: console_log("AGENTIC CONTROLLER", x)
# inputs
r2rml_file =        Path(__file__).parent / "../../temp/mbz_r2rml.ttl"
schema_sql_file =   Path(__file__).parent / "../../temp/mbz_schema.sql"
tr_patterns_file =  Path(__file__).parent / "../../knowledge/tr_patterns.txt"
# outputs
parsing_md_file =   Path(__file__).parent / "../../temp/parsing.md"
parsing_json_file = Path(__file__).parent / "../../temp/parsing.json"

async def transform_r2rml_to_transformation_rules() -> str:
   print(console('transform_rdf_to_rdf()'))

   ### PASS THE R2RML FILE TO THE INPUT AS CONTEXT
   with open(r2rml_file, "r") as file:
      r2rml_content = file.read()
      ### PASS THE SCHEMA FILE TO THE INPUT AS CONTEXT
      with open(schema_sql_file, "r") as file2:
         schema_sql_content = file2.read()
         ### PASS THE TR PATTERNS FILE TO THE INPUT AS CONTEXT
         with open(tr_patterns_file, "r", encoding="utf-8") as file3:
            tr_patterns_content = file3.read()
            inputs = {
               'r2rml_mapping': r2rml_content, # This key must be the same in input_description in the Task
               'rdb_schema':    schema_sql_content,
               'tr_patterns':   tr_patterns_content
            }

            ### CALL THE CREW
            answer = transformation_rules_team.kickoff(inputs)

            # print(f'answer: {answer}')

            ### SAVE THE ANSWER AS JSON IN THE \TEMP FOLDER 
            with open(parsing_json_file, "w", encoding="utf-8") as file:
               file.write(answer.raw)
               # file.write(answer.model_dump())
               return answer