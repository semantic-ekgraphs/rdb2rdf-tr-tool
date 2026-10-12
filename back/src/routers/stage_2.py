from fastapi import APIRouter
from ..controllers.r2rml_to_after_trigger.stage_2_after_trigger_gen import after_trigger_gen_controller
from constants import TAG_TR_TO_TRIGGER

router  = APIRouter(
   prefix="/tr-to-after-trigger",
   tags=[TAG_TR_TO_TRIGGER],
   responses={404: {"description": "Not Found!"}}
)

@router.get("/trigger-planning/", description="Route to plan AFTER trigger.")
async def plan_trigger():  
   return await after_trigger_gen_controller.plan_after_trigger()


@router.get("/trigger-synthesis/", description="Route to generate AFTER trigger.")
async def synthesizes_verifies_trigger():  
   return await after_trigger_gen_controller.synthesizes_verifies_trigger()


@router.get("/trigger-static-verification/", description="Route for trigger static verification.")
async def trigger_static_verification():  
   return await after_trigger_gen_controller.trigger_static_verification()