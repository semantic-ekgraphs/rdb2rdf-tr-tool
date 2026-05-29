import { RDF_Node } from "../RDF_Node";

export interface SVOntologyModel {
   uri: RDF_Node;
   label: RDF_Node;
   description?: RDF_Node | null;
   /** qualidade */
   value_of_quality?: RDF_Node
   /** eventos */
   createdAt: RDF_Node;
   modifiedAt?: RDF_Node;
   deletedAt?: RDF_Node;
}