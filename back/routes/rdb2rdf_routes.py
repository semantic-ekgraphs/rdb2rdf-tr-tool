from fastapi import APIRouter
from controllers.rdb2rdf import rdb2rdf_controller
from controllers.rdb2rdf import entity_preserving
from constants import TAG_RDB2RDF

router  = APIRouter(
   prefix="/rdb2rdf",
   tags=[TAG_RDB2RDF],
   responses={404: {"description": "Not Found!"}}
)


# @router.get("/object-preserving-analysis/", description="Route to object-preserving analysis in R2RML mappings")
# async def object_preserving_analysis():  
#    return await rdb2rdf_controller.object_preserving_analysis()



@router.get("/entity-preserving-analysis/", description="Route to entity-preserving analysis in R2RML mappings")
async def analyzes_entity_preservation_R2RML_mappings():  
   return await rdb2rdf_controller.analyzes_entity_preserving_R2RML_mappings()


# @router.get("/agentic/r2rml-to-tr/", 
#    description="Route to transform R2RML mappings to Object-Preserving Tranformation Rules")
# async def transform_r2rml_to_transformation_rules():  
#    return await rdb2rdf_controller.transform_r2rml_to_transformation_rules()



# @router.get("/agentic/generate-after-trigger/", 
#    description="Route to generate AFTER Trigger from RDB2RDF Tranformation Rules")
# async def generate_after_trigger(relation:str):  
#    return await rdb2rdf_controller.generate_after_trigger(relation)






















# @router.get("/agentic/tr-to-trigger/", 
#    tags=[TAG_AGENTIC], 
#    description="Route to generate AFTER Trigger from RDB2RDF Tranformation Rules")
# async def generate_after_trigger_from_rdb2rdf_transformation_rules(relation:str):  
#    print(console('generate_after_trigger_from_rdb2rdf_transformation_rules()'))  
#    print(f'+ pivot relation: {relation}')
#    return await rdb2rdf_controller.generate_after_trigger_from_rdb2rdf_transformation_rules(relation)


# @router.post("/schema-assistent/", 
#    tags=[TAG_LLM], 
#    description="Routes used to call the schema assistent agent.")
# async def call_schema_assistent(question:str, headers: Annotated[HeadersModel, Header()]):  
#    print(console('call_schema_assistent()'))  
#    return organization_controller.call_schema_assistent(data, headers.repository, headers.language)


# @router.get("/agentic/queue/", tags=[TAG_AGENTIC])
# async def queue():  
#    print(console('queue()'))  
#    return await qa_controller.queue()


# @router.get("/agentic/pdf_rag_tool/", tags=[TAG_AGENTIC])
# async def pdf_rag_tool():  
#    print(console('pdf_rag_tool()'))  
#    return await qa_controller.pdf_rag_tool()


# @router.get("/agentic/knowledge/", tags=[TAG_AGENTIC])
# async def using_knowledge():  
#    print(console('using_knowledge()'))  
#    return await qa_controller.using_knowledge()