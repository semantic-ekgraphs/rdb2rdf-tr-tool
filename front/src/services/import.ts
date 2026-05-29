import api from './api'

export async function createFile(file: FormData, datasetURI: string, date: string) {
   // export async function createFile(data: { path: string, data: string }) {
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