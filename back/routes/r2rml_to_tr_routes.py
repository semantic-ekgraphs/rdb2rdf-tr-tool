from fastapi import APIRouter
from controllers.rdb2rdf import rdb2rdf_controller
from controllers.rdb2rdf import entity_preserving
from controllers.r2rml_to_tr import r2rml_to_tr_controller
from constants import TAG_R2RML_TO_TR

router  = APIRouter(
   prefix="/r2rml-to-tr",
   tags=[TAG_R2RML_TO_TR],
   responses={404: {"description": "Not Found!"}}
)

@router.get("/compilation/", description="Route to R2RML-to-TR Compilation.")
async def compile_R2RML_to_TR():  
   return await r2rml_to_tr_controller.compile_r2rml_to_trasnformation_rules_using_knowledge_sources()
   # return await r2rml_to_tr_controller.compile_R2RML_to_Trasnformation_rules()


