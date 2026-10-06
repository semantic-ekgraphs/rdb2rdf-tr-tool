from fastapi import APIRouter
from controllers.r2rml_to_after_trigger.after_trigger_gen import after_trigger_gen_controller
from constants import TR_TO_AFTER_TRIGGER

router  = APIRouter(
   prefix="/tr-to-after-trigger",
   tags=[TR_TO_AFTER_TRIGGER],
   responses={404: {"description": "Not Found!"}}
)

@router.get("/compilation/", description="Route to TR-to-After-Trigger Compilation.")
async def compile_tr_to_after_trigger():  
   return await after_trigger_gen_controller.transform_transformation_rules_into_after_trigger()


