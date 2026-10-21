from typing import Optional, List, Any
from enum import Enum
from pydantic import BaseModel, Field


# ==========================================
# 1. DEFINING OUTPUT MODELS WITH Pydantic
# ==========================================
# object_source_type permite garantir que o LLM leu o esquema relacional, 
# por meio de verificação manual. Quando ele traz VARCHAR(255) NOT NULL
# essa informação não está no R2RML
class TriplesMapParsing(BaseModel):
   triples_map_id: str = Field(
      default=None, 
      description="The rr:TriplesMap identifier", 
      examples=["<#Person>, <PersonTriplesMap>, ex:PersonTriplesMap, <https://schema.org/Person>"]
   )
   logical_table:  str = Field(
      default=None, 
      description="The SQL query or relation database in the rr:logicalTable"
   )
   transformation_function: Optional[str] = Field(
      default=None, 
      description="All SQL datatype transformation functions (like UPPER, LOWER, REPLACE, SUBSTRING, etc) applied to attributes in the extracted SQL query",
      examples=["UPPER(client.surname)", "REPLACE(cliente.name, 'sr', 'Sr')"]
   )
   selection_condition: Optional[str] = Field(
      default=None, 
      description="All Selection conditions in an extracted SQL query used to filter rows in a database relation, employing operators such as equal to (=), not equal to (!= or <>), greater than/less than (< >), BETWEEN, IN, LIKE, IS NULL, IS NOT NULL, SIMILAR TO and all selection conditions operators known in SQL and relational database literature, as well as possible combinations thereof"
   )
   subject_template: str = Field(
      default=None, 
      description="The URI template defined for the rr:TriplesMap"
   )
   subject_class: str = Field(
      default=None, 
      description="The RDF class for rr:subjectMap"
   )
   rdf_predicate: Optional[str] = Field(
      default=None, 
      description="The mapped RDF/OWL property"
   )   
   object_source: Optional[str] = Field(
      default=None, 
      description="The column from rr:objectMap and the attribute between \{\} placeholder within rr:template in the rr:subject",
      examples=["id from ```rr:subjectMap [ rr:template \"http://example.com/person/\{id\}#_\" ] .```", "track_count from ```rr:objectMap [ rr:column \"track_count\" ; rr:datatype xsd:int ] ;```"]
   )
   object_source_type: Optional[str] = Field(
      default=None, 
      description="The data type of 'object_source' in the relational schema",
      examples=["INT", "SERIAL", "UUID", "VARCHAR", "SMALLINT", "INTEGER", "TIMESTAMP", "BOOLEAN", "VARCHAR(50)"]
   )
   attribute_condition: Optional[str] = Field(
      default=None, 
      description="The attribute condition",
      examples=["NOT NULL", "UNIQUE", "PRIMARY KEY"]
   )
   datatype: Optional[str] = Field(
      default=None, 
      description="The datatype from rr:objectMap"
   )
   term_type: Optional[str] = Field(
      default=None, 
      description="The R2RML property used to define whether the mapped RDF/OWL property should be an IRI, a blank node, or a literal",
      examples=["rr:IRI", "rr:BlankNode", "rr:Literal"]
   )
   object_template: Optional[str] = Field(
      default=None, 
      description="The template URI from rr:objectMap"
   )
   child_column: str = Field(
      default=None,
      description="The child column in JOIN ... ON expressions"
   )
   parent_column: str = Field(
      default=None, 
      description="The parent column in JOIN ... ON expressions"
   )
   foreign_key: Optional[str] = Field(
      default=None, 
      description=("If SQL query contain at least one JOIN clause, the name of the CONSTRAINT within <Relational Schema> that relates the ALTER TABLE and the REFERENCE table in each JOIN in the extracted SQL query. "
                  "Or if rr:objectMap contain rr:joinCondition, the FOREIGN KEY and REFERENCES. "
                  "Never invent or create CONSTRAINT names. "
                  "Do not duplicate CONTRAINTS name."
      )
   )

class TriplesMapParsingList(BaseModel):
   parsings: List[TriplesMapParsing]





class EntityPreservationRow(BaseModel):
   triples_map_id: str = Field(
      default=None, 
      description="The rr:TriplesMap identifier", 
      examples=["foaf:Person, <https://schema.org/Person>"]
   )
   relation: str = Field(
      default=None, 
      description="The relation",
      examples=["company → <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> / <https://schema.org/Organization>"]
   )
   pivot_relation: str = Field(
      default=None, 
      description="The pivot relation"
   )
   entity_preserving: bool = Field(
      default=None, 
      description="Verify whether entity identities are preserved. " \
         "Write the result by concatenating 'Yes' or 'No', ' - ', and the very short justification."
      )
   uri_function: str = Field(
      default=None, 
      description="Generates and validates URI construction functions"
   )
   relational_path: str = Field(
      default=None, 
      description="Analyzes relational paths", 
      examples=["fk_company_employee", "FK company(employee_id) REFERENCES employee(id)"]
   )
   issue: str = Field(
      default=None, 
      description="Detects constructs that violate the entity-preserving property"
   )
   recommended_correction: str = Field(
      default=None, 
      description="Recommended list of corrections."
   )


class TransformationRuleRow(BaseModel):
   triples_map_id: str = Field(
      default=None, 
      description="The rr:TriplesMap identifier", 
      examples=["foaf:Person, <https://schema.org/Person>"]
   )
   rule_id: str = Field(
      default=None, 
      description=("The transformation rule (TR) identifier, following the pattern 'tr-<pivot relation>-<sequential integer for the pivot relation>'"),
      examples=["tr-company-1", "tr-company-2", "tr-employee-1"]
   )
   rule_type: str = Field(
      default=None, 
      description=("Analyze the mapping logic and classify it precisely into one of the four formal categories:\n"
                           "- CTR;\n"
                           "- OTR (regular or reification);\n"
                           "- Local-DTR; or\n "
                           "- Path-DTR.\n")
      )
   pivot_relation: str = Field(
      default=None, 
      description="Identify the pivot relation that determines resource identity and subject URI generation"
   )
   uri_constructor: str = Field(
      default=None, 
      description="the derived URI constructor and hasURI predicate"
   )
   entity_preservation: str = Field(
      default=None, 
      description="records the entity-preservation analysis"
   )
   formula: str = Field(
      default=None, 
      description=" Construct the formal TR specification using the appropriate Global URI Predicates and auxiliary built-ins"
   )


class TransformationRuleValidation(BaseModel):
   rule_id: str = Field(
      default=None, 
      description="The transformation rule (TR) identifier"
   )
   pivot_relation_audit: str = Field(
      default="FAIL", 
      description="Verification against source metadata.S",
      examples=["PASS", "FAIL"]
   )
   relational_path_audit: str = Field(
      default="FAIL", 
      description="Verification of foreign key join paths",
      examples=["PASS", "FAIL"]
   )
   uri_constructor_audit: str = Field(
      default="FAIL", 
      description="Verification of URI templates and namespace predicates",
      examples=["PASS", "FAIL"]
   )
   predicate_selection_conditions: str = Field(
      default="FAIL", 
      description="Verification that SQL selection logic and RDF predicates match the original mapping",
      examples=["PASS", "FAIL"]
   )
   semantic_consistency_status: str = Field(
      default="FAIL", 
      description="Final verification against original R2RML semantics",
      examples=["PASS", "FAIL"]
   )
   issue: str = Field(
      default=None, 
      description="Description of the semantic deviation from original R2RML mappings"
   )
   required_correction: str = Field(
      default=None, 
      description="Recommended adjustment to achieve full semantic equivalence"
   )