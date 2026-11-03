from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ExampleState(BaseModel):
   counter: int = 0
   message: str = ""

class OutputStateExampleFlow(Flow[ExampleState]):
   @start()
   def search_topic(self):
      self.state.message = "Hello from first_method"
      self.state.counter += 1
      return "Output from first_method"

   @listen(search_topic)
   def write_peotry(self, first_output):
      self.state.message += " - updated by second_method"
      self.state.counter += 1
      return f"Second method received: {first_output} - {self.state.message}"


flow = OutputStateExampleFlow()
flow.plot("my_flow_plot")
final_output = flow.kickoff()

print("---- Final Output ----")
print(final_output)
print("Final State:")
print(flow.state)