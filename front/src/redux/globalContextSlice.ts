import { createSlice } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'
import type { ClassModel } from '../models/ClassModel'
import { NUMBERS } from '../commons/constants'
import { getGlobalStateOfAppAtTheLocalStorage } from '../commons/utils'

export interface GlobalContextState {
  // A aplicação precisa dos seguintes atributos para identificar o atual contexto de exploração:
    // O idioma (pt, en), 
    // o tipo de visão (0==VU, 1==VE, 2==VF), 
    // o recurso (URI)
    // a classe (URI)
  language: string
  view: string | number
  exportedView?: string
  resourceURI: string
  initialResourceOfNavigation: string
  stack_of_resource_navigated: string[]
  classRDF?: ClassModel
}

const localStorageGlobalState = JSON.parse(getGlobalStateOfAppAtTheLocalStorage()) || undefined

const initialState: GlobalContextState = {
  language: localStorageGlobalState.language || "pt",
  view: localStorageGlobalState.view || NUMBERS.CODE_OF_UNIFICATION_VIEW,
  resourceURI: localStorageGlobalState.resourceURI || "",
  initialResourceOfNavigation: "",
  stack_of_resource_navigated: [],
  classRDF: localStorageGlobalState.classRDF || undefined,
  exportedView: localStorageGlobalState.exportedView || ""
}

export const contextSlice = createSlice({
  name: 'globalContext',
  initialState,
  reducers: {
    updateLanguage: (state, action: PayloadAction<string>) => {
      state.language = action.payload
    },
    updateView: (state, action: PayloadAction<string|number>) => {
      state.view = action.payload
    },
    updateExportedView: (state, action: PayloadAction<string>) => {
      state.exportedView = action.payload
    },
    updasteResourceURI: (state, action: PayloadAction<string>) => {
      state.resourceURI = action.payload
    },
    updateInitialResourceOfNavigation: (state, action: PayloadAction<string>) => {
      state.initialResourceOfNavigation = action.payload
    },
    pushResourceInStackOfResourcesNavigated: (state, action: PayloadAction<string>) => {
      state.stack_of_resource_navigated.push(action.payload)
    },
    removeResourceOfStackOfResourcesNavigated: (state) => {
      state.stack_of_resource_navigated.pop()
    },
    cleanStackOfResourcesNavigated: (state) => {
      state.stack_of_resource_navigated = []
    },
    updateClassRDF: (state, action: PayloadAction<ClassModel>) => {
      state.classRDF = action.payload
    },
    updateResourceAndView: (state, action: PayloadAction<{resource:string, view:string}>) => {
      state.resourceURI = action.payload.resource
      state.view = action.payload.view
    },
  },
})

// Action creators are generated for each case reducer function
export const { 
  updateLanguage, 
  updateView, 
  updateExportedView, 
  updasteResourceURI, 
  updateInitialResourceOfNavigation, 
  pushResourceInStackOfResourcesNavigated,
  removeResourceOfStackOfResourcesNavigated, 
  cleanStackOfResourcesNavigated,
  updateClassRDF, 
  updateResourceAndView } = contextSlice.actions

export default contextSlice.reducer