import { RDF_Node } from "./RDF_Node";

export interface CompetenceQuestionModel {
  uri: RDF_Node;
  identifier: RDF_Node;
  label: RDF_Node;
  name: RDF_Node;
  description: RDF_Node | null;
  repository: RDF_Node;
  sparql: RDF_Node; 
}