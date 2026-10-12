from fastapi import APIRouter
from ..controllers.r2rml_to_after_trigger.stage_3_triiger_validation_repair import trigger_validation_repair_controller
from constants import TAG_TRIGGER_VALIDATION_AND_REPAIR

router  = APIRouter(
   prefix="/trigger-validation",
   tags=[TAG_TRIGGER_VALIDATION_AND_REPAIR],
   responses={404: {"description": "Not Found!"}}
)

@router.get("/test-generation/", description="Route to plan AFTER trigger.")
async def test_generation():  
   return await trigger_validation_repair_controller.test_generation()



@router.get("/runtime-validation/", description="Route to plan AFTER trigger.")
async def runtime_validation():  
   return await trigger_validation_repair_controller.runtime_validation()



@router.get("/automatic-diagnosis-repair/", description="Route to plan AFTER trigger.")
async def automatic_diagnosis_repair():  
   return await trigger_validation_repair_controller.automatic_diagnosis_repair()