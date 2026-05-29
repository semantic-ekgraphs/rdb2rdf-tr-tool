import type { RDF_Node } from "./RDF_Node";
import type { ResourceModel } from "./ResourceModel";

export interface DatasetModel extends ResourceModel {
	organization_uri: RDF_Node | null;
	delta_table_uri: RDF_Node | null
}