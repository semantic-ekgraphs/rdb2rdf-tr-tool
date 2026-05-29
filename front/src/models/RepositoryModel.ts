import { RDF_Node } from "./RDF_Node";

export interface RepositoryModel {
  id: RDF_Node;
  readable: RDF_Node;
  title: RDF_Node;
  uri: RDF_Node;
  writable: RDF_Node;
}