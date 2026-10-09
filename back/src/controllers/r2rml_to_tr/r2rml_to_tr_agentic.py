from datetime import datetime
from crewai import Agent, Task, Crew
from llms import gpt_4o_mini_openai
# from knowledge.sources_of_knowledge  import transformation_rules_formalism
# from knowledge.sources_of_knowledge import knowledge_source_transformation_rule_patterns
from knowledge.sources_of_knowledge import knowledge_of_formal_entity_preserving_specification
from knowledge.sources_of_knowledge import knowledge_source_transformation_rule_patterns_v2
date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# from models.task_output import TriplesMapParsing, TriplesMapParsingList
from .model import TriplesMapParsing


agent_r2rml_to_tr = Agent(
   role="Principal Knowledge Engineer and Formal Semantic Web Architect",
   goal=(
      "Translate R2RML TriplesMaps into schema-grounded, mathematically rigorous "
      "Transformation Rules (TRs) by reconstructing the underlying semantic structure "
      "of the relational views, identifying precise pivot relations, determining entity-preservation "
      "compliance, and isolating structural relational paths as the final term of rule bodies."
   ),
   backstory=(
      "You are a world-class authority on semantic data integration frameworks and the creator of "
      "advanced relational-to-RDF compilation formalisms. You possess an unparalleled mastery of both "
      "relational engine internals (DDL, foreign-key traversals, query graph dependencies) and formal "
      "logic representations of Linked Data (CTR, DTR, OTR patterns). You reject blind syntactic "
      "translation and single-shot code generation; instead, you treat mapping migration as a complex, "
      "multi-step deductive reasoning task. You excel at auditing schemas to isolate identity pivots, "
      "characterizing complex n-ary associations or events as non-object-preserving mappings, designing "
      "elegant relational views to act as pseudo-pivots, and mapping semantic connectivity precisely via "
      "ordered chains of schema-validated foreign keys."
   ),
   verbose=True,
   memory=False,
   llm=gpt_4o_mini_openai,
)

# Step 1 - R2RML Parsing (this parsing transform R2RML in a table)
expected_csv_output_2 = f"""
A raw CSV (comma-separated values) document, where the first line is the header consisting solely of the following names:
{";".join(list(TriplesMapParsing.model_fields.keys()))}

Terminate the process if the header contains names other than those specified, and recreate the header with the correct names.

The output must be formatted according to the following specifications:
- Delimiter: Use semicolon (`;`) to separate values;
- Quoting & Escaping: Any field containing commas, line breaks, or quotation marks (such as SQL queries or transformation functions) MUST be wrapped entirely in double quotes (`"`). Internal double quotes must be escaped as `""`.
- Raw Output Only: The output must contain ONLY the raw CSV content. Do NOT wrap the output in Markdown code blocks (e.g., ```csv), and do NOT include introductory text, explanations, or metadata footnotes.

Generate an additional row for the R2RML mapping of type rr:subjectMap regarding the analyzed TriplesMap:
- For subjectMap, the mapped rdf is always 'rdf:type' and mapped object is 'None'.
"""

task_parsing_r2rml_to_table = Task(
   description="""
For each TriplesMap in the R2RML mappings extracts:
- Identifier of the triples mapping (rr:TriplesMap).
- Table name or SQL query in the logical table (rr:logicalTable).
- All SQL transformation functions (UPPER, LOWER, REPLACE, SUBSTRING, etc) applied to attributes in the SQL query. For example, from the SQL query `rr:logicalTable [ rr:sqlQuery \"\"\"SELECT empresa.id, UPPER(empregado.nome) AS nome FROM empresa INNER JOIN empregado ON empresa.empregado = empregado.id\"\"\" ] ;`, the transformation functions to be extracted is 'UPPER(empregado.nome)' — function and parameters. Repete the data extract for row with same triples_map_id.
- Selection conditions in an SQL query used to filter rows in a database table, employing operators such as equal to (=), not equal to (!= or <>), greater than/less than (< >), BETWEEN, IN, LIKE, IS NULL, IS NOT NULL, SIMILAR TO and all selection conditions operators known in SQL and relational database literature, as well as possible combinations thereof. Repete the data extract for row with same triples_map_id.
- Source R2RML mapping: rr:subjectMap or rr:predicateObjectMap.
- The RDF class and template URI of subject mapping (rr:subjecMap). If the RDF class is not included in the subject mapping, consider it to be None. The same applies if the template is not included.
- All RDF predicate, column and datatype of object mapped. The column and datatype from object map as string format: \"column, datatype\".
Input Context: 
- the R2RML mappings for the RDF view provided between <r2rml></r2rml>:
<r2rml>
{r2rml_mapping}
</r2rml>
Important Requirements:
- Analyze each Triples Map independently.
- Do not parse commented-out TriplesMap. Comments in R2RML start with #.""",
   expected_output=expected_csv_output_2,
   output_file=f"temp/r2rml_parsing_{date_now}.csv",
   markdown=False,
   agent=agent_r2rml_to_tr
)


# Step 2 - R2RML Parsed (this transforma parsed R2RML in TRs)

# ;hasURI predicate;URI Constructor predicate;Transformation Rules
# and corresponding URI_R Constructor predicate conform transformation rules patterns. 
# - Generate the Transformation Rules.
expected_csv_output_3 = f"""
A raw CSV (comma/semicolon-separated values) document, where the first line is the header consisting solely of the following names:
triples_map_id;pivot_relation;justify_preservation;hasURI predicate
Terminate the process if the header contains names other than those specified, and recreate the header with the correct names.
The output must be formatted according to the following specifications:
- Delimiter: Use semicolon (`;`) to separate values;
- Quoting & Escaping: Any field containing commas, line breaks, or quotation marks MUST be wrapped entirely in double quotes (`"`). Internal double quotes must be escaped as `\"`.
- Raw Output Only: The output must contain ONLY the raw CSV content. Do NOT wrap the output in Markdown code blocks (e.g., ```csv), and do NOT include introductory text, explanations, or metadata footnotes."""

task_compile_parsed_r2rml_to_transformation_rules = Task(
   description="""
Compile an Entity-Preserving R2RML mapping into as Transformation Rules analysing the content of parsed R2RML triples mapping. The R2RML-to-TR Compilation Process consists of the following subtasks:
- Identify the pivot relation from each triples map identifier analysing the logical table content of parsed R2RML triples mapping.
- Justify the entity preservation.
- Derive the hasURI predicate from the content of the parsed R2RML triples mapping following the hasURI predicate pattern.


Input Context: 
- the parsed R2RML mappings as table delimited between <EntityPreservingR2RMLMapping></EntityPreservingR2RMLMapping> tags:
<EntityPreservingR2RMLMapping>
{csv}
</EntityPreservingR2RMLMapping>
Important Requirements:
- Analyze each row, independently""",
   # context=[task_parsing_r2rml_to_table],
   expected_output=expected_csv_output_3,
   output_file=f"temp/parsed_r2rml_to_tr_260827.csv",
   markdown=False,
   agent=agent_r2rml_to_tr
)

# Versão usando conhecimento passado como arquivo
task_compile_r2rml_to_tr = Task(
   description="""You are given the following inputs:
   - the relational database schema: {rdb_schema}
   - the R2RML mappings defining the LinkedBrainz RDF view: {r2rml_mapping}
   - Additional integrity constraints: Assume that the attribute name is a unique identifier of the tag relation.

Task: Your task is to  transforms an Entity-Preserving R2RML mapping into a certified semantic specification expressed as Transformation Rules. The R2RML-to-TR Compilation Process consists of the following five steps (subtasks):
1. Identify the Pivot Relation and Verify Entity Preservation.
2. Derive and Validate the URI Constructor and corresponding hasURI predicate. 
3. Validate Pivot Relations and URI constructors
4. Generate and Validate the Transformation Rules.
5. Produce the Certified Semantic Specification.

Each Triples Map must be processed independently through these six steps. Transformation Rules must be generated only if the mapping is classified as entity-preserving and both the pivot relation and the URI constructor are successfully validated. Otherwise, the Triples Map must be classified as Manual Analysis Required, and no Transformation Rules should be generated.

Process Output
The output of the R2RML-to-TR Compilation Process is a structured JSON file containing the information extracted and generated during the six compilation steps for each R2RML Triples Map. The JSON file records the entity-preservation analysis, the identified pivot relation, the derived URI constructor and hasURI predicate, the validation results, and the generated Transformation Rules. For mappings that fail the validation process, the output records the corresponding validation errors and marks them as Manual Analysis Required, without generating Transformation Rules.

This JSON file provides a structured and machine-readable representation of the compilation results and serves as the input for the subsequent trigger-generation phase.
---
Step 1 — Identify the Pivot Relation and Verify Entity Preservation 
For each Triples Map, jointly identify its candidate pivot relation and determine whether the mapping preserves the identity of the RDF subject with respect to that relation.

First, analyze the R2RML logical table, Subject Map, and relational schema to identify the relation whose tuples determine the identity of the generated RDF subject. This relation is the candidate pivot relation. It must be selected from the semantics of the mapping and the schema constraints, rather than from the syntactic order of relations in the SQL query. In particular, do not assume that the first relation in the FROM clause is the pivot relation.

Then, verify the entity-preserving property with respect to the identified candidate. Check that:
1. each participating pivot tuple determines a single RDF subject;
2. each generated RDF subject corresponds to a single participating pivot tuple;
3. the Subject Map is functionally determined by the pivot tuple, directly or through functional foreign-key paths; and
4. SQL constructs such as aggregation, GROUP BY, DISTINCT, or UNION do not alter the required correspondence between pivot tuples and RDF subjects.

Record the candidate pivot relation, the supporting relational and R2RML evidence, and the result of each check. If no unique candidate can be identified, or if the entity-preserving property cannot be established, mark the mapping for human validation and report the unresolved condition.

Step 2 — Derive the URI Constructor and corresponding hasURI predicate
2.1 Derive the URI Constructor: 

URI_R(r,s) ≡ hasURI(template, <e1,...,en>, s)
where
-  template denotes the URI template extracted from the R2RML Subject Map, 
- <e1,...,en> is the ordered sequence of pivot-rooted attribute expressions corresponding to the placeholders of the R2RML URI template;, and 
- s is the URI associated with the pivot tuple r.
Pivot-rooted attribute expressions have one of the following forms:
ei ::= r.A
ei ::= [FK(r,t)/t.A]
where r.A denotes an attribute of the pivot tuple, and [FK(r,t)/t.A] denotes the value of attribute A obtained after following the foreign key FK from the pivot tuple r to tuple t.
For every URI component,
identify whether it is
a pivot attribute [r.A]
or
an FK-path attribute expression [ [FK(r,t)/t.A].]
The resulting URI constructor must preserve exactly the same placeholder order defined by the original R2RML template. In particular, verify that the placeholder values uniquely identify each participating pivot tuple. If uniqueness cannot be established from the schema or the mapping, classify the Triples Map as Manual Analysis Required.
2.2 Derive the corresponding predicate
hasURI(template, <e1,...,en>, s) iff
	s = instantiate(template, encode(eval(e1)), ..., encode(eval(en))).
by specifying
the URI template;
every FK navigation required to obtain placeholder values;
the concatenation order used to construct the final URI.
The instantiate function replaces each placeholder of the template with the encoded value obtained by evaluating the corresponding expression while preserving all constant fragments of the template.
Evaluation rules:
  eval(r.A) = r[A]
  eval([FK(r,t)/t.A]) = t[A], provided that FK(r,t) holds.

  
Step 3 — Validate the Pivot Relation and URI Constructor

Validate that the selected pivot relation correctly represents the identity of the RDF subject and that the derived URI constructor is semantically equivalent to the original R2RML subject map. Verify that every template placeholder is functionally determined by the pivot tuple, either directly or through a functional foreign-key path; that the original template fragments and placeholder order are preserved; and that evaluating the URI constructor produces exactly the same subject URI as the R2RML mapping for every logical-table row. Also verify that each generated URI corresponds to exactly one pivot tuple and that each participating pivot tuple generates at most one subject URI. If any condition cannot be established, classify the mapping as Manual Analysis Required.

Step 4 — Generate and Validate  the Transformation Rules
After the Triples Map has been classified as entity-preserving and both the pivot relation and the URI constructor have been successfully validated, generate the corresponding Transformation Rules. 
The Transformation Rules must be generated strictly according to the TR formalism provided in Section 3 of the paper [2027 EDBT]. Do not invent rule types, predicates, operators, or syntactic constructs that are not defined in the provided formalism. 
Rule Naming Convention
Assign a unique identifier to each generated Transformation Rule using the following format :psi_<pivot_relation>_<sequential_number> , where <sequential_number> is an integer assigned sequentially within the same pivot relation.
Example: psi_artist_1 psi_artist_2
The generated rules must:
- use the validated pivot relation as the pivot of the transformation;
- use the validated URI​ predicate to identify the RDF subject;
- preserve the semantics of the original R2RML Triples Map;
- translate each predicate-object map into the corresponding transformation rule;
- preserve all relevant join conditions, attribute expressions, constants, datatypes, language tags, and IRI-construction expressions;
- generate only rules that are supported by the relational schema and explicitly defined in the R2RML mapping.
- RelationalPath must be represented as an ordered list of foreign key constraints, RelationalPath=[fk1,…,fkn]\ where each fki​:
   - is a concrete foreign key constraint defined in the relational schema;
   - appears exactly with its original name as declared in the schema;
   - occupies the position corresponding to its traversal order along the relational path;
   - connects the pivot relation to the target relation;
   - must not be replaced by generic symbols such as FK, path, RelationalPath, relational_path_from_SQL, or by any other auxiliary predicate or invented notation.
   - The compilation process must preserve the exact sequence of foreign key constraints extracted from the relational schema. No abstraction, renaming, or simplification of the relational path is permitted.
Transformation Rules must be generated only when:
Entity-Preserving: YES
Pivot Relation Validation: VALIDATED
URI Constructor Validation: VALIDATED
Otherwise, no Transformation Rules must be generated, and the Triples Map must be reported as:  Manual Analysis Required. 
The Generation and Validation of the transformation rules is jointly processed in 3 sub steps 

4.1: Generate and Validate the Class Transformation rules
For each validated Entity-Preserving TriplesMap:
1. Instantiate the CTR template defined by the proposed formalism.
2. Reuse the validated compilation specification produced in the previous phase.
3. Populate the CTR template with:
   - the RDF class generated by the TriplesMap;
   - the validated pivot relation;
   - the validated URI constructor;
   - the corresponding hasURI predicate;
   - the selection condition, when specified by the R2RML mapping.
4. If no selection condition is defined, generate the CTR without a selection predicate.
5. Preserve the URI generation and selection condition exactly as specified by the R2RML mapping.
6. Do not introduce new predicates, notation, selection conditions, or auxiliary expressions beyond those defined by the formalism.
7. Produce one Class Transformation Rule (CTR) for each validated Entity-Preserving TriplesMap.
8. Validate the generated CTR Validate the generated CTR by comparing it with the corresponding R2RML TriplesMap, the validated compilation specification, and the formal CTR template.
Do not generate a new CTR unless a correction is explicitly requested. Do not introduce new predicates, notation, relations, attributes, or conditions.

VALIDATION CHECKS for CTR
1. Template conformance

 Verify that the generated rule is a valid instance of the formal CTR template.

2. RDF class

 Verify that the class in the head of the CTR is exactly the class generated by the corresponding R2RML TriplesMap.


3. Pivot relation

 Verify that the relation used in the body of the CTR is exactly the validated pivot relation.


4. URI constructor

 Verify that the CTR uses the validated URI constructor associated with the pivot relation.


5. URI equivalence

 Verify that the URI generated by the CTR is equivalent to the URI generated by the R2RML Subject Map, including:

   - URI template or constant;
   - referenced attributes;
   - placeholder order;
   - foreign-key paths, when applicable;
   - term type.
6. hasURI predicate

 Verify that the hasURI expression is instantiated exactly as defined in the validated compilation specification.


7. Selection condition

 Verify that the selection condition is included when specified by the logical table or SQL query of the R2RML mapping.

 If no selection condition exists in the mapping, verify that the CTR does not introduce one.

 Verify that the selection condition preserves the original relational semantics and does not omit, weaken, strengthen, or modify any predicate.


8. Schema consistency

 Verify that every referenced relation, attribute, foreign key, and path exists in the relational schema and is used with the correct name and direction.


9. No unsupported content

 Verify that the CTR does not contain:


   - invented predicates;
   - undefined notation;
   - additional joins;
   - additional filters;
   - omitted URI components;
   - attributes not functionally determined by the pivot relation.
10. Entity-preserving consistency

 Verify that the CTR remains consistent with the previously validated Entity-Preserving specification, including the one-to-one correspondence between pivot tuples and generated RDF subjects.
- For each failed check, identify the conflicting elements in the generated CTR, the R2RML mapping, or the validated specification.
- Return PASS only if all applicable checks pass. Otherwise, return FAIL.

  2.2: Generate and Validate the Object Transformation rules
For each Predicate-Object Map that generates an RDF resource, first classify the rule as either a Regular OTR or a Reification OTR.
Regular OTR
Generate a Regular OTR when the RDF object represents a target entity whose URI is generated by the URI constructor associated with a target CTR.
Validate that:
1. the rule conforms to the Regular OTR pattern;
2. the predicate is identical to the R2RML predicate;
3. the source-side atoms reproduce the RHS of the domain CTR;
4. the target-side atoms reproduce the RHS of the target CTR;
5. the source and target URI constructors preserve their respective R2RML term maps;
6. the relational path connects the source and target pivot relations;
7. every path step uses a schema-defined foreign key in the correct order and direction;
8. all applicable SQL selection conditions are preserved; and
9. the rule generates exactly the same subject-predicate-object triples as the R2RML Predicate-Object Map.
Reification OTR
Generate a Reification OTR when the RDF object is a URI obtained by reifying a relational value or the result of a relational transformation, rather than by applying the URI constructor of a target CTR.
Validate that:
1. the rule conforms to the Reification OTR pattern;
2. the predicate is identical to the R2RML predicate;
3. the subject-side atoms reproduce the RHS of the domain CTR;
4. the input attributes correspond exactly to the R2RML Object Map or logical-table expressions;
5. all required nonNull atoms are present;
6. all value-conversion and transformation operations are preserved in their original order;
7. the output variable of the transformation is the input variable of RDFURI;
8. RDFURI(u,o) produces the same RDF IRI as the R2RML Object Map;
9. no target CTR, target pivot relation, or canonical target URI constructor is introduced;
10. any relational path required to obtain the input values preserves the R2RML joins and schema foreign keys; and
11. the rule generates exactly the same subject-predicate-object triples as the R2RML Predicate-Object Map.
Return UNDETERMINED and request human validation when the OTR type, target entity, relational path, transformation, or URI reification cannot be established unambiguously.

2.3: Generate and Validate the Data Transformation rules
For each PredicateObjectMap that generates RDF literal:
1. Instantiate the DTR template defined by the proposed formalism.
2. Reuse the previously generated Class Transformation Rule (CTR) corresponding to the subject class.
3. Derive:
   - the target relation containing the attribute referenced by the ObjectMap;
   - the relational path from the pivot relation to the target relation, when the attribute is not stored in the pivot relation;
   - the transformation function specified by the ObjectMap, when applicable.
4. If the attribute belongs to the pivot relation, no relational path should be generated.
5. Represent relational paths exactly using the formal notation defined in Section 3. Do not introduce auxiliary predicates or alternative notation.
6. Preserve all transformation functions, datatypes, language tags, constants, templates, and literal values exactly as specified in the R2RML mapping.
7. Produce one Data Transformation Rule (DTR) for each PredicateObjectMap.
Validate the generated DTR by comparing it with the corresponding R2RML PredicateObjectMap, the validated subject CTR, the relational schema, and the formal DTR template.
Do not generate a new DTR unless a correction is explicitly requested. Do not introduce new predicates, notation, relations, attributes, paths, transformation functions, or conditions.

VALIDATION CHECKS for DTR 
1. Template conformance

 Verify that the generated rule is a valid instance of the formal DTR template.


2. Datatype property

 Verify that the predicate in the head of the DTR is exactly the datatype property specified by the corresponding R2RML PredicateObjectMap.


3. Subject construction

 Verify that the subject-side atoms of the DTR reproduce the right-hand side of the validated CTR for the domain class, including:


   - the pivot relation RDR_DRD​;
   - the URI constructor BD[d,s]B_D[d,s]BD​[d,s];
   - the selection condition, when applicable.
4. Target relation

 Verify that the relation containing the source value is correctly identified.

 If the referenced attribute belongs to the pivot relation, verify that the target relation is the pivot relation itself.

 If the referenced attribute belongs to another relation, verify that the correct target relation is used.


5. Relational path

 When the target relation differs from the pivot relation, verify that the relational path:


   - connects the pivot relation to the target relation;
   - exactly reproduces the join structure induced by the R2RML mapping;
   - uses only foreign keys defined in the relational schema;
   - preserves the correct order of traversals;
   - preserves the correct forward or inverse direction of each traversal;
   - does not omit, add, or replace any traversal.
6. If the target relation is the pivot relation, verify that no relational path is introduced.


7. Source attributes

 Verify that all attributes referenced by the DTR are exactly those specified by the R2RML ObjectMap or by the corresponding logical table expression.


8. Transformation expression

 Verify that the literal-producing expression exactly preserves the transformation specified by the ObjectMap, including, when applicable:


   - direct column access;
   - constants;
   - templates;
   - concatenation;
   - casts;
   - normalization functions;
   - user-defined transformation functions;
   - function names;
   - input arguments;
   - argument ordering.
9. Verify that no transformation is introduced when the ObjectMap defines only a direct column reference.


10. Literal construction

 Verify that the generated literal preserves all applicable R2RML term-map characteristics, including:


   - lexical value;
   - rr:termType;
   - rr:datatype;
   - rr:language;
   - constant literal value;
   - template structure and placeholder order.
11. Null semantics

 Verify that the DTR preserves the null-handling semantics of the R2RML mapping and does not generate an RDF literal when the corresponding ObjectMap would produce no RDF term.


12. Selection conditions

 Verify that all relevant selection conditions inherited from the subject CTR or required by the logical table are preserved.

 Verify that the DTR does not omit, weaken, strengthen, or introduce selection conditions.


13. Schema consistency

 Verify that every referenced relation, attribute, foreign key, and transformation input exists in the relational schema and is used with the correct name and type.


14. No unsupported content

 Verify that the DTR does not contain:


   - invented predicates;
   - undefined notation;
   - additional joins;
   - additional filters;
   - alternative relational paths;
   - invented attributes;
   - invented transformation functions;
   - omitted literal components;
   - datatype or language annotations not present in the mapping.
- For each failed check, identify the conflicting elements in the generated DTR, the R2RML PredicateObjectMap, the validated CTR, or the relational schema.
Do not classify an omitted optional component as an error when it is not required by the corresponding R2RML mapping

---
Important Requirements
   - Analyze each Triples Map independently.
   - Never infer URI templates that are not explicitly defined in the R2RML mapping.
   - Preserve the original placeholder order of the R2RML template.
   - Every URI component must be rooted at the pivot tuple.
   - Use FK-path attribute expressions whenever the value is obtained through a foreign-key navigation.
   - Be conservative. If the existence of a unique pivot relation cannot be established, classify the mapping as Manual Analysis Required.
""",
   expected_output="""Output Specification
- The output of the compilation process must be a semi-structured CSV file containing one entry for each R2RML Triples Map analyzed. Each entry must record the information extracted, derived, validated, and generated during the six compilation steps. 
For each Triples Map, the CSV output must include:
   - Triples Map Identifier: the identifier of the analyzed R2RML Triples Map.
   - Entity-Preserving: YES or NO.
   - Justification: an explanation of the entity-preservation classification.
   - Pivot Relation: the identified pivot relation.
   - Pivot Relation Validation: VALIDATED or FAILED, together with the corresponding validation evidence or errors.
   - R2RML Subject Template: the original URI template extracted from the R2RML Subject Map.
   - URI Constructor: the derived URI_R(r,s) predicate.
   - URI Components: the ordered list of pivot-rooted attribute expressions corresponding to the placeholders of the R2RML subject template.
   - hasURI Definition: the instantiated hasURI predicate, including the template and the ordered URI components.
   - URI Constructor Validation: VALIDATED or FAILED, together with the corresponding validation evidence or errors.
   - Transformation Rules: the TRs generated from the Triples Map, when the mapping and its derived components have been successfully validated.
   - Status: COMPILED or MANUAL_ANALYSIS_REQUIRED. 
If a Triples Map is not entity-preserving, or if the pivot relation or URI constructor cannot be successfully validated, the corresponding CSV entry must report the reason for failure, set the status to MANUAL_ANALYSIS_REQUIRED, and no Transformation Rules must be generated.
The CSV output must preserve the traceability between the original R2RML Triples Map, the results of the entity-preservation analysis, the derived pivot and URI specifications, the validation results, and the generated Transformation Rules.
- Generate a table containing one entry for each identified pivot relation. For each entry, include:
   - the name of the pivot relation;
   - the URI constructor derived from the corresponding R2RML Subject Map;
   - the formal definition of the associated hasURI function. 
- Generate a table containing one entry for each generated Transformation Rule, ordered by pivot relation. For each rule, report the main compilation artifacts, including:
   - Rule ID;
   - Rule type (CTR, OTR, or DTR);
   - Pivot relation;
   - Generated RDF class or property;
   - Rule Body
   - URI constructor(s);
   - hasURI predicate(s);
   - Source R2RML mapping (TriplesMap or PredicateObjectMap);
   - Relational path (when applicable);
   - Transformation expression (when applicable);
   - Selection condition (when applicable).

===========================================
Example:  Uri constructor for pivot table artist_tag 

R2RML: 
lb:artist_tag a rr:TriplesMap ;
  rr:logicalTable [rr:sqlQuery
    \"\"\"SELECT artist.gid, tag.name
       FROM artist_tag
         INNER JOIN artist ON artist_tag.artist = artist.id          INNER JOIN tag ON artist_tag.tag = tag.id\"\"\"] ;  
 rr:subjectMap [rr:template "http://musicbrainz.org/artist/\{gid\} #tag/\{name\}";
                 rr:class muto:Tagging] ;
  rr:predicateObjectMap
    [rr:predicate muto:taggedResource ;
     rr:objectMap lb:sm_artist] ,
    [rr:predicate muto:hasTag ;
     rr:objectMap lb:sm_tag] .
Pivot relation: artist_tag
URI predicate:
URI_artist_tag(r,s) ≡
hasURI(
  "http://musicbrainz.org/artist/\{gid\}#tag/\{name\}",
  <
    [artist_tag_fk_artist(r,a)/a.gid],
    [artist_tag_fk_tag(r,t)/t.name]
  >,
  s
)
Semantics:
s = instantiate(
      "http://musicbrainz.org/artist/\{gid\}#tag/\{name\}",
      encode(eval([artist_tag_fk_artist(r,a)/a.gid])),
      encode(eval([artist_tag_fk_tag(r,t)/t.name]))
	)
Assuming:
  a.gid = '8f3d4d52'
  t.name = 'Jazz'
the resulting URI is:
  http://musicbrainz.org/artist/8f3d4d52#tag/Jazz
This example illustrates that hasURI reproduces exactly the URI specified by the original R2RML template, while the values inserted into the placeholders are obtained through the pivot-rooted attribute expressions.
""",
   output_file=f"temp/r2rml_to_tr_compilation_{date_now}.csv",
   agent=agent_r2rml_to_tr
)



### ==========================================
### TRANSFORMATION RULES TEAM
### ==========================================
r2rml_to_tr_compilation_team = Crew(
   agents  = [agent_r2rml_to_tr],
   tasks   = [
      # task_parsing_r2rml_to_table,
      task_compile_parsed_r2rml_to_transformation_rules
   ],
   process = 'sequential',
   knowledge_sources=[knowledge_of_formal_entity_preserving_specification, 
                      knowledge_source_transformation_rule_patterns_v2]
)




# For each TriplesMap in the R2RML mappings extracts:
#    - Identifier of the TriplesMap analyzed;
#    - Logical table or extracted SQL query;
#    - Selection condition in the logical table or SQL query. A selection condition is everything after the WHERE clause in SQL query;
#    - Transformation functions such as LOWER, UPPER, REPLACE, COUNT, etc.
#    - Source R2RML mapping: subjectMap or predicateObjectMap;
#    - URI subject template from subjectMap;
#    - The class of subject mapping;
#    - The mapped RDF class or property;
#    - All predicate map from Predicate Object Map. Mapped object (column and datatype).

# - the output model between <output_model></output_model>
#    <output_model>
#    {output_model}
#    </output_model>



# Generate a separate line for each predicateObjectMap in the analyzed TriplesMap:
# - Place the SQL built-in transformation functions in the transformation_function field.

# For each subjectMap and predicateObjectMap do:
# - add the content of WHERE clause into the selection_condition field. Do not forget.
# - add the built-in transformation functions into the transformation_function field. Do not forget.
# - If the subjectMap has as value a constant of kind 'lb:sm_company' - defined in the R2RML as a triple 'lb:sm_company rr:template \"http://example.org/company/<id>\"' - replace the constant for it's literal value \"http://example.com/company/<id>\" to populate the uri_subject_template field.

# Example of expected CSV output format:
# {";".join(list(TriplesMapParsing.model_fields.keys()))}
# lb:department_mapping;"SELECT code, name FROM depart";None;None;rr:subjectMap;http://example.org/depart/<code>;ex:Department;rdf:type;None
# lb:department_mapping;"SELECT code, cost FROM depart";None;None;rr:predicateObjectMap;http://example.org/depart/<code>;ex:Department;ex:price;"cost, xsd:decimal"
# lb:company_mapping;"SELECT id, REPLACE(LOWER(company.name), 'test', 'exame') FROM company WHERE company.name IS NOT NULL";"REPLACE(LOWER(company.name), 'test', 'exame')";"company.name IS NOT NULL";rr:subjectMap;http://example.org/company/<id>;ex:Company;rdf:type;None
# lb:company_mapping;"SELECT id, REPLACE(LOWER(company.name), 'test', 'exame') FROM company WHERE company.name IS NOT NULL";"REPLACE(LOWER(company.name), 'test', 'exame')";"company.name IS NOT NULL";rr:predicateObjectMap;http://example.org/company/<id>;ex:Company;foaf:name;"name, xsd:string"
# lb:client_mapping;"SELECT id, name, postalCode FROM client WHERE client.name IS NOT NULL AND client.postalCode < 62800";None;"client.name IS NOT NULL AND client.postalCode < 62800";rr:predicateObjectMap;http://example.org/client/<id>;ex:Client;foaf:name;"name, xsd:string"


# - Delimiter: Use commas (`,`) to separate values;
# - If the subjectMap do not has the `rr:class` element, put the RDF class - i.e. the value defined for the `rr:object` of predicate Object Map - in the 'subject_class' column.
# {";".join(list(TriplesMapParsing.model_fields.keys()))}

# expected_csv_output = f"""
# A purely raw CSV (Comma-Separated Values) document, using the first line as a strict header containing the exact column names listed in the <output_model> model.

# The output must be formatted according to the following specifications:
# - Delimiter: Use semicolon (`;`) to separate values;
# - Quoting & Escaping: Any field containing commas, line breaks, or quotation marks (such as SQL queries or transformation functions) MUST be wrapped entirely in double quotes (`"`). Internal double quotes must be escaped as `""`.
# - Raw Output Only: The output must contain ONLY the raw CSV content. Do NOT wrap the output in Markdown code blocks (e.g., ```csv), and do NOT include introductory text, explanations, or metadata footnotes.

# Generate a separate line for the subjectMap in the analyzed TriplesMap:
# - For subjectMap, the mapped rdf is always 'rdf:type' and mapped object is None.
# - Do not parse commented-out TriplesMap. Comments in R2RML start with #.
# - If the subjectMap URI uses a variable template such as `lb:sm_company rr:template "http://example.com/company/<id>"`, do not use `lb:sm_company` to populate the URI subject template field... use `"http://example.com/company/<id>"` instead.

# Generate a separate line for each predicate map in the analyzed TriplesMap:
# - Do not forget: Place the extracted selection condition in the 'selection_condition' field, not in the 'transformation_function' field;
# - Do not forget: Place the extracted transformation function in the 'transformation_function' field.

# Example of expected CSV output format:
# triplesmap_id;transformation_functions
# lb:company_mapping;"SELECT id, name FROM company";None;None;rr:subjectMap;"http://musicbrainz.org/company/{id}";org:Company;rdf:type;None;None
# lb:company_mapping;"SELECT id, name FROM company WHERE company.name IS NOT NULL";"company.name IS NOT NULL";"REPLACE(name, 'test', 'exame'), LOWER(company.name)";rr:predicateObjectMap;"http://musicbrainz.org/company/{id}";org:Company;foaf:name;"name, xsd:string"
# lb:client_mapping;"SELECT id, name, postalCode FROM client WHERE client.name IS NOT NULL AND client.postalCode < 62800";"client.name IS NOT NULL AND client.postalCode < 62800";None;rr:predicateObjectMap;"http://musicbrainz.org/cliente/{id}";org:Client;vcard:postal-code;"postalCode, xsd:int"
# """




# ---------------------------------------------------------
# Adaptado por mim
# Arquivos fonte passados dinamicamente no kickoff como strings/contexto
inputs_context_object_preserving = """
Input Thecnical Context:
- Transformation Rules Patterns: {tr_patterns}
- R2RML mappings: {r2rml_mapping}
- Relational Database Schema: {rdb_schema}
- URI Predicates Definition: {uri_definition}
"""
# - Consider the Relational Database Schema, delimited by <rdb_schema></rdb_schema>,
# to identify pivot relations, joins, foreign-key paths and more:
#    <rdb_schema>{rdb_schema}<rdb_schema>
   
# - Consider the R2RML mappings delimited by <r2rml>:
# <r2rml>{r2rml_mapping}</r2rml>.

# - Consider the revised URI Predicates Definition delimited by <uri_predicates_definition> tag: 
# <uri_predicates_definition>{uri_definition}</uri_predicates_definition>.


list_triples_map_task = Task(
   description="""
      Extract all 'rr:TriplesMap' instances from the R2RML mappings below. 
List only the resource names (e.g., subjects defined with 'a' or 'rdf:type rr:TriplesMap'). 
Exclude any statements lacking these properties.

Input:
<R2RML mappings>
{r2rml_mapping}
</R2RML mappings>
   """,
   expected_output=(
      "A list of all TriplesMap names found"
   ),
   output_file=f"temp/object_preserving_{date_now}.txt",
   agent=agent_r2rml_to_tr
)


object_preserving_analysis_task = Task(
   description="""Analyze each R2RML mapping to determine whether it satisfies the entity-preserving property. 
If so, identify the pivot relation and derive the URI predicate responsible for generating 
the RDF resource identifiers. 


Phase 1: Object-preserving R2RML Mappings
An R2RML mapping is object-preserving when each RDF resource representing an instance of a class 
corresponds to exactly one tuple of a designated relation in the source schema, called the pivot relation, 
and each pivot tuple generates at most one RDF resource. In other words, the mapping preserves 
the identity of relational entities in the RDF view.

This interpretation is particularly natural in the context of schema mappings between 
relational databases and RDF. The purpose of such mappings is to establish semantic correspondences 
between constructs of the relational schema and constructs of the RDF vocabulary:
entity relations are mapped to RDF classes;
relationships are mapped to object properties;
attributes are mapped to datatype properties.

Consequently, the mapping is expected to preserve the identity of the entities already represented 
in the relational schema, rather than creating new entities through aggregation, grouping, or other 
analytical transformations. Each RDF instance therefore represents an existing relational entity, 
identified by a single pivot tuple, even when some of the values required to construct its URI 
are obtained from related tuples.

Although the R2RML language allows arbitrary SQL queries in logical tables, including queries involving 
GROUP BY, DISTINCT, UNION, or aggregation, such mappings generally define derived analytical views rather 
than semantic correspondences between relational entities and RDF classes. Therefore, while such mappings 
are valid R2RML specifications, they fall outside the scope of entity-preserving RDB2RDF mappings, which 
are the focus of the proposed framework.
For this reason, the transformation-rule formalism adopted in this work deliberately assumes 
object-preserving mappings. This assumption establishes a one-to-one correspondence between pivot tuples 
and RDF resources, which is the fundamental property on which the incremental maintenance theory and its 
correctness proofs are built. 

Antes mesmo de gerar as TRs, a LLM (ou um analisador) verifica se o mapeamento R2RML é object preserving:
existe uma pivot relation?
cada recurso RDF corresponde a exatamente uma tupla pivot?
não há agregações, GROUP BY, DISTINCT, UNION ou outras construções que eliminem a correspondência 1:1?
a definição da URI é funcionalmente determinada pela tupla pivot (mesmo que utilize atributos alcançados 
por caminhos PK/FK)?
The proposed compilation process assumes that the input R2RML specification is entity-preserving. 
If this assumption is violated, the problem is not merely syntactic but conceptual. In such cases, there 
is no semantics-preserving compilation into Transformation Rules, since the correspondence between 
relational entities and RDF resources is no longer one-to-one. Therefore, such mappings should be 
detected and reported for human analysis rather than automatically transformed by the compiler.

Identificação da Pivot relation

Um mapeamento R2RML é object preserving se pode ser associado com uma pivot relation.  
Nesse caso deve ser identificado qual a “pivot relation” do R2RML,  para depois então gerar a TRs usando 
a pivot relation. 

A pergunta que se deve fazer é: 
considerando um mapeamento R2RML, Existe uma relação R tal que cada tupla de R gera exatamente um recurso 
RDF e vice-versa?
Se existe a relação R, então pode ser definida uma CTR Ψ that maps tuples of a pivot relation 𝑅 into RDF 
instances of a class 𝐶. It establishes a semantic correspondence between a pivot tuple 𝑟 and an RDF 
resource 𝑥, such that each pivot tuple is associated with at most one RDF instance, and distinct pivot 
tuples generate distinct RDF resources. Thus, the mapping preserves the identity of relational entities 
in the RDB2RDF view. 
""",
   expected_output="""A CSV document whose content be a list of the 
   genereted URIs.   

   IMPORTANT INSTRUCTIONS:
- Do not invent relations or attributes that are not present in the R2RML.
- use the foreign keys to define relational paths
- Use the actual SQL joins in the R2RML mappings.
- Preserve the semantics of the R2RML mapping..
- When a literal value is produced from a column, use RDFLiteral or an equivalent built-in.
- When a value is transformed, such as LOWER, REPLACE, LIKE, or SIMILAR TO, represent this using auxiliary built-ins.
- Clearly separate clean object-preserving mappings from mappings that require adaptation.
- Prefer concise formal rules, but include enough explanation to justify the pivot relation and object-preserving classification.
""",
   output_file=f"temp/uris_{date_now}.csv",
   agent=agent_r2rml_to_tr
)


mapping_analysis_task = Task(
   description=(
      "Analyze provided R2RML mapping in the <R2RML_mappings> to determine if each rr:TriplesMap is 'object-preserving'.\n\n"
      "Criteria for an object-preserving mapping:\n"
      "- A single 'pivot relation' must exist where each tuple generates exactly one RDF resource and vice versa.\n"
      "- The mapping must NOT contain aggregations (e.g., GROUP BY, DISTINCT, UNION) that break the 1:1 correspondence.\n"
      "- The URI generation must be functionally determined by the pivot tuple, even if attributes are retrieved via PK/FK paths.\n\n"
      "Instructions:\n"
      "0. Evaluate all rr:TriplesMap counted in the task output before.\n"
      "1. Evaluate if each rr:TriplesMap satisfies the above criteria.\n"
      "2. If it is NOT object-preserving, report it as a violation for human analysis.\n"
      "3. If it IS object-preserving, identify the pivot relation and the URI predicate responsible for resource identification.\n"
      "4. If it IS object-preserving, generate the URI predicates and hasURI following the URI Predicates Definition taking the included example 1 and example 2.\n\n"
      "5. Consider the Transformation Rules Patterns in the context input.\n\n"
      "Input Thecnical Context:\n"
      "<R2RML_mappings>"
      "{r2rml_mapping}" \
      "</R2RML_mappings>\n"
      "<Transformation Rules Patterns>"
      "{tr_patterns}" \
      "</Transformation Rules Patterns>\n"
      "<Relational Database Schema>"
      "{rdb_schema}" \
      "</Relational Database Schema>\n"
      "<URI Predicates Definition>"
      "{uri_definition}" \
      "</URI Predicates Definition>"
   ),
   expected_output=(
      "A structured analysis report containing for all rr:TriplesMap counted in the task output before:\n"
      "- Boolean status: Is the mapping object-preserving? (Yes/No)\n"
      "- Pivot Relation: [Name of the relation, or 'None']\n"
      "- URI Predicate: [URI term map or predicate used for identification]\n"
      "- hasURI: [function]\n"
      "- Justification: A concise explanation of why it passed or failed the criteria."
   ),
   output_file=f"temp/uris_{date_now}.txt",
   context=[list_triples_map_task],
   agent=agent_r2rml_to_tr
)


task_extract_entity_preserving = Task(
   description="""Analyze each R2RML mappings below.
Write the resource names (e.g., subjects defined with 'a' or 'rdf:type rr:TriplesMap') and 
'Yes' next to the name of 'rr:TriplesMap' if the mapping preserves the tuple entity, or 'No' if it does not.
Justify observing the definition of the object-preserving strictly based on provided knowlegde sources.
Input:
<R2RML mappings>
{r2rml_mapping}
</R2RML mappings>
   
Strict Guardrails:
   - If no TriplesMap is found, simply write 'Not Found'.
   """,
   expected_output=(
      "A structured analysis report containing for all 'rr:TriplesMap'\n"
      "- Boolean status: Is the mapping object-preserving? (Yes/No)\n"
      "- TriplesMap: name of TriplesMap\n"
      "- Justification: A concise explanation of whether or not it constitutes object preservation, according to the definition of object preservation found in the knowledge sources."
   ),
   output_file=f"temp/entity_preserving_analysis_{date_now}.txt",
   agent=agent_r2rml_to_tr
)

