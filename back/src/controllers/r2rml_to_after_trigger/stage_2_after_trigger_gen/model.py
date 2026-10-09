from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field

class TriggerPlanRow(BaseModel):
   relation: str
   relevant_rules: str
   pivot_relevant_rules: str
   relation_relevant_rules: str
   multiple_path_occurrences: bool
   compute_a_minus: bool
   compute_a_plus: bool
   compute_s2: bool
   compute_delta_pivot: bool
   compute_delta_rel: bool
   compute_delta: bool


class StaticVerificationRow(BaseModel):
   relation: str
   status: str
   criterion: str
   finding: str
   affected_component: str = ""
   repair_instruction: str = ""