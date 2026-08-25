import json
from pathlib import Path
from datetime import datetime
from utils import console_log, read_txt_file, write_json_after_trigger_output_file
from .rdb2rdf_agentic import object_preserving_team, transformation_rules_team
from .entity_preserving import entity_preserving_team
# from .workflow import transformation_rules_team
# from .workflow import object_preserving_team
# from .agent_trigger import ivm_trigger_crew_v2
# from .agent_vania import team_after_trigger

console = lambda x: console_log("RDB2RDF CONTROLLER", x)
# inputs
r2rml_file                = Path(__file__).parent / "../../temp/mbz_r2rml_short.ttl"
rdb_schema_file           = Path(__file__).parent / "../../temp/mbz_schema_short.sql"
tr_patterns_file          = Path(__file__).parent / "../../knowledge/tr_patterns_v2.txt"
ivm_formal_framework_file = Path(__file__).parent / "../../knowledge/ivm-formal-framework.txt"
maintenance_queue_file    = Path(__file__).parent / "../../knowledge/maintenance-queue-infrastructure.txt"
ontology_file             = Path(__file__).parent / "../../knowledge/ontology.txt"
uri_definition_file       = Path(__file__).parent / "../../knowledge/uri_predicates_definition.txt"
# outputs
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
parsing_md_file           = Path(__file__).parent / "../../temp/parsing.md"
parsing_json_file         = Path(__file__).parent / f"../../temp/parsing_r2rml_{date_now}.json"
mbz_tr_file               = Path(__file__).parent / "../../temp/mbz_tr.json"


# async def generate_after_trigger(relation:str) -> str:
#    print(console('generate_after_trigger()'))
   
#    ivm_formal_framework_content = read_txt_file(ivm_formal_framework_file)
#    maintenance_queue_content    = read_txt_file(maintenance_queue_file)
#    schema_sql_content           = read_txt_file(schema_sql_short_file)
#    ontology_content             = read_txt_file(ontology_file)
#    with open(mbz_tr_file, 'r', encoding='utf-8') as file:
#       mbz_tr_content = json.load(file)

#       inputs = {
#          'ivm_formal_framework':             ivm_formal_framework_content,
#          'musicbrainz_schema':               schema_sql_content,
#          'mb_trs_source':                    mbz_tr_content,
#          'musicbrainz_ontology':             ontology_content,
#          'maintenance_queue_infrastructure': maintenance_queue_content,
#          'relation':                         relation
#       }

#       answer = team_after_trigger.kickoff(inputs)
#       print(f'answer: {answer}')

#       trigger_json_file = Path(__file__).parent / f'../../temp/trigger_{relation}_{date_now}.json'
#       # with open(trigger_json_file, "w", encoding="utf-8") as file_trigger_output:
#       #    file_trigger_output.write('answer.raw')
#       write_json_after_trigger_output_file(trigger_json_file, answer.raw)
#       return 'answer'




# async def transform_r2rml_to_transformation_rules() -> str:
#    print(console('transform_r2rml_to_transformation_rules()'))

#    r2rml_content       = read_txt_file(r2rml_file)
#    schema_sql_content  = read_txt_file(schema_sql_short_file)
#    tr_patterns_content = read_txt_file(tr_patterns_file)

#    # These key must be the same in input_description in the Task
#    inputs = {
#       'r2rml_mapping': r2rml_content, 
#       'rdb_schema':    schema_sql_content,
#       'tr_patterns':   tr_patterns_content
#    }

#    answer = transformation_rules_team.kickoff(inputs)

#    _return = None
#    with open(parsing_json_file, "w", encoding="utf-8") as file:
#       # ensure_ascii=False: Crucial if your data includes international characters, symbols, or emojis. This saves them natively rather than converting them to escape sequences like \u1234
#       _return = file.write(answer.raw)
#       if _return is not None:
#          return answer
#       else:
#          return {'message': 'Fail!!'}
            




# async def object_preserving_analysis() -> str:
#    print(console('object_preserving_analysis()'))

#    # schema_sql_content     = read_txt_file(schema_sql_short_file)
#    r2rml_content    = read_txt_file(r2rml_file)
#    # uri_definition_content = read_txt_file(uri_definition_file)
#    # tr_patterns_content = read_txt_file(tr_patterns_file)

#    inputs = {
#       # 'rdb_schema':     schema_sql_content,
#       'r2rml_mapping':  r2rml_content, 
#       # 'uri_definition': uri_definition_content,
#       # 'tr_patterns':    tr_patterns_content
#    }

#    answer = object_preserving_team.kickoff(inputs)
   
#    if answer is not None:
#       return answer
#    else:
#       return {'message': 'Fail!!'}





async def analyzes_entity_preserving_R2RML_mappings():
   print(console('analyzes_entity_preserving_R2RML_mappings()'))

   rdb_schema_content = read_txt_file(rdb_schema_file)
   r2rml_content      = read_txt_file(r2rml_file)
   # uri_definition_content = read_txt_file(uri_definition_file)
   # tr_patterns_content = read_txt_file(tr_patterns_file)

   inputs = {
      'rdb_schema':     rdb_schema_content,
      'r2rml_mapping':  r2rml_content, 
      # 'uri_definition': uri_definition_content,
      # 'tr_patterns':    tr_patterns_content
   }
   answer = entity_preserving_team.kickoff(inputs)
   if answer is not None:
      return answer
   else:
      return {'message': 'Fail!!'}



#################################
### TRIGGERS TEAM
#################################


# mbz_tr_file =        Path(__file__).parent / "../../temp/parsings.json"
# ivm_formal_framework_file =        Path(__file__).parent / "../../knowledge/ivm-formal-framework.txt"
# async def generate_after_trigger_from_rdb2rdf_transformation_rules(relation:str) -> str:
#    print(console('generate_after_trigger()'))
   
#    with open(ivm_formal_framework_file, "r", encoding="utf-8") as file4:
#       ivm_formal_framework_content = file4.read()

#       inputs = {
#          'ivm_formal_framework': ivm_formal_framework_content,
#          'musicbrainz_schema':     None,
#          'mb_trs_source':          None,
#          'musicbrainz_ontology':   None,
#          'relation': relation
#       }

#       answer = ivm_trigger_crew_v2.kickoff(inputs)
#       print(f'answer: {answer}')

#       ### SAVE THE ANSWER WITH THE AFTER TRIGGER AS JSON IN THE \TEMP FOLDER 
#       # trigger_json_file = Path(__file__).parent / f"../../temp/trigger_{relation}_{datetime.now()}.json"
#       # with open(trigger_json_file, "w", encoding="utf-8") as file_of_trigger:
#       #    file_of_trigger.write(answer.raw)
#       write_json_after_trigger_output_file(answer.raw, relation)
#       return answer

   # return "transform_transformation_rules_in_after_trigger"












# from crewai_files import File, ImageFile, PDFFile, AudioFile, VideoFile, TextFile

# image = ImageFile(source="screenshot.png")
# pdf = PDFFile(source="report.pdf")
# audio = AudioFile(source="meeting.mp3")
# video = VideoFile(source="demo.mp4")
# text = TextFile(source="data.csv")

# file = File(source="document.pdf")

