import { type RDF_Node } from "./RDF_Node";

export interface ResourceModel {
  uri?: RDF_Node;
  identifier?: RDF_Node;
  label: RDF_Node;
  title?: RDF_Node;
  description?: RDF_Node;
  image?: RDF_Node;
  comment?: RDF_Node;
  created_at?: RDF_Node;
  modified_at?: RDF_Node;
  deleted_at?: RDF_Node;
}

// export interface ContextModel {
//   p: RDF_Node;
//   o: RDF_Node;
//   label: RDF_Node;
//   same?: RDF_Node;
// }