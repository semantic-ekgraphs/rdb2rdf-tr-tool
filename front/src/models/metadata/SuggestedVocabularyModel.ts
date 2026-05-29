import { type RDF_Node } from "../RDF_Node";

export interface SuggestedVocabularyModel {
   uri:       RDF_Node;
   explanation:       RDF_Node;
   isActive:       RDF_Node;
   namespace:       RDF_Node;
   prefix:       RDF_Node;
   property:       RDF_Node;
   rdfProperty:       RDF_Node;
   rdfProperty_label:       RDF_Node;
   suggested:       RDF_Node;
   suggested_label:       RDF_Node;
   vocabulary_label:       RDF_Node;
}
