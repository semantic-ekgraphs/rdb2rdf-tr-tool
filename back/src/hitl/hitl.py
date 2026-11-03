# human_in_the_loop_flow.py
from crewai.flow.flow import Flow, start, router, listen
from litellm import acompletion
from ag_ui_crewai.sdk import copilotkit_stream, CopilotKitState


class HumanInTheLoopFlow(Flow[CopilotKitState]):
   @start()
   @listen("route_follow_up")
   async def start_flow(self):
      pass

   @router(start_flow)
   async def chat(self):
      system_prompt = (
         "You perform tasks for the user. When asked to do a task, call the "
         "tool the frontend provides so the user can approve or adjust the steps "
         "before you continue."
      )

      response = await copilotkit_stream(
         await acompletion(
               model="openai/gpt-4o-mini",
               messages=[
                  {"role": "system", "content": system_prompt},
                  *self.state.messages,
               ],
               tools=[*self.state.copilotkit.actions],  # tools registered by the frontend
               parallel_tool_calls=False,
               stream=True,
         )
      )

      message = response.choices[0].message
      self.state.messages.append(message)
      return "route_end"

   @listen("route_end")
   async def end(self):
      pass