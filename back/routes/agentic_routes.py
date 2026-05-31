from fastapi import APIRouter
from controllers.agentic import qa_controller, rdb2rdf_controller
from constants import TXT_TEN_DASHES, TAG_AGENTIC
from utils import console_log, info

router = APIRouter()
# linha = len(TXT_TEN_DASHES + " DATASET ROUTES " + TXT_TEN_DASHES)
console = lambda x: console_log("AGENTIC ROUTES", x)


# @router.post("/schema-assistent/", 
#    tags=[TAG_LLM], 
#    description="Routes used to call the schema assistent agent.")
# async def call_schema_assistent(question:str, headers: Annotated[HeadersModel, Header()]):  
#    print(console('call_schema_assistent()'))  
#    return organization_controller.call_schema_assistent(data, headers.repository, headers.language)



@router.get("/agentic/trp_qa/", 
   tags=[TAG_AGENTIC],
   description="Route to answer a user's questions about TRs patterns")
# async def make_a_question(data: QuestionModel , headers: Annotated[HeadersModel, Header()]):  
async def answer_tr_patterns_question(user_question: str):  
   print(console('answer_tr_patterns_question()'))  
   info('user question', user_question)
   return await qa_controller.answer_tr_patterns_question(user_question)



@router.get("/agentic/r2rml2tr/", 
   tags=[TAG_AGENTIC], 
   description="Route to transform R2RML mappings to RDF Tranformation Rules")
async def transform_r2rml_to_transformation_rules():  
   print(console('transform_r2rml_to_transformation_rules()'))  
   return await rdb2rdf_controller.transform_r2rml_to_transformation_rules()