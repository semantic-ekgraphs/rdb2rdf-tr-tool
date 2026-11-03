from crewai.flow.flow import Flow, start, listen, or_
from crewai.flow.human_feedback import human_feedback, HumanFeedbackResult

class ReviewFlow(Flow):
   @start()
   def generate_transformation_rules(self):
      return "Este é um conteúdo gerado por IA que precisa de revisão."
   
   @human_feedback(
      message="Do you approve these Transformation Rules?",
      emit=["approved", "rejected", "needs_revision"],
      llm="gpt-4o-mini",
      default_outcome="needs_revision",
   )
   @listen(or_("generate_transformation_rules", "needs_revision"))
   def review_transformation_rules(self):
      return "TRs to be reviewed..."

   @listen("approved")
   def on_approval(self, result: HumanFeedbackResult):
      print(f"Approved! Feedback: {result.feedback}")
      print(f"Approved! Feedback: {result.output}")

   @listen("rejected")
   def on_rejection(self, result: HumanFeedbackResult):
      print(f"Rejected. Reason: {result.feedback}")

# flow = ReviewFlow()
# flow.plot("my_flow_plot")
# final_output = flow.kickoff()

# print("---- Final Output ----")
# print(f"Final State: {flow.state}")
