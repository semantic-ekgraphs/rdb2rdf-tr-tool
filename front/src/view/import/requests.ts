// import type { AxiosInstance } from "axios"
import api from '../../services/api'
// import type { ColumnModel } from "../../models/metadata/ColumnModel"

export async function createFile(file: FormData, datasetURI: string, date: string) {
   return api.post(`/importfile/?date=${date}&datasetURI=${datasetURI}`,
      file,
      {
         headers: {
            'accept': 'application/json',
            'Content-Type': 'multipart/form-data',
         },
      }
   )
}



// interface IColumn {
//    uri: string | null
//    label: string
//    name: string
//    dtype: string
//    is_active: boolean
// }

// export async function createDatasetColumn(data: IColumn, rawSchema: IColumn[]) {
//    const response = await api.post('/columns/', data)
//    console.log('CREATE RESPONSE -->', response.data)
//    const updateRawSchema: IColumn[] = rawSchema.map((r: IColumn) => {
//       if (r.name == response.data.resource.name) {
//          return { ...r, uri: response.data.resource.uri }
//       } else {
//          return r
//       }
//    })
//    return updateRawSchema
// }


interface IColumn {
   uri: string
   label: string
   name: string
   dtype: string
   is_active: boolean
}

export async function updateDatasetColumn(data: IColumn) {
   console.log('data.uri', data.uri)
   console.log('data.uri', encodeURIComponent(data.uri))
   const encoded_uri = encodeURIComponent(data.uri)
   const response = await api.put(`/columns/${encodeURIComponent(encoded_uri)}`, data)
   // const response = await api.put(`/columns/teste`, data)
   // console.log('UPDATE RESPONSE -->', response.data)
   // const updateRawSchema: ColumnModel[] = rawSchema.map((r: ColumnModel) => {
   //    if (r.name == response.data.resource.name) {
   //       return { ...r, uri: response.data.resource.uri }
   //    } else {
   //       return r
   //    }
   // })
   return response
}


// export async function softDeleteDatasetColumn(api: AxiosInstance, uri: string, data: IColumn, rawSchema: IColumn[]) {
//    const response = await api.delete(`/columns/?uri=${uri}`, data)
//    console.log('DELETE RESPONSE -->', response.data)
//    const updateRawSchema: IColumn[] = rawSchema.map((r: IColumn) => {
//       if (r.name == response.data.resource.name) {
//          return { ...r, uri: response.data.resource.uri }
//       } else {
//          return r
//       }
//    })
//    return updateRawSchema
// }