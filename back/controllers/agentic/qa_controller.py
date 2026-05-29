from constants import TXT_TEN_DASHES
from uuid import uuid4
from utils import filter_by_language, console_log, print_json_idented, info
from .workflow import answer_team

console = lambda x: console_log("AGENTIC CONTROLLER", x)


async def answer_a_user_question(user_question:str) -> str:
   print(console('answer_a_user_question()'))
   inputs = {
      'user_question': user_question,
   }
   answer = answer_team.kickoff(inputs)
   return answer