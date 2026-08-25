import os
from dotenv import load_dotenv
from crewai import LLM 
load_dotenv()
_GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

##############################################
### GROQ
##############################################
llama3_groq = LLM(
   model="groq/llama-3.3-70b-versatile", 
   temperature=0,
   api_key=_GROQ_API_KEY
)

gpt_oss_20b_groq = LLM(
   model="groq/openai/gpt-oss-20b", 
   temperature=0,
   api_key=_GROQ_API_KEY
)

gpt_oss_120b_groq = LLM(
   model="groq/openai/gpt-oss-120b", 
   temperature=0,
   api_key=_GROQ_API_KEY
)


##############################################
### OLLAMA
##############################################

llama_3b_Ollama = LLM(
   model="ollama/llama3.1:8b", 
   temperature=0,
   base_url="http://localhost:11434"
)

##############################################
### OPENAI (do mais fraco para o mais potente)
##############################################

gpt_4o_mini_openai = LLM(
   model="openai/gpt-4o-mini", 
   api_key=_OPENAI_API_KEY,
   temperature=0,
)

gpt_5_lua_openai = LLM(
   model="openai/gpt-5-lua", 
   api_key=_OPENAI_API_KEY,
   temperature=0,
)