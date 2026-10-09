from .qa_agentic import team_answer_questions_about_people_using_ks


async def answer_person_question_with_knowledge_sources(user_question:str) -> str:
   inputs = {
      'user_question': user_question,
   }
   answer = team_answer_questions_about_people_using_ks.kickoff(inputs)
   return answer 