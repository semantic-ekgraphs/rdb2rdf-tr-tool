from typing import Optional, List
from pydantic import BaseModel, Field

# ==========================================
# 1. DEFINING OUTPUT MODELS WITH Pydantic
# ==========================================
class LogicalTable(BaseModel):
   query_or_relation:        str = Field(default=None, description="Table name or SQL query in the rr:logicalTable")
   transformation: Optional[str] = Field(default=None, description="All SQL transformation functions (UPPER, LOWER, REPLACE, SUBSTRING, etc) applied to attributes in the extracted SQL query")
   condition:      Optional[str] = Field(default=None, description="Selection conditions in an SQL query used to filter rows in a database table, employing operators such as equal to (=), not equal to (!= or <>), greater than/less than (< >), BETWEEN, IN, LIKE, IS NULL, IS NOT NULL, SIMILAR TO and all selection conditions operators known in SQL and relational database literature, as well as possible combinations thereof.")
      

class MetadataParsing(BaseModel):
   triples_map_id:          str = Field(default=None, description="Identifier of the rr:TriplesMap")
   logical_table:  LogicalTable = Field(default=None, description="Logical Tables.")
