import { RDF_Node } from "../RDF_Node";


export interface ExportedViewModel {
   uri: RDF_Node;
   label: RDF_Node;
   description: RDF_Node | null;
}

// export interface ExportedSpecificationViewModel {
//    uri: RDF_Node;
//    label: RDF_Node;
//    name: RDF_Node;
//    description: RDF_Node | null;
//    subject_datasource: RDF_Node | null;
//    connection_url: RDF_Node | null;
//    username: RDF_Node | null;
//    password: RDF_Node | null;
//    jdbc_driver: RDF_Node | null;
// }