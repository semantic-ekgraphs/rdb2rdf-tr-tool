from constants import TXT_TEN_DASHES
from uuid import uuid4
from pathlib import Path
from utils import filter_by_language, console_log, print_json_idented, info
from .workflow import transformation_rules_team

console = lambda x: console_log("AGENTIC CONTROLLER", x)
path_temp_r2rml = Path(__file__).parent / "../../temp/mbz_r2rml.ttl"
path_temp_parsing = Path(__file__).parent / "../../temp/parsing.md"
path_temp_parsing_json = Path(__file__).parent / "../../temp/parsing.json"

async def transform_r2rml_to_transformation_rules() -> str:
   print(console('transform_rdf_to_rdf()'))
   with open(path_temp_r2rml, "r") as file:
      r2rml_content = file.read()
      inputs = {
         'r2rml_mapping': r2rml_content,
      }
      answer = transformation_rules_team.kickoff(inputs)
      with open(path_temp_parsing_json, "w", encoding="utf-8") as file:
         file.write(answer.raw)
         return answer
      # return "transform_r2rml_to_transformation_rules"