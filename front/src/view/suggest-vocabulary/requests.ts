// import type { SuggestedVocabularyModel } from '../../models/metadata/SuggestedVocabularyModel'
// import type { DatasetModel } from '../../models/DatasetModel'
import { double_encode_uri } from '../../commons/utils'
import type { RDF_Node } from '../../models/RDF_Node'
import type { ResponseDataModel } from '../../models/ResponseDataModel'
import api from '../../services/api'

interface ISuggestedProperty {
   uri: string
   label: string
   isActive: boolean
   property?: string
   prefix?: string
   namespace?: string
}

export async function updateSuggestedProperty(data: ISuggestedProperty) {
   const encoded_uri = encodeURIComponent(data.uri)
   const response = await api.put(`/datasets/suggested-property/${encodeURIComponent(encoded_uri)}`, data)
   return response
}


interface IResource {
   uri: RDF_Node,
   type: RDF_Node,
   label: RDF_Node,
   image: RDF_Node,
   properties: { objects: ResponseDataModel[] },
}
export async function suggestOntologizationVocabulary(data: IResource) {
   const ontologization = data.properties.objects.find(d => d.p.value == "http://www.arida.ufc.br/VEKG#hasOntologization")
   console.log('+ data:', ontologization?.o.value)
   const encoded_uri = double_encode_uri(ontologization?.o.value as string)
   const response = api.get(`/llm/suggest-ontologization-vocabulary/?ontologization_uri=${encoded_uri}`)
   return response
}