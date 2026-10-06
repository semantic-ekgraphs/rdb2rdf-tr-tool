from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field

# ==========================================
# 1. DEFINING OUTPUT MODELS WITH Pydantic
# ==========================================
class TriplesMapParsing(BaseModel):
   triples_map_id: str = Field(default=None, 
                               description="The rr:TriplesMap identifier", 
                               examples=["foaf:Person, <https://schema.org/Person>"])
   logical_table: str = Field(default=None, 
                              description="The SQL query or relation database in the rr:logicalTable")
   transformation_function: Optional[str] = Field(default=None, 
                                                  description="All SQL datatype transformation functions (like UPPER, LOWER, REPLACE, SUBSTRING, etc) applied to attributes in the extracted SQL query",
                                                  examples=["UPPER(client.surname)", "REPLACE(cliente.name, 'sr', 'Sr')"])
   selection_condition: Optional[str] = Field(default=None, 
                                              description="All Selection conditions in an extracted SQL query used to filter rows in a database relation, employing operators such as equal to (=), not equal to (!= or <>), greater than/less than (< >), BETWEEN, IN, LIKE, IS NULL, IS NOT NULL, SIMILAR TO and all selection conditions operators known in SQL and relational database literature, as well as possible combinations thereof")
   subject_template: str = Field(default=None, 
                                 description="The URI template defined for the rr:TriplesMap")
   subject_class: str = Field(default=None, 
                              description="The RDF class for rr:subjectMap")
   rdf_predicate: Optional[str] = Field(default=None, 
                                        description="The mapped RDF/OWL property")
   object_source: Optional[str] = Field(default=None, 
                                        description="The column from rr:objectMap")
   datatype: Optional[str] = Field(default=None, 
                                   description="The datatype from rr:objectMap")
   object_template: Optional[str] = Field(default=None, 
                                          description="The template URI from rr:objectMap")
   child_column: str = Field(default=None,
                             description="The child column in JOIN ... ON expressions")
   parent_column: str = Field(default=None, 
                              description="The parent column in JOIN ... ON expressions")
   foreign_key: Optional[str] = Field(default=None, 
                                      description="If SQL query contain at least one JOIN clause, the name of the CONSTRAINT within <Relational Schema> that relates the ALTER TABLE and the REFERENCE table in each JOIN in the extracted SQL query. Never invent or create CONSTRAINT names. Do not duplicate CONTRAINTS name.")

class TriplesMapParsingList(BaseModel):
   parsings: List[TriplesMapParsing]





class EntityPreservationRow(BaseModel):
   relation: str
   pivot_relation: str
   entity_preserving: bool
   uri_function: str
   relational_path: str
   issue: str = ""
   recommended_correction: str = ""


class TransformationRuleRow(BaseModel):
   rule_id: str
   rule_type: str
   pivot_relation: str
   relevant_relations: str
   uri_function: str
   predicate: str = ""
   object_function: str = ""
   relational_path: str = ""
   selection_condition: str = ""
   named_graph: str = ""