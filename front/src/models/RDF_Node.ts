/**Um nó nas respostas das consultas SPARQL 
 * vem nesse formato {type, value}.
 * Opcionalmente, vem { datatype } */
export interface RDF_Node {
  type: string,
  value: string,
  datatype?: string,
  'xml:lang'?: string
}