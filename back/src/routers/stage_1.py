from fastapi import APIRouter
from ..controllers.r2rml_to_after_trigger.stage_1_tr_gen import tr_gen_controller
from constants import TAG_R2RML_TO_TR

router  = APIRouter(
   prefix="/r2rml-to-tr",
   tags=[TAG_R2RML_TO_TR],
   responses={404: {"description": "Not Found!"}}
)

@router.get("/metadata-extraction/", 
            description="Route to extract R2RML metadata.")
async def extract_metadata():  
   return await tr_gen_controller.extract_metadata()



@router.get("/entitiy-preservation-analysis/", 
            description="Route to analyzes entity-preservation from extracted metadata.")
async def analyzes_entity_preservation():  
   return await tr_gen_controller.analyzes_entity_preservation()



@router.get("/tr-gen/", 
            description="Route to convert R2RML mapping to transformation r ules.")
async def generates_transformation_rules():  
   return await tr_gen_controller.generates_transformation_rules()