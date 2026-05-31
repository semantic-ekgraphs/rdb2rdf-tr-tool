from pathlib import Path
from constants import TXT_TEN_DASHES
from uuid import uuid4
from utils import filter_by_language, console_log, print_json_idented, info
from .workflow import answer_team

console = lambda x: console_log("AGENTIC CONTROLLER", x)
path_knowledge_tr_patterns = Path(__file__).parent / "../../knowledge/tr_patterns.txt"


async def answer_tr_patterns_question(user_question:str) -> str:
   print(console('answer_a_user_question()'))
   with open(path_knowledge_tr_patterns, "r", encoding="utf-8") as file:
      tr_patterns_content = file.read()
      inputs = {
         'user_question': user_question,
         'answer_task_inputs_description': tr_patterns_content
      }
      answer = answer_team.kickoff(inputs)
      return answer