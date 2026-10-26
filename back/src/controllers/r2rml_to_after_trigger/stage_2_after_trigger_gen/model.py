from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


# "1. Compute the set $Relev(R)$ of all relevant Transformation Rules.\n"
# "2. Classify each rule in the set as 'pivot-relevant' or 'relation-relevant'.\n"
# "3. Identify whether multiple occurrences of relation $R$ exist in the rule's relational path.\n"
# "4. Map and specify which formal maintenance components must be computed by the trigger, "
# "including: affected pivot tuples for deletion ($A^-$), affected pivot tuples for insertion ($A^+$), "
# "post-update contributions ($S2$), and final insertion ($\Delta^+$) and deletion ($\Delta^-$) changesets.\n\n"
# "Consolidate all analyses into a declarative execution plan that will directly guide the trigger synthesis agent."
# relation: str = Field(
# default=None, 
# description="The relation",
#                          examples=["company → rdf:type / schema:Organization"])
class TriggerPlanRow(BaseModel):
   relation: str = Field(
      default=None, 
      description="The relation",
      examples=["company, employee, supplier"]
   )
   relevant_rules: str = Field(
      default=None, 
      description="Compute the set $Relev(R)$ of all relevant Transformation Rules for relation $R$",
      examples=["tr-company-1, tr-company-2", "tr-employee-5"]
   )
   rules: str = Field(
      default=None, 
      description="The transformation rule formula"
   )
   rule_classification: str = Field(
      default=None, 
      description="Classify each rule in the set as 'pivot-relevant' or 'relation-relevant'",
      examples=["pivot-relevant", "relation-relevant"]
   )
   multiple_path_occurrences: bool = Field(
      default=None, 
      description="Identify whether multiple occurrences of relation $R$ exist in the rule's relational path",
      examples=["Yes", "No"]
   )
   compute_a_minus: bool = Field(
      default=None, 
      description="Determines whether the maintenance components —the affected pivot tuples ($A^{-}$)— need to be computed",
      examples=["Yes", "No"]
   )
   compute_a_plus: bool = Field(
      default=None, 
      description="Determines whether the maintenance components —the affected pivot tuples ($A^{+}$)— need to be computed",
      examples=["Yes", "No"]
   )
   compute_s2: bool = Field(
      default=None, 
      description="Determines whether the maintenance components —post-update contributions (S2)— need to be computed",
      examples=["Yes", "No"]
   )
   compute_delta_pivot: bool = Field(
      default=None, 
      description="Determines whether the maintenance components —post-update deletions changesets contributions (\Delta^+_\{\text\{pivot\}\})— need to be computed",
      examples=["Yes", "No"]
   )
   compute_delta_rel: bool = Field(
      default=None, 
      description="Determines whether the maintenance components —post-update insertions changesets contributions (\Delta^+_\{\text\{rel\}\})— need to be computed",
      examples=["Yes", "No"]
   )
   compute_delta_plus: bool = Field(
      default=None,
      description="Determines whether the maintenance components —Final net insertion changeset for the relevant rules: contributions present after the update and absent before it, after set-semantic deduplication. It includes eligible insertions from both (\Delta^+\{\text\{pivot\}\}) and (\Delta^+\{\text\{rel\}\}).",
      examples=["Yes", "No"]
   )
   compute_delta_minus: bool = Field(
      default=None,
      description="Determines whether the maintenance components —Final net deletion changeset for the relevant rules: contributions present before the update and absent after it, after set-semantic deduplication. It includes removals from the manufacturer pivot rules and any tr-products-5 contributions invalidated by the changed manufacturer endpoint.",
      examples=["Yes", "No"]
   )


class StaticVerificationRow(BaseModel):
   relation: str
   status: str
   criterion: str
   finding: str
   affected_component: str = ""
   repair_instruction: str = ""