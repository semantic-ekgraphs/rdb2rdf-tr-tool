from crewai import Agent, Task
from llms import llama3_groq


#################################
### TRANSFORMATION RULES TEAM
#################################

#################################
### TRIGGERS TEAM
#################################


#################################
### ANSWER TEAM
#################################
generic_answer_agent = Agent(
   role="Oráculo que responde perguntas de qualquer tipo",
   goal="Responder uma pergunta de usuário",
   backstory="""Tem mais de 1000 anos experiência em resposta a perguntas simples e complexas.""",
   verbose=True,
   llm=llama3_groq
)
answer_task = Task(
   description="""
      Responder a pergunta "{user_question}"
   """,
   expected_output="""
      Um texto de exatamente 20 palavras em inglês.
      Não mais que 20 palavras e não menos que 20 palavras.
   """,
   agent=generic_answer_agent,
)