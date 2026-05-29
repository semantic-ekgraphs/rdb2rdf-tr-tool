import type { RDF_Node } from "../RDF_Node";


export interface DeltaTableModel {
	label:       RDF_Node
	uri:         RDF_Node
	description: RDF_Node | null
   //
	// organization: RDF_Node | null
	table_path: RDF_Node;
}
