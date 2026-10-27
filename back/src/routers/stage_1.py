from fastapi import APIRouter
from pathlib import Path
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
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
   return await tr_gen_controller.extract_metadata("a_r2rml.ttl", "a_schema.sql")



@router.get("/entitiy-preservation-analysis/", 
            description="Route to analyzes entity-preservation from extracted metadata.")
async def analyzes_entity_preservation():  
   return await tr_gen_controller.analyzes_entity_preservation()



@router.get("/tr-gen/", 
            description="Route to convert R2RML mapping to transformation r ules.")
async def generates_transformation_rules():  
   return await tr_gen_controller.generates_transformation_rules()



TEMP_DIR = Path("../temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/metadata-extraction/", 
            description="Route to extract R2RML metadata.")
async def metadata_extraction(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
   try:
      # Sanitização simples e salvamento em /temp
      file1_path = TEMP_DIR / Path(file1.filename).name
      file2_path = TEMP_DIR / Path(file2.filename).name

      with open(file1_path, "wb") as buffer:
         shutil.copyfileobj(file1.file, buffer)

      with open(file2_path, "wb") as buffer:
         shutil.copyfileobj(file2.file, buffer)

        # Execute aqui a lógica de extração usando file1_path e file2_path
      return await tr_gen_controller.extract_metadata(file1.filename,file2.filename)
        
   except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))


   



# @router.post("/entitiy-preservation-analysis/", 
#             description="Route to analyzes entity-preservation from extracted metadata.")
# async def analyzes_entity_preservation():  
#    return await tr_gen_controller.analyzes_entity_preservation()



# @router.post("/tr-gen/", 
#             description="Route to convert R2RML mapping to transformation r ules.")
# async def generates_transformation_rules():  
#    return await tr_gen_controller.generates_transformation_rules()