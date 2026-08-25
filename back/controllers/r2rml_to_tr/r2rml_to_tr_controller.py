import json
from pathlib import Path
from datetime import datetime
from utils import console_log, read_txt_file, write_json_after_trigger_output_file
from utils import read_csv_and_transform_in_input_to_task
# from .r2rml-to-tr_agentic import object_preserving_team, transformation_rules_team
# from .entity_preserving import entity_preserving_team
# from .workflow import transformation_rules_team
# from .workflow import object_preserving_team
# from .agent_trigger import ivm_trigger_crew_v2
# from .agent_vania import team_after_trigger
from .r2rml_to_tr_mbz import r2rml_to_tr_compilation_team
# from .r2rml_to_tr_mbz import r2rml_to_tr_compilation_team_using_knowledge_sources
from .r2rml_to_tr_agentic import r2rml_to_tr_compilation_team_using_knowledge_sources
from .r2rml_to_tr_agentic import task_parsing_r2rml_to_table

console = lambda x: console_log("R2RML2TR CONTROLLER", x)
# inputs
rdb_schema_file           = Path(__file__).parent / "../../temp/mbz_schema_short.sql"
r2rml_file                = Path(__file__).parent / "../../temp/mbz_r2rml_short_short.ttl"
tr_patterns_file          = Path(__file__).parent / "../../knowledge/tr_patterns_v2.txt"
tr_formalism_file         = Path(__file__).parent / "../../knowledge/formal_espec_entity_preserving.txt"
ivm_formal_framework_file = Path(__file__).parent / "../../knowledge/ivm-formal-framework.txt"
maintenance_queue_file    = Path(__file__).parent / "../../knowledge/maintenance-queue-infrastructure.txt"
ontology_file             = Path(__file__).parent / "../../knowledge/ontology.txt"
uri_definition_file       = Path(__file__).parent / "../../knowledge/uri_predicates_definition.txt"
# outputs
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
parsing_md_file           = Path(__file__).parent / "../../temp/parsing.md"
parsing_json_file         = Path(__file__).parent / f"../../temp/parsing_r2rml_{date_now}.json"
mbz_tr_file               = Path(__file__).parent / "../../temp/mbz_tr.json"


async def compile_R2RML_to_Trasnformation_rules():
   print(console('compile_R2RML_to_Trasnformation_rules()'))

   rdb_schema_content   = read_txt_file(rdb_schema_file)
   r2rml_content        = read_txt_file(r2rml_file)
   tr_formalism_content = read_txt_file(tr_formalism_file)
   tr_patterns_content  = read_txt_file(tr_patterns_file)

   inputs = {
      'rdb_schema':    rdb_schema_content,
      'r2rml_mapping': r2rml_content, 
      'tr_formalism':  tr_formalism_content,
      'tr_patterns':   tr_patterns_content
   }
   answer = r2rml_to_tr_compilation_team.kickoff(inputs)
   if answer is not None:
      return answer
   else:
      return {'message': 'Fail!!'}




from utils import cut_json_struture
from utils import get_descriptions_of_a_pydantic_model
from .model import TriplesMapParsing
async def compile_r2rml_to_trasnformation_rules_using_knowledge_sources():
   print(console('compile_R2RML_to_Trasnformation_rules_with_knowledge_sources()'))

   # _model = cut_json_struture(dict(TriplesMapParsing.model_json_schema()["properties"]))

   # descriptions_model = get_descriptions_of_a_pydantic_model(dict(TriplesMapParsing.model_json_schema()["properties"]))
   # print(f'{descriptions_model}')
   # inputs = {
   #    'rdb_schema'   : read_txt_file(rdb_schema_file),
   #    'r2rml_mapping': read_txt_file(r2rml_file), 
   #    'output_model': _model
   # }

   csv_file = Path(__file__).parent / f"../../temp/r2rml_parsing_2026-08-25_09-30-51-correct.csv"
   csv_content = read_csv_and_transform_in_input_to_task(csv_file, ";"),
   inputs = {
      'csv' : str(csv_content)
   }

   answer = r2rml_to_tr_compilation_team_using_knowledge_sources.kickoff(inputs)

   if answer is not None:
      return answer
   else:
      return {'message': 'Fail!!'}