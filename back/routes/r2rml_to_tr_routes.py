from fastapi import APIRouter
from controllers.rdb2rdf import rdb2rdf_controller
from controllers.rdb2rdf import entity_preserving
from controllers.r2rml_to_tr import r2rml_to_tr_controller
from controllers.r2rml_to_after_trigger.tr_gen import tr_gen_controller
from constants import TAG_R2RML_TO_TR

router  = APIRouter(
   prefix="/r2rml-to-tr",
   tags=[TAG_R2RML_TO_TR],
   responses={404: {"description": "Not Found!"}}
)

@router.get("/extract-metadata/", 
            description="Route to extract R2RML metadata.")
async def extract_metadata():  
   return await tr_gen_controller.extract_metadata()



@router.get("/entitiy-preservation-analysis/", 
            description="Route to analyzes entity-preservation from extracted metadata.")
async def analyzes_entity_preservation():  
   return await tr_gen_controller.analyzes_entity_preservation_in_R2RML_mappings()



@router.get("/tr-gen/", 
            description="Route to Convert R2RML mapping to Transformation Rules.")
async def transformation_rules_generation():  
   return await tr_gen_controller.transformation_rules_generation()