from crewai.flow.flow import Flow, start, listen
from crewai.flow.human_feedback import human_feedback, HumanFeedbackResult

class SimpleReviewFlow(Flow):
   @start()
   @human_feedback(
      message="Do you approve this content?"
   )
   def generate_transformation_rules(self):
      return "Este é um conteúdo gerado por IA que precisa de revisão."

   @listen(generate_transformation_rules)
   def process_feedback(self, result: HumanFeedbackResult):
      print(f"Conteúdo: {result.output}")
      print(f"Humano disse: {result.feedback}")

flow = SimpleReviewFlow()
flow.plot("my_tr_flow_plot")
final_output = flow.kickoff()

print("---- Final Output ----")
print(final_output)
print("Final State:")
print(flow.state)