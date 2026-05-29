// export interface SavedQueryModel {
//   name: string;
//   body: string;
//   shared: string;
//   owner: string;
//   repository: string;
// }

import { RDF_Node } from "./RDF_Node";

export interface SavedQueryModel {
  uri: RDF_Node;
  identifier: RDF_Node;
  name: RDF_Node;
  label: RDF_Node;
  description: RDF_Node | null;
  repository: RDF_Node;
  generalizationClass: RDF_Node;
  sparql: RDF_Node; 
}

