import type { RDF_Node } from "./RDF_Node";

export interface ClassModel {
  label?: RDF_Node;
  comment?: RDF_Node;
  created?: RDF_Node;
  modified?: RDF_Node;
  deleted?: RDF_Node;
  classURI: RDF_Node;
  subclassURI?: RDF_Node;
  image?: RDF_Node;
}

