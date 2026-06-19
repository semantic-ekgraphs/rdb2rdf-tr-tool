from constants import TXT_TEN_DASHES
from uuid import uuid4
from pathlib import Path
from utils import filter_by_language, console_log, print_json_idented, info
from .workflow import transformation_rules_team, ivm_compilation_crew
from .agent_trigger import ivm_trigger_crew_v2

console = lambda x: console_log("AGENTIC CONTROLLER", x)
# inputs
r2rml_file =        Path(__file__).parent / "../../temp/mbz_r2rml.ttl"
schema_sql_file =   Path(__file__).parent / "../../temp/mbz_schema.sql"
tr_patterns_file =  Path(__file__).parent / "../../knowledge/tr_patterns.txt"
# outputs
parsing_md_file =   Path(__file__).parent / "../../temp/parsing.md"
parsing_json_file = Path(__file__).parent / "../../temp/parsing.json"
trigger_json_file = Path(__file__).parent / "../../temp/trigger.json"

async def transform_r2rml_to_transformation_rules() -> str:
   print(console('transform_r2rml_to_transformation_rules()'))

   ### PASS THE R2RML FILE TO THE INPUT AS CONTEXT
   with open(r2rml_file, "r") as file:
      r2rml_content = file.read()
      ### PASS THE SCHEMA FILE TO THE INPUT AS CONTEXT
      with open(schema_sql_file, "r") as file2:
         schema_sql_content = file2.read()
         ### PASS THE TR PATTERNS FILE TO THE INPUT AS CONTEXT
         with open(tr_patterns_file, "r", encoding="utf-8") as file3:
            tr_patterns_content = file3.read()
            inputs = {
               'r2rml_mapping': r2rml_content, # This key must be the same in input_description in the Task
               'rdb_schema':    schema_sql_content,
               'tr_patterns':   tr_patterns_content
            }

            ### CALL THE CREW
            answer = transformation_rules_team.kickoff(inputs)

            # print(f'answer: {answer}')

            ### SAVE THE ANSWER AS JSON IN THE \TEMP FOLDER 
            with open(parsing_json_file, "w", encoding="utf-8") as file:
               file.write(answer.raw)
               # file.write(answer.model_dump())
               return answer
            



#################################
### TRIGGERS TEAM
#################################
from crewai_files import File, ImageFile, PDFFile, AudioFile, VideoFile, TextFile

image = ImageFile(source="screenshot.png")
pdf = PDFFile(source="report.pdf")
audio = AudioFile(source="meeting.mp3")
video = VideoFile(source="demo.mp4")
text = TextFile(source="data.csv")

file = File(source="document.pdf")

# inputs
mbz_tr_file =        Path(__file__).parent / "../../temp/parsings.json"
ivm_formal_framework_file =        Path(__file__).parent / "../../knowledge/IVM_abril_21__Current_version_ (9).pdf"
# outputs
async def generate_after_trigger_from_transformation_rules() -> str:
   print(console('transform_transformation_rules_in_after_trigger()'))
   with open(ivm_formal_framework_file, "r", encoding="utf-8") as file4:
      ivm_formal_framework_content = file4.read()
      inputs = {
         'ivm_framework_document': ivm_formal_framework_content,
         'musicbrainz_schema':     None,
         'mb_trs_source':          None,
         'musicbrainz_ontology':   None,
         'table': "artist"
      }

      ### CALL THE CREW
      # answer = ivm_compilation_crew.kickoff(inputs)
      answer = ivm_trigger_crew_v2.kickoff(inputs)
      print(f'answer: {answer}')

      ### SAVE THE ANSWER WITH THE AFTER TRIGGER AS JSON IN THE \TEMP FOLDER 
      with open(trigger_json_file, "w", encoding="utf-8") as file_of_trigger:
         file_of_trigger.write(answer.raw)
         return answer

   # return "transform_transformation_rules_in_after_trigger"
