from typing import Optional, List
from pydantic import BaseModel, Field

# ==========================================
# 1. DEFINING OUTPUT MODELS WITH Pydantic
# ==========================================


class TriplesMapParsing(BaseModel):
   triples_map_id:          str = Field(default=None, description="Identifier of the triples mapping (rr:TriplesMap).")
   logical_table:           str = Field(default=None, description="Table name or SQL query in the logical table (rr:logicalTable).")
   transformation_function: Optional[str] = Field(default=None, description="All SQL transformation functions (UPPER, LOWER, REPLACE, SUBSTRING, etc) applied to attributes in the extracted SQL query")
   selection_condition:     Optional[str] = Field(default=None, description="Selection conditions in an SQL query used to filter rows in a database table, employing operators such as equal to (=), not equal to (!= or <>), greater than/less than (< >), BETWEEN, IN, LIKE, IS NULL, IS NOT NULL, SIMILAR TO and all selection conditions operators known in SQL and relational database literature, as well as possible combinations thereof.")
   source_r2rml_mapping:    str = Field(default=None, description="Source R2RML mapping: rr:subjectMap or rr:predicateObjectMap")
   subject_class:           Optional[str] = Field(default=None, description="The RDF class of subject mapping (rr:subjectMap).")
   uri_subject_template:    Optional[str] = Field(default=None, description="Subject URI template defined in the subject mapping.")
   mapped_rdf_predicate:    Optional[str] = Field(default=None, description="The mapped RDF class or property.")
   mapped_object:           Optional[str] = Field(default=None, description="The column and datatype from object map as string format: \"column, datatype\".")

class TriplesMapParsingList(BaseModel):
   parsings: List[TriplesMapParsing]