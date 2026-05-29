import axios from "axios";
import { TEXTS } from "../commons/constants";
// import { getLocalStorageLanguage } from '../commons/utils'
const api = axios.create({
  baseURL: "http://127.0.0.1:8000"
});
// api.defaults.headers.common["repository"] =  localStorage.getItem("repository") as string;
api.defaults.headers.common["repository"] =  TEXTS.NAME_OF_THE_REPOSITORY
// api.defaults.headers.common["language"] =  getLocalStorageLanguage();
api.defaults.headers.common["language"] =  "pt"
api.defaults.headers.common["Authorization"] = "Bearer " + localStorage.getItem("token");
api.defaults.headers.common["Access-Control-Allow-Origin"] = "*";

api.interceptors.response.use(
  function (response) {
    if (response.data.status_code === 409) {
      throw new Error(response.data.detail);
    }
    else {
      return response;
    }
  },
  function (error) {
    if (!error.response) {
      throw new Error("Servidor não disponível");
    } else if (error.response?.status === 400) {
      throw new Error("Solicitação incorreta");
    } else if (error.response?.status === 401) {
      throw new Error(error.response?.data);
    } else if (error.response?.status === 403) {
      api.defaults.headers.common["Authorization"] = "Bearer " + localStorage.getItem("token");
      window.location.reload();
    } else if (error.response?.status === 404) {
      api.defaults.headers.common["Authorization"] = "Bearer " + localStorage.getItem("token");
      throw new Error(error.response.data);
    } else if (error.response?.status === 409) {
      throw new Error(error.response.data);
    } else if (error.response?.status === 500) {
      throw new Error(error?.response.data);
    } else if (error.response?.status === 504) {
      throw new Error("Tempo esgotado");
    } else {
      api.defaults.headers.common["Authorization"] = "Bearer " + localStorage.getItem("token");
      throw new Error("Erro desconhecido");
    }
  }
);

export default api;