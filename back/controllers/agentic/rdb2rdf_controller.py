from constants import TXT_TEN_DASHES
from uuid import uuid4
from pathlib import Path
from utils import filter_by_language, console_log, print_json_idented, info
from .workflow import transformation_rules_team

console = lambda x: console_log("AGENTIC CONTROLLER", x)
path_temp = Path(__file__).parent / "../../temp/mbz_r2rml.ttl"

async def transform_rdf_to_rdf() -> str:
   print(console('transform_rdf_to_rdf()'))
   with open(path_temp, "r") as file:
      content = file.read()
      inputs = {
         'r2rml_mapping': content,
      }
      answer = transformation_rules_team.kickoff(inputs)
      return answer