import { ManipulateType } from "dayjs";
import { LOCAL_STORAGE } from "./constants";

export function printt(text: string, value?: any): void {
	console.log(`*** ${text.toUpperCase()} ***`, value ? value : "")
}

export function double_encode_uri(normal_uri: string) {
	const decode_uri = encodeURIComponent(normal_uri)
	return encodeURIComponent(decode_uri)
}

export const changeBgColorCard = (idx: number, selectedIndex: number) => selectedIndex == idx ? "#edf4fc" : "None";


export function getPropertyFromURI(uri: string): string {
	if (uri) {
		const splitOne = uri?.split("/")
		const quantityOfTokens_1 = splitOne?.length
		const lastToken1 = splitOne[quantityOfTokens_1 - 1]
		let lastToken2 = lastToken1
		if (lastToken1.includes("#")) {
			const split2 = lastToken1.split("#")
			const quantityOfTokens_2 = split2?.length
			lastToken2 = split2[quantityOfTokens_2 - 1].toString()
		}
		return lastToken2;
	}
	return "";
}

export function getContextFromURI(uri: string): string {
	let lastToken2: string = ""
	// logo após de .org | .com |
	// logo antes de #
	if (uri && uri.includes("resource")) {
		const splitOne = uri.split("/resource/")
		const lastToken1 = splitOne[1]

		const split2 = lastToken1.split("/")
		lastToken2 = split2[0]
	}
	return lastToken2
}

export function getClassFromURI(uri: string): string {
	if (uri) {
		const splitOne = uri?.split("/")
		const quantityOfTokens_1 = splitOne?.length
		const lastToken1 = splitOne[quantityOfTokens_1 - 2]
		return `${lastToken1}`;
	}
	return "";
}

export function getClassAndIdentifierFromURI(uri: string): string {
	if (uri) {
		const splitOne = uri?.split("/")
		const quantityOfTokens_1 = splitOne?.length
		const lastToken1 = splitOne[quantityOfTokens_1 - 2]
		const lastToken2 = splitOne[quantityOfTokens_1 - 1]

		return `${lastToken1}/${lastToken2}`;
	}
	return "";
}



export function getIdentifierFromURI(uri: string): string {
	if (uri) {
		const splitOne = uri?.split("/")
		const quantityOfTokens_1 = splitOne?.length
		const lastToken2 = splitOne[quantityOfTokens_1 - 1]

		return `${lastToken2}`;
	}
	return "";
}


export function splitKGPrefixInNamedGraph(name: string): string {
	if (name) {
		const splitOne = name.split("_")
		const quantityOfTokens = splitOne.length
		const lastToken = splitOne[quantityOfTokens - 1]
		return lastToken;
	}
	return "";
}

// export function getAppHigienizadoFromClasse(uri: string): string {
//   const classe = getClassFromURI(uri)
//   const id = getIdentifierFromURI(uri)
//   switch (classe) {
//     case 'Estabelecimento':
//       return `http://www.sefaz.ma.gov.br/resource/AppEndereco/Estabelecimento/${id}`
//     case 'Empresa':
//       return `http://www.sefaz.ma.gov.br/resource/AppEndereco/Empresa${id}`
//     default:
//       return "";
//   }
// }

export function setContextLocalStorage(context: string): void {
	localStorage.setItem('context', context)
}

export function getContextLocalStorage(): string {
	return localStorage.getItem('context') || ""
}


export function setLocalStorageWithRepository(repository: string): void {
	window.localStorage.setItem('repository', repository)
}

export function getLocalStorageRepository(): string {
	return window.localStorage.getItem('repository') || ""
}


export function setLocalStorageWithLanguage(language: string): void {
	window.localStorage.setItem('language', language)
}

export function getLocalStorageLanguage(): string {
	return window.localStorage.getItem('language') || ""
}

export function setTypeClassLocalStorage(typeClass: string): void {
	localStorage.setItem('typeClass', typeClass)
}

export function getTypeOfClassOnLocalStorage(): string {
	return localStorage.getItem('typeClass') || ""
}


export function updateLocalStorageGlobalStateOfApplication(object: any) {
	const _currentGlobalContext = window.localStorage.getItem(LOCAL_STORAGE.GLOBAL_STATE_OF_APP) as string
	const updatedGlobalContext = { ...JSON.parse(_currentGlobalContext), ...object }
	window.localStorage.setItem(LOCAL_STORAGE.GLOBAL_STATE_OF_APP, JSON.stringify(updatedGlobalContext))
}

/** Get Global State Of Application at the Local Storage */
export function getGlobalStateOfAppAtTheLocalStorage(): string {
	return localStorage.getItem(LOCAL_STORAGE.GLOBAL_STATE_OF_APP) || '{ "state": "[NO LOCALSTORAGE]" }'
}

export function getDateFromInstantTimelin(instantURI: string): string {
	if (instantURI) {
		const lastToken1 = instantURI?.split("/Instant/")[1]
		/** NÃO PODE USAR SPLIT("-"). TEM ID QUE USA "-" */
		// let split2 = lastToken1.split("-") 

		const splitComAno = lastToken1.split('T')[0].split("-")
		const splitComHora = lastToken1.split('T')[1]
		const _d = splitComAno[splitComAno.length - 1]
		const _m = splitComAno[splitComAno.length - 2]
		const _y = splitComAno[splitComAno.length - 3]
		const data = `${_y}-${_m}-${_d}`
		const hora = decodeURIComponent("T" + splitComHora)
		const asDate = new Date(data + hora)
		return asDate.toLocaleDateString("pt-BR") + " " + asDate.toLocaleTimeString()
	}
	return "";
}


export function getPatternsClassRDF2GlobalContext(arrayNewClass: any[]) {
	const pattern_object_classRDF = {
		classURI: { type: 'url', value: arrayNewClass[0] },
		comment: { 'xml:lang': 'pt', type: 'literal', value: '' },
		label: { 'xml:lang': 'pt', type: 'literal', value: arrayNewClass[3] },
	}
	return pattern_object_classRDF
}



export function translate_frequency_of_change(frequencyOfChangeinText: string) {
	interface IFrequencyOFChange {
		number_of_days: number;
		type: ManipulateType
	}
	const frequencies_detailed: { [id: string]: IFrequencyOFChange } = {
		"<http://voag.linkedmodel.org/voag#Daily>": { number_of_days: 1, type: 'day' },
		"<http://voag.linkedmodel.org/voag#weekly>": { number_of_days: 7, type: 'day' },
		"<http://voag.linkedmodel.org/voag#Quarterly>": { number_of_days: 15, type: 'day' },
		"<http://voag.linkedmodel.org/voag#Monthly>": { number_of_days: 30, type: 'day' },
		"<http://voag.linkedmodel.org/voag#Yearly>": { number_of_days: 365, type: 'day' }
	}
	return frequencies_detailed[frequencyOfChangeinText]
}

export const retrive_frequency_of_chage = (rdf_frequency: string | null | undefined) => {
	switch (rdf_frequency) {
		case "<http://voag.linkedmodel.org/voag#Daily>":
			return "diário"
		case "<http://voag.linkedmodel.org/voag#weekly>":
			return "semanal"
		case "<http://voag.linkedmodel.org/voag#Quarterly>":
			return "quinzenal"
		case "<http://voag.linkedmodel.org/voag#Monthly>":
			return "mensal"
		case "<http://voag.linkedmodel.org/voag#Yearly>":
			return "anual"
		default:
			return "mensal"
	}
}