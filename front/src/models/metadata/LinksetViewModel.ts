import { RDF_Node } from "../RDF_Node";

export interface LinksetViewModel {
	uri: RDF_Node;
	label: RDF_Node;
	name: RDF_Node;
	description: RDF_Node | null;
	/** qualidade */
	value_of_quality: RDF_Node
	/** eventos */
	createdAt: RDF_Node;
  modifiedAt?: RDF_Node;
  deletedAt?: RDF_Node;
  
  linkPredicate: RDF_Node;
  hasLinkageRule: RDF_Node;
  sourceView: RDF_Node;
  targetView: RDF_Node;
}