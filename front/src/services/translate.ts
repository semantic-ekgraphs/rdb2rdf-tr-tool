export interface StringIndexObject {
   [key: string]: string;
}
export interface IStringIndexObject {
   [key: string]: StringIndexObject;
}


export const global_translate: IStringIndexObject = {
   "title": {
      "pt-BR": "Título",
      "pt": "Título",
      "en": "Title"
   },
   "label": {
      "pt-BR": "Label/Rótulo",
      "pt": "Label/Rótulo",
      "en": "Label"
   },
   "name": {
      "pt-BR": "Nome",
      "pt": "Nome",
      "en": "Name"
   },
   "description": {
      "pt-BR": "Descrição",
      "pt": "Descrição",
      "en": "Description"
   },
   "image": {
      "pt-BR": "Imagem",
      "pt": "Imagem",
      "en": "Image"
   },
   "hompage": {
      "pt-BR": "Site",
      "pt": "Site",
      "en": "Homepage"
   }
}

export const global_translate_for_list: IStringIndexObject = {
   "resource": {
      "pt-BR": "Recurso",
      "pt": "Recurso",
      "en": "Resource"
   },
   "noDataToShow": {
      "pt-BR": "Sem dados para mostrar",
      "pt": "Sem dados para mostrar",
      "en": "No data to show"
   },
   "rowsPerPage": {
      "pt-BR": "Linhas por página",
      "pt": "Linhas por página",
      "en": "Rows per page"
   },
   "searchByName": {
      "pt-BR": "Pesquise pelo nome do recurso",
      "pt": "Pesquise pelo nome do recurso",
      "en": "Search by resource name/label"
   }
}


export const global_translate_placeholder: IStringIndexObject = {
   "label": {
      "pt-BR": "ex: Brito Navegantes",
      "pt": "ex: Brito Navegantes",
      "en": "ex: Nasvile City"
   },
   "name": {
      "pt-BR": "ex: Brito",
      "pt": "ex: Brito",
      "en": "ex: Nasvile"
   },
   "description": {
      "pt-BR": "ex: Esta é a descrição sobre...",
      "pt": "ex: Esta é a descrição sobre...",
      "en": "ex: This describe any..."
   },
   "image": {
      "pt-BR": "ex: http://ibge/map/ce.png",
      "pt": "ex: http://ibge/map/ce.png",
      "en": "ex: http://nasville.org/map/view.jpeg"
   }
}


export const global_translate_for_butons: IStringIndexObject = {
   "send": {
      "pt": "Enviar",
      "en": "Senc"
   },
   "cancel": {
      "pt": "Cancelar",
      "en": "Cancel"
   },
   "delete": {
      "pt": "Deletar",
      "en": "Delete"
   },
   "update": {
      "pt": "Atualizar",
      "en": "Update"
   }
}