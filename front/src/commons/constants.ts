/**SEMANTIC WEB */
// const MOKG = "http://www.arida.ufc.org/ontologies/metadata-of-knowledge-graph#";
// export const VSKG = "http://www.arida.ufc.br/VSKG/";

export const TEXTS = {
	// APPLICATION: "be:ekg - Building and Exploring EKG.",
	NAME_OF_THIS_APPLICATION: "Sigrafo",
	DEPLOY: "DEV", /**options: DEV or PRODUCTION */
	CODE_OF_UNIFICATION_VIEW: "unification-view",
	CODE_OF_EXPORTED_VIEW: "exported-view",
	CODE_OF_FUSION_VIEW: "fusion-view",
	CODE_OF_METADATA_VIEW: "metadata-view",
	NAME_OF_THE_REPOSITORY: "EKG_SIGRAFO"
}

const URL_BASE_OF_THE_ARIDA = "http://www.arida.ufc.br"
// const HOME_PAGE_OF_ARIDA = "http://www.arida.ufc.br"

export const NAMESPACES = {
	RDF: "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
	RDFS: "http://www.w3.org/2000/01/rdf-schema#",
	OWL: "http://www.w3.org/2002/07/owl#",
	DC: "http://purl.org/dc/elements/1.1/",
	DCTERMS: "http://purl.org/dc/terms/",
	FOAF: "http://xmlns.com/foaf/0.1/",
	D2RQ: "http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#",
	DBO: "http://dbpedia.org/ontology/",
	VANN: "http://purl.org/vocab/vann/",
	WIKIDATA_ENTITY: "http://www.wikidata.org/entity/",
	WIKIDATA_PROPS: "http://www.wikidata.org/prop/direct/",
	WIKIBASE: "http://wikiba.se/ontology#",
	BLAZEGRAPH_BD: "http://www.bigdata.com/rdf#",
	SEFAZMA: "http://www.sefaz.ma.gov.br/ontology/",
	SCHEMA: "http://schema.org/",
	SKOS: "http://www.w3.org/2004/02/skos/core#",
	TIMELINE: "http://www.arida.ufc.br/ontologies/timeline#",
	BASE: "http://www.sefaz.ma.gov.br/resource/",
	VEKG: "http://www.arida.ufc.br/VEKG#",
	VSKG: "http://www.arida.ufc.br/VSKG#",
	DQV: "http://www.w3.org/ns/dqv#",
	VSKGR: `${URL_BASE_OF_THE_ARIDA}/VSKG/resource/`,
	META_EKG: `${URL_BASE_OF_THE_ARIDA}/meta-ekg/resource/`,
	ARIDA_RESOURCE_METADATA: `${URL_BASE_OF_THE_ARIDA}/resource/metadata/`,
	ARIDA_RESOURCE_KG_METADATA: `${URL_BASE_OF_THE_ARIDA}/resource/kg-metadata/`,
	MOKG: "http://www.arida.ufc.org/ontologies/metadata-of-knowledge-graph#"
}

export const PREFIXIES = {
	RDF: `PREFIX rdf: <${NAMESPACES.RDF}>\n`,
	RDFS: `PREFIX rdfs: <${NAMESPACES.RDFS}>\n`,
	OWL: `PREFIX owl: <${NAMESPACES.OWL}>\n`,
	D2RQ: `PREFIX d2rq: <${NAMESPACES.D2RQ}>\n`,
	DCT: `PREFIX dcterms: <${NAMESPACES.DCTERMS}>\n`,
	FOAF: `PREFIX foaf: <${NAMESPACES.FOAF}>\n`,
	DBO: `PREFIX dbo: <${NAMESPACES.DBO}>\n`,
	QDV: `PREFIX qdv: <${NAMESPACES.DQV}>\n`,
	VANN: `PREFIX vann: <${NAMESPACES.VANN}>`,
	WIKIDATA_ENTITY: `PREFIX wd: <${NAMESPACES.WIKIDATA_ENTITY}>\n`,
	WIKIDATA_PROPS: `PREFIX wdt: <${NAMESPACES.WIKIDATA_PROPS}>\n`,
	WIKIBASE: `PREFIX wikibase: <${NAMESPACES.WIKIBASE}>\n`,
	BLAZEGRAPH_BD: `PREFIX bd: <${NAMESPACES.BLAZEGRAPH_BD}>\n`,
	SEFAZMA: `PREFIX : <${NAMESPACES.SEFAZMA}>\n`,
	SKOS: `PREFIX skos: <${NAMESPACES.SKOS}>\n`,
	BASE: `PREFIX : <${NAMESPACES.BASE}>\n`,
	VEKG: `PREFIX vekg: <${NAMESPACES.VEKG}>\n`,
	VSKG: `PREFIX : <${NAMESPACES.VSKG}>\n`,
	VSKGR: `PREFIX : <${NAMESPACES.VSKGR}>\n`,
}

export const ENDPOINTS = {
	DEV: {
		MOKG: "http://localhost:7200/repositories/metagraph",
		INTERFACE_MASHUP: "http://localhost:7200/repositories/INTERFACE_MASHUP",
		VSKG: "http://localhost:7200/repositories/VSKG_TULIO",
		DBPEDIA: "https://dbpedia.org/sparql",
		WIKIDATA: "https://query.wikidata.org/sparql",
		OD_EKG_SEFAZMA: "http://localhost:7200/repositories/ONTOLOGIA_DOMINIO",
		GRAFOS_PRODUCAO: "http://localhost:7200/repositories/GRAFO_PRODUCAO_MATERIALIZADO",
	},
	PRODUCTION: {
		MOKG: "http://localhost:7200/repositories/metagraph",
		INTERFACE_MASHUP: "http://localhost:7200/repositories/INTERFACE_MASHUP",
		VSKG: "http://localhost:7200/repositories/VSKG_TULIO",
		DBPEDIA: "https://dbpedia.org/sparql",
		WIKIDATA: "https://query.wikidata.org/sparql"
	},

}

const REPOSITORY_ID = "EKG_CONTEXT"
const IP = "localhost"
const PORT = "7200"
export const NAMED_GRAPHS = {
	DATA: "",
	// KG_METADATA: "http://www.arida.ufc.br/metakg/named-graph/KG-METADATA",
	KG_MASHUP: `http://${IP}:${PORT}/repositories/${REPOSITORY_ID}/rdf-graphs/KG-MASHUP`,
	T_BOX: `http://${IP}:${PORT}/repositories/${REPOSITORY_ID}/rdf-graphs/KG_METADATA`,
	KG_METADATA_TBOX: `http://${IP}:${PORT}/repositories/${REPOSITORY_ID}/rdf-graphs/KG_METADATA_TBOX`,
	KG_METADATA_ABOX: `http://${IP}:${PORT}/repositories/${REPOSITORY_ID}/rdf-graphs/KG_METADATA_ABOX`,
	KG_TBOX: `http://${IP}:${PORT}/repositories/${REPOSITORY_ID}/rdf-graphs/KG_TBOX`

}

export const MAIN_PREFIXIES = `PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX vann: <http://purl.org/vocab/vann/>
    PREFIX mokg: <http://www.arida.ufc.org/ontologies/metadata-of-knowledge-graph#>
    PREFIX vskg: <http://www.arida.ufc.br/VSKG#>
    BASE <http://www.arida.ufc.org/resource/>
    `

export const PREFIXIES_SPARQL = {
	MOKG: "PREFIX mokg: <http://www.arida.ufc.org/ontologies/metadata-of-knowledge-graph#>\n",
	VSKG: "PREFIX vsgk: <http://www.arida.ufc.br/VSKG#>\n",
	DC: "PREFIX dc: <http://purl.org/dc/elements/1.1/>\n",
	DCT: "PREFIX dcterms: <http://purl.org/dc/terms/>\n",
	OWL: "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n",
	RDFS: "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n",
	RDF: "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n",
	FOAF: "PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n",
	DBO: "PREFIX dbo: <http://dbpedia.org/ontology/>\n",
	VANN: "PREFIX vann: <http://purl.org/vocab/vann/>",
	WIKIDATA_ENTITY: "PREFIX wd: <http://www.wikidata.org/entity/>\n",
	WIKIDATA_PROPS: "PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n",
	WIKIBASE: "PREFIX wikibase: <http://wikiba.se/ontology#>\n",
	BLAZEGRAPH_BD: "PREFIX bd: <http://www.bigdata.com/rdf#>\n"
}

export const WIKIDATA = {
	INSTANCIA_DE: "wdt:P31",
	PAIS: "wd:Q6256",
	ORGANIZATION: "wd:Q43229"
}



/**APPLICATION */
export const ROUTES = {
	HOME: "/",
	ABOUT: '/about',
	METAGRAPHS: "/metagrahs",
	METAGRAPHS_FORM: "/metagraph-form",

	ORGANIZATION_LIST: "/organizations",
	ORGANIZATION_FORM: "/organization-form",
	ORGANIZATION_DOC: "/organization-doc",

	ORGANIZATION_LIST_: "/organizations",
	ORGANIZATION_FORM_: "/organization-form",
	ORGANIZATION_DOC_: "/organization-doc",
	PERSONS: "/persons",
	USERS: "/users",

	ENDPOINT_CONFIG: "/config",
	REPOSITORY_LIST: "/repositories",
	SAVED_QUERY_LIST: "/saved-queries",
	SAVED_QUERY_FORM: "/saved-query-form",

	COMPETENCE_QUESTIONS_LIST: "/competence-questions",
	COMPETENCE_QUESTIONS_FORM: "/competence-questions-form/",

	DATASOURCE_LIST: "/datasources",
	DATASOURCE_FORM: "/datasources-form",
	DATASOURCE_FORM_RDB: "/datasources-form-rdb",
	DATASOURCE_FORM_csv: "/datasources-form-csv",
	DATASOURCE_PROPS_URI: "/datasources/:uri",

	PROVENANCE_LIST: "/provenances",
	PROVENANCE_FORM: "/provenances-form",
	PROVENANCE_FORM_RDB: "/provenances-form-rdb",
	PROVENANCE_FORM_csv: "/provenances-form-csv",
	PROVENANCE_PROPS_URI: "/datasources/:uri/provenances",
	PROVENANCE_EXT_SCHEMA: "/provenances/:uri/extract-schema",

	EXTRACT_CSV: "/datasources/extract",
	EXTRACT_CSV_URI: "/datasources/:uri/extract-schema",
	EXTRACT_DATA_CSV_URI: "/datasources/:uri/extract-data",
	// DATASOURCE_LIST_: "/datasources",
	// DATASOURCE_FORM_: "/datasources-form",

	TABLE_LIST: "/datasources/tables",
	TABLE_FORM: "/table-form",
	COLUMN_LIST: "/columns",
	COLUMN_FORM: "/column-form",
	TOPICS: "/topics",
	// NAVIGATION
	CLASSES: "/classes",
	CLASSES_VIEW: "/classes/view/",
	CLASSES_VIEW_VIEW: "/classes/view/:view/",
	CLASSES_VIEW_VIEW_ESV: "/classes/view/:view/esv/",
	CLASSES_VIEW_VIEW_ESV_ESV: "/classes/view/:view/esv/:esv",
	CLASSES_VIEW_VIEW_ESV_ESV_LANG: "/classes/view/:view/esv/:esv/lang",
	CLASSES_VIEW_VIEW_ESV_ESV_LANG_LANG: "/classes/view/:view/esv/:esv/lang/:lang",
	RESOURCES: "/resources",
	PROPERTIES: "/properties",
	PROPERTIES_URI: "/properties/:uri",
	TIMELINE: "/timeline",
	TIMELINE_URI: "/timeline/:uri",
	TIMELINE_RESOURCE: "/timeline?resource",
	// KG DE METADADOS
	MANAGE_METAGRAPH: '/manage-metagraph',
	MANAGE_META_DATASOURCES: '/manage-meta-datasources',

	SEMANTIC_VIEW: '/semantic-view',
	LOCAL_GRAPH_CONSTRUCT: '/localgraph-construct',
	LOCAL_GRAPH_FORM: '/localgraph-form',
	EXPORTED_SEMANTIC_VIEW_LIST: '/exported-semantic-views',
	EXPORTED_SEMANTIC_VIEW_FORM: '/exported-semantic-views-form',
	EXPORTED_VIEW_MANAGE: '/exportedview-manage',

	MAPPINGS_LIST: '/mappings',
	TRIPLES_MAP_FORM: '/triplesmap-form',

	META_MASHUP_LIST: '/meta-mashups',
	META_MASHUP_FORM: '/meta-mashup-form',
	META_MASHUP_MANAGE: '/meta-mashup-manage',
	META_MASHUP_SPARQP_QUERY_PARAMS_FORM: '/meta-mashup/sparql-query-params',

	METADATA_PROPERTIES: '/meta-properties',
	METADATA_PROPERTIES_URI: '/meta-properties/:uri',
	// LLM
	LLM: '/qa'
},

	USER_TYPE = {
		ADMIN: "ADMIN",
		COLAB: "COLAB"
	},

	METADATA_GRAHP_TYPE = {
		EKG: "EKG",
		MASHUP: "Mashup"
	};

/**Ontologia de Domínio */
export const VSKG_TBOX = {
	CLASS: {
		RELATIONAL_DATABASE: "http://rdbs-o#Relational_Database",
		CSV_FILE: "https://www.ntnu.no/ub/ontologies/csv#CsvDocument"
	},
	PROPERTY: {
		RDF_TYPE: "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		IS_A: `${NAMESPACES.RDF}type`,
		LABEL: `${NAMESPACES.RDFS}label`,
		NAME: `${NAMESPACES.FOAF}name`,
		DOMAIN: `${NAMESPACES.RDFS}domain`,
		RANGE: `${NAMESPACES.RDFS}range`,
		DC_IDENTIFIER: `${NAMESPACES.DC}identifier`,
		DC_DESCRIPTION: `${NAMESPACES.DC}description`,
		DCTERMS_DESCRIPTION: `${NAMESPACES.DCTERMS}description`,
		HAS_APPLICATION: `${NAMESPACES.VSKG}hasApplication`,
		// METADADOS GENÉRICOS
		THUMBNAIL: `${NAMESPACES.SCHEMA}thumbnail`,
		// FONTE DE DADOS
		DATASOURCE_TYPE: `${NAMESPACES.VSKG}datasourceType`,
		DB_USERNAME: `${NAMESPACES.D2RQ}username`,
		DB_PASSWORD: `${NAMESPACES.D2RQ}password`,
		DB_JDBC_DRIVER: `${NAMESPACES.D2RQ}jdbcDriver`,
		DB_CONNECTION_URL: `${NAMESPACES.D2RQ}jdbcDSN`,
		CSV_FILE_PATH: `${NAMESPACES.VSKG}csvFilePath`,
		/** PROVENIÊNCIA */
		HAS_PROVENANCE: `${NAMESPACES.VEKG}hasProvenance`,
		/** QUALIDADE */
		HAS_QUALITY_METADATA: `${NAMESPACES.DQV}hasQualityMetadata`
	},
	INDIVIDUAL: {
		NULL: `${NAMESPACES.VEKG}Null`
	},
	P_META_MASHUP_HAS_EXPORTED_VIEW: "http://www.arida.ufc.br/VSKG#hasExportedView"
}


/** Vocabulary expected by EKG Context Explorer tool
 * Some KG has dc:descrittion, other has dcterms:description
 * or rdfs:comment at least dc:description
 */
export const EKG_CONTEXT_VOCABULARY = {
	CLASS: {
		RELATIONAL_DATABASE: "http://rdbs-o#Relational_Database",
		CSV_FILE: "https://www.ntnu.no/ub/ontologies/csv#CsvDocument"
	},
	PROPERTY: {
		SAMEAS: `${NAMESPACES.OWL}sameAs`,
		RDF_TYPE: "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		IS_A: `${NAMESPACES.RDF}type`,
		LABEL: `${NAMESPACES.RDFS}label`,
		COMMENT: `${NAMESPACES.RDFS}comment`,
		NAME: `${NAMESPACES.FOAF}name`,
		DOMAIN: `${NAMESPACES.RDFS}domain`,
		RANGE: `${NAMESPACES.RDFS}range`,
		DC_IDENTIFIER: `${NAMESPACES.DC}identifier`,
		DC_DESCRIPTION: `${NAMESPACES.DC}description`,
		DC_TITLE: `${NAMESPACES.DC}title`,
		DCTERMS_DESCRIPTION: `${NAMESPACES.DCTERMS}description`,
		DCTERMS_TITLE: `${NAMESPACES.DCTERMS}title`,
		SKOS_DEFINITION: `${NAMESPACES.DC}definition`,
		HAS_APPLICATION: `${NAMESPACES.VSKG}hasApplication`,
		// METADADOS GENÉRICOS
		THUMBNAIL: `${NAMESPACES.SCHEMA}thumbnail`,
		IMAGE: `${NAMESPACES.SCHEMA}image`,
		// FONTE DE DADOS
		DATASOURCE_TYPE: `${NAMESPACES.VSKG}datasourceType`,
		DB_USERNAME: `${NAMESPACES.D2RQ}username`,
		DB_PASSWORD: `${NAMESPACES.D2RQ}password`,
		DB_JDBC_DRIVER: `${NAMESPACES.D2RQ}jdbcDriver`,
		DB_CONNECTION_URL: `${NAMESPACES.D2RQ}jdbcDSN`,
		CSV_FILE_PATH: `${NAMESPACES.VSKG}csvFilePath`,
		/** PROVENIÊCIA DA FONTE DE DADOS */
		HAS_PROVENANCE: `${NAMESPACES.VEKG}hasProvenance`,
		/** QUALIDADE */
		HAS_QUALITY: `${NAMESPACES.VEKG}hasQualityMetadata`,
		HAS_TIMELINE: `${NAMESPACES.TIMELINE}has_timeline`,
	},
	P_META_MASHUP_HAS_EXPORTED_VIEW: "http://www.arida.ufc.br/VSKG#hasExportedView"
}

export const DATASOURCE_TYPES = {
	// "Banco de Dados Relacional": `${VSKG}RelationalDataBase_DataSource`,
	"RDB": VSKG_TBOX.CLASS.RELATIONAL_DATABASE,
	// "No-SQL": `${VSKG}NoSQL_DataSource`,
	// "Triplestore": `${VSKG}Triplestore_DataSource`,
	"CSV": VSKG_TBOX.CLASS.CSV_FILE,
	// "RDF": `${VSKG}RDF_DataSource`
}

export const FONTE_PRINCIPAL = "http://www.sefaz.ma.gov.br/resource/Cadastro_SEFAZ-MA"
// export let APP_HIGIENIZACAO = {
//   Estabelecimento: "http://www.sefaz.ma.gov.br/resource/AppEndereco/Estabelecimento"
// }

export const NUMBERS = {
	TIME_OUT_FROM_REQUEST: 350,
	TABLE_WIDTH: 7,
	SIZE_TEXT_MENU_CONTEXT: "0.8rem",
	// SIZE_TEXT_MENU_CONTEXT: "1.2rem",
	SIZE_ICONS_MENU_CONTEXT: 19.4,
	PADDING_ITEMS_MENU_CONTEXT: 0.8,
	SCROOL_WINDOWS_Y: 5,
	IDX_TIMELINE: -4,
	IDX_FUSION_VIEW: -3,
	IDX_UNIFICATION_VIEW: -2,
	IDX_SELECTED_VIEW: -1,
	IDX_EXPORTED_VIEW: 0,
	CODE_OF_UNIFICATION_VIEW: 0,
	CODE_OF_EXPORTED_VIEW: 1,
	CODE_OF_FUSION_VIEW: 2,
	CODE_OF_METADATA_VIEW: 3,
	// GRAPHDB_BROWSER_CONFIG: "&config=636bec7f4b2446018b09e14ad8bd9117",
	GRAPHDB_BROWSER_CONFIG: "&config=27f4d973c994431b8fcf6b61ddbd7ff4",
	INICIAL_ROWS_PER_PAGE: 6,
	/** TAMANHOS DOS PAINEIS ESQUERDO E DIRETO DAS TELAS DE PROPRIEDADES DO RECURSO */
	SIZE_LEFT_PANEL_OF_PROPERTIES: 9.5,
	// SIZE_LEFT_PANEL_OF_PROPERTIES: 7,
	SIZE_RIGTH_PANEL_OF_PROPERTIES: 2.5,
	WIDTH_OF_P: TEXTS.DEPLOY == "PRODUCTION" ? 3.5 : 2.5,
	WIDTH_OF_O: TEXTS.DEPLOY == "PRODUCTION" ? 8.5 : 9.5,
	/** Propeties screen */
	FONTSIZE_PROPERTY: 14,
	// FONTSIZE_PROPERTY: 20,
	FONTSIZE_VALUE_PROPERTY: "0.54rem",
	// FONTSIZE_VALUE_PROPERTY: "0.7rem",
	FONTWEIGHT_PROPERTY: 550,

	BULLET_SIZE: 5,
	FONTSIZE_CLASS_IN_ELEVATION_PAPER: 18,
	// Layout
	DRAWER_WIDTH: 240,
	MINI_DRAWER_WIDTH: 100
}

// https://encycolorpedia.pt/1976d2
export const COLORS = {
	CINZA_01: "#c2cff1",
	CINZA_02: "#a3b7e9",
	CINZA_03: "#c2cff1",
	CINZA_04: "#5a8bda",
	AZUL_03: "#152b42",
	AZUL_04: "#1976d2",
	AZUL_05: "#1f4369",
	GREEN_01: "#00C200",
	YELLOW_01: "#e9da02",
	YELLOW_02: "#b5a84f",
	YELLOW_03: "#c2b242",
	RED_01: "#a83260",
	TO_DATA_SOURCES_IN_UNIFICATION_VIEW: ['#aca589', '#c2cff1', '#81a1e2', '', '', '', '', '', '', '', '', '', '', '', ''],
	METADATA_PROVENANCE: "#a01231",
	METADATA_QUALITY: "#4446c4",
	DIVERGENCE_ASTERISC: "#ed0215",
	DIVERGENCE_CHIP: '#d7c94b8f'
}

export enum Frequency {
	Daily = "diário",
	weekly = "semanal",
	Quartily = "quinzenal",
	Monthly = "mensal",
	yearly = "anual",
	UncertainFrequency = "indefenido"
}

export const LOCAL_STORAGE = {
	LANGUAGE: "language",
	REPOSITORY: "repository",
	CONTEXT: "context",
	GLOBAL_STATE_OF_APP: "globalStateOfApplication",
	TYPE_OF_CLASS: "typeClass"
}
export type typesOfView = "e" | "u" | "f" | "0" | "1" | "2" | "3";

