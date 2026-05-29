import { RDF_Node } from "./RDF_Node";

export interface PropertyObjectEntity {
  p: RDF_Node;
  o: RDF_Node;
  l?: RDF_Node;
  same?: RDF_Node;
  label?: RDF_Node;
}