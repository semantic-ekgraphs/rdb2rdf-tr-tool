from crewai import Agent, Task, Crew
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from .qa_knowledge import person_knowledge_source_txt, person_knowledge_source_str
from llms import gpt_4o_mini_openai

people_relationship_response_agent = Agent( 
   role="Senior Analyst specialized in persons and relationships.", 
   goal="Extract and report information strictly based on provided knowlegde sources.", 
   backstory="""You are an expert analyst. Your core principle is total fidelity 
   to knowledge source material. You only process what is explicitly stated in the provided knowledge sources.
   You never use outside knowledge. You are incapable of hallucination, inference, or assumption. """, 
   verbose=True, 
   memory=False,
   llm=gpt_4o_mini_openai
)


task_answer_people_relationship_question = Task( 
   description=(
      "1. Answer this specific question: '{user_question}'.\n"
      "2. Strict Guardrails:\n"
      "  - If the the knowledge sources does not contain the answer, you state 'Sorry...I don't know answer!'.\n"
      "  - Do not consider similar names; respond only to identical names.\n"
      "  - Do not add conversational filler, polite greetings, or supplementary explanations.\n"
      "  - Do not infer relationships not explicitly stated in the knowledge sources."
   ), 
   expected_output="A direct, concise sentence answering the question, not exceeding 50 words.", 
   agent=people_relationship_response_agent
)


# person_knowledge_source = StringKnowledgeSource(
#    content="Renato é casado com Eliene. Ele tem os filhos Manuel Neto e Ravi."
# )

team_answer_questions_about_people_using_ks = Crew(
   agents=[people_relationship_response_agent],
   tasks=[task_answer_people_relationship_question],
   process='sequential',
   knowledge_sources=[person_knowledge_source_txt, person_knowledge_source_str]
)