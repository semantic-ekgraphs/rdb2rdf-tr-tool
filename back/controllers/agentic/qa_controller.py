from pathlib import Path
from constants import TXT_TEN_DASHES
from uuid import uuid4
from utils import filter_by_language, console_log, print_json_idented, info
from .workflow import answer_team

console = lambda x: console_log("AGENTIC CONTROLLER", x)
tr_patterns_file = Path(__file__).parent / "../../knowledge/tr_patterns.txt"


async def answer_tr_patterns_question(user_question:str) -> str:
   print(console('answer_a_user_question()'))
   with open(tr_patterns_file, "r", encoding="utf-8") as file:
      tr_patterns_content = file.read()
      inputs = {
         'user_question': user_question,
         'tr_patterns_content': tr_patterns_content
      }
      answer = answer_team.kickoff(inputs)
      return answer