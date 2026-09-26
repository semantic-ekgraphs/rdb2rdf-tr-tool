from fastapi import APIRouter
from controllers.rdb2rdf import rdb2rdf_controller
from controllers.rdb2rdf import entity_preserving
from controllers.r2rml_to_tr import r2rml_to_tr_controller
from constants import TR_TO_AFTER_TRIGGER

router  = APIRouter(
   prefix="/tr-to-after-trigger",
   tags=[TR_TO_AFTER_TRIGGER],
   responses={404: {"description": "Not Found!"}}
)

@router.get("/compilation/", description="Route to TR0-to-After-Trigger Compilation.")
async def compile_tr_to_after_trigger():  
   return "await r2rml_to_tr_controller.compile_tr_to_after_trigger()"


