from fastapi import APIRouter
from controllers.qa import qa_controller
from constants import TAG_QA

router  = APIRouter(
   prefix="/qa",
   tags=[TAG_QA],
   responses={404: {"description": "Not Found!"}}
)


@router.get("/person/", description="Route to answer a user's questions about person and relationship")
async def answer_person_relationship_question(user_question: str):  
   return await qa_controller.answer_person_question_with_knowledge_sources(user_question)
