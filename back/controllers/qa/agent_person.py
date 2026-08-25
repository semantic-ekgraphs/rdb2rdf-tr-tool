# from crewai_tools import FileReadTool
# from pathlib import Path
# from crewai import Agent, Task
# from llms import llama3_groq, gpt_4o_mini_openai

# # Inicialização da ferramenta
# kg_persons = Path(__file__).parent / "../../knowledge/renato-data.txt"
# file_read_tool = FileReadTool(file_path=str(kg_persons))

# # Refinamento do Agent: Adição de diretrizes de comportamento estritas no backstory
# persona_agent = Agent( 
#    role="Senior Analyst specialized in persons and relationships.", 
#    goal="Extract and report information strictly based on provided knowlegde sources.", 
#    backstory="""You are an expert analyst. Your core principle is total fidelity 
#    to source material. You never use outside knowledge. If the provided context 
#    from the tool does not contain the answer, you state 'Sorry...I don't know answer!'. 
#    You are incapable of hallucination, inference, or assumption. You only process 
#    what is explicitly stated in the provided text file.""", 
#    tools=[file_read_tool],
#    verbose=True, 
#    llm=gpt_4o_mini_openai
# )

# # Refinamento da Task: Foco em "Contexto Obrigatório"
# answer_person_task = Task( 
#    description=(
#       "1. Use the FileReadTool to read the content of the file.\n"
#       "2. Analyze the file content to answer this specific question: '{user_question}'.\n"
#       "3. Strict Guardrails:\n"
#       "   - Use ONLY the information retrieved from the tool.\n"
#       "   - If the answer is not explicitly in the text, you MUST answer: 'Sorry...I don't know answer!'\n"
#       "   - Do not add conversational filler, polite greetings, or supplementary explanations.\n"
#       "   - Do not infer relationships not explicitly stated in the text."
#    ), 
#    expected_output="A direct, concise sentence answering the question based solely on the provided text, not exceeding 100 words.", 
#    agent=persona_agent
# )