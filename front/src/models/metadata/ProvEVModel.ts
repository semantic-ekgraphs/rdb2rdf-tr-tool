import { RDF_Node } from "../RDF_Node";



export interface ResourceProvenanceModel {
   class: RDF_Node | null;
   class_label: RDF_Node | null;
   ev: RDF_Node | null;
   ev_label: RDF_Node | null;
   ds: RDF_Node | null;
   ds_label: RDF_Node | null;
   mappings: RDF_Node | null;
   mappings_label: RDF_Node | null;
   subject: RDF_Node | null;
   subject_label: RDF_Node | null;
   pom: RDF_Node | null;
   pom_label: RDF_Node | null;
   namedGraph: RDF_Node | null;
   uv_specification: RDF_Node | null;
   uv_specification_label: RDF_Node | null;
   normalization_function: RDF_Node | null
   normalization_function_label: RDF_Node | null
}

export interface TripleProvenanceModel {
   class: RDF_Node | null;
   class_label: RDF_Node | null;
   ev: RDF_Node | null;
   ev_label: RDF_Node | null;
   ds: RDF_Node | null;
   ds_label: RDF_Node | null;
   mappings: RDF_Node | null;
   mappings_label: RDF_Node | null;
   subject: RDF_Node | null;
   subject_label: RDF_Node | null;
   pom: RDF_Node | null;
   pom_label: RDF_Node | null;
   namedGraph: RDF_Node | null;
   uv_specification: RDF_Node | null;
   uv_specification_label: RDF_Node | null;
   normalization_function: RDF_Node | null
   normalization_function_label: RDF_Node | null
}