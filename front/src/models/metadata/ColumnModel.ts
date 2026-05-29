import { type RDF_Node } from "../RDF_Node";


export interface ColumnModel {
   uri:       RDF_Node;
   label:     RDF_Node;
   name:      RDF_Node;
   dtype:     RDF_Node;
   is_active: RDF_Node;
}
