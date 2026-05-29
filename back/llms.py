import os
from dotenv import load_dotenv
from crewai import LLM 

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

##############################################
### CREWAI
##############################################
llama3_groq = LLM(
   model="groq/llama-3.3-70b-versatile", 
   temperature=0,
   api_key=GROQ_API_KEY
)