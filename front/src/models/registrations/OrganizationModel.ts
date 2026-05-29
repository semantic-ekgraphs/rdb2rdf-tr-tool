import type { RDF_Node } from "../RDF_Node";


export interface OrganizationModel {
	label:       RDF_Node
	uri:         RDF_Node
	description: RDF_Node | null
   //
   homepage: RDF_Node | null
   acronym:  RDF_Node | null
}
