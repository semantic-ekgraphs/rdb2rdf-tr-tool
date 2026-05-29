import type { RDF_Node } from "./RDF_Node";


export interface DeltaTableModel {
   uri: RDF_Node;
   label: RDF_Node;
   description: RDF_Node | null;
   table_path: RDF_Node;
}

