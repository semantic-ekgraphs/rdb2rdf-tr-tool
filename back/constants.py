import os
from dotenv import load_dotenv
# from singleton import SingletonSpark
load_dotenv()
ENVIROMENT:str = os.getenv("DEPLOY")

class TEXTS:  
	def __init__(self): pass
	CODE_OF_GENERALIZATION_CLASS = "0"
	CODE_OF_EXPORTED_CLASS = "1"
	CODE_OF_EXPORTED_VIEW = "exported-view"
	CODE_OF_LINKSET_VIEW = "linkset-view"
	CODE_OF_UNIFICATION_VIEW = "unification-view"
	CODE_OF_FUSION_VIEW = "fusion-view"
	CODE_OF_METADATA_VIEW = "metadata-view"
	METADATA = "2"
	HOME_DIRECTORY = os.path.expanduser('~')
	TEN_DASHES = "_" * 10
	
class Prefixies:
	def __init__(self): pass
	""""""
	VSKG = "vskg:"
	VEKG = "vekg:"
	VOSV = "vosv:"

TXT_CODE_OF_GENERALIZATION_CLASS = "0"
TXT_CODE_OF_EXPORTED_CLASS = "1"
TXT_CODE_OF_EXPORTED_VIEW = "exported-view"
TXT_CODE_OF_LINKSET_VIEW = "linkset-view"
TXT_CODE_OF_UNIFICATION_VIEW = "unification-view"
TXT_CODE_OF_FUSION_VIEW = "fusion-view"
TXT_CODE_OF_METADATA_VIEW = "metadata-view"
TXT_METADATA = "2"
TXT_HOME_DIRECTORY = os.path.expanduser('~')
TXT_TEN_DASHES = "-" * 20
# TAGS PARA A DOCUMENTAÇÃO SWAGGER DA API
TAG_DATASETS = "Datasets"
TAG_SCHEMA = "Schema"
# REGISTRIONS
TAG_REGISTRATION = "Registration"
TAG_ORGANIZATION = "Organization"
TAG_DELTA_TABLE = "Delta Table"
TAG_IMPORT_FILE = "ImportFile"
TAG_USER = "User"
TAG_RESOURCE = "Resource"
# LLM
TAG_LLM = "LLM"
TAG_AGENTIC = "Agentic"

class NameSpaces:
	def __init__(self): pass
	# REUSO
	DC = "http://purl.org/dc/elements/1.1/"
	D2RQ = "http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#"
	DRM = "http://vocab.data.gov/def/drm#"
	DCAT = "http://www.w3.org/ns/dcat#"
	DCTERMS = "http://purl.org/dc/terms/"
	DQV = "http://www.w3.org/ns/dqv#"
	FOAF = "http://xmlns.com/foaf/0.1/"
	OWL = "http://www.w3.org/2002/07/owl#"
	PAV =  "http://purl.org/pav/"
	PROV =  "http://purl.org/pav/"
	RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	RDFS = "http://www.w3.org/2000/01/rdf-schema#"
	R2RML = "http://www.w3.org/ns/r2rml#"
	SCHEMA = "http://schema.org/"
	TIMELINE = "http://purl.org/NET/c4dm/timeline.owl#"
	VCARD = "http://www.w3.org/2006/vcard/ns#"
	VOID = "http://rdfs.org/ns/void#"
	VOAF = "http://purl.org/vocommons/voaf#"
	VANN = "http://purl.org/vocab/vann/"
	VOAG = "http://voag.linkedmodel.org/schema/voag#"
	XSD = "http://www.w3.org/2001/XMLSchema#"
	# NOVOS
	ARIDA = "http://www.arida.ufc.br/"
	ARIDA_ONTOLOGY = "http://www.arida.ufc.br/ontology/"
	ARIDA_RESOURCE = "http://www.arida.ufc.br/resource/"
	VEKG = "http://www.arida.ufc.br/VEKG#"
	VEKG_RESOURCE = "http://www.arida.ufc.br/VEKG/resource/"
	VSKG = "http://www.arida.ufc.br/VEKG#"
	VSKG_RESOURCE = "http://www.arida.ufc.br/VSKG/resource/"
	VOSV = "http://www.arida.ufc.br/vosv#"
	VOSV_RESOURCE = "http://www.arida.ufc.br/vosv/resource/"
	META_EKG = "http://www.arida.ufc.br/kg-metadata/resource/"
	RESOURCE_METADATA = "http://www.arida.ufc.br/resource/metadata/"
	SAVED_QUERY = "http://www.arida.ufc.br/ontologies/saved-query#"
	SEFAZMA = "http://www.sefaz.ma.gov.br/ontology/"


class Prefixies_SPARQL:
	def __init__(self): pass
	# REUSO
	# namespace = lambda p, n: f"PREFIX {p}: <{n}>\n"
	# RDF = f"PREFIX rdf: <{NameSpaces.RDF}>\n"
	# RDF = namespace("rdf", NameSpaces.RDF)
	RDF = f"PREFIX rdf: <{NameSpaces.RDF}>\n"
	RDFS = f"PREFIX rdfs: <{NameSpaces.RDFS}>\n"
	OWL = f"PREFIX owl: <{NameSpaces.OWL}>\n"
	FOAF = f"PREFIX foaf: <{NameSpaces.FOAF}>\n"
	SCHEMA = f"PREFIX schema: <{NameSpaces.SCHEMA}>\n"
	VCARD = f"PREFIX vcard: <{NameSpaces.VCARD}>\n"
	D2RQ = f"PREFIX d2rq: <{NameSpaces.D2RQ}>\n"
	DQV = f"PREFIX dqv: <{NameSpaces.DQV}>\n"
	DRM = f"PREFIX drm: <{NameSpaces.DRM}>\n"
	DCAT = f"PREFIX dcat: <{NameSpaces.DCAT}>\n"
	XSD = f"PREFIX xsd: <{NameSpaces.XSD}>\n"
	DC = f"PREFIX dc: <{NameSpaces.DC}>\n"
	DCTERMS = f"PREFIX dcterms: <{NameSpaces.DCTERMS}>\n"
	RR = f"PREFIX rr: <{NameSpaces.R2RML}>\n"
	TL = f"PREFIX tl: <{NameSpaces.TIMELINE}>\n"
	VSKG = f"PREFIX vskg: <{NameSpaces.VSKG}>\n"
	VOSV = f"PREFIX vosv: <{NameSpaces.VOSV}>\n"
	VEKG = f"PREFIX vekg: <{NameSpaces.VEKG}>\n"
	VOID = f"PREFIX void: <{NameSpaces.VOID}>\n"
	VOAG = f"PREFIX voag: <{NameSpaces.VOAG}>\n"
	VOAF = f"PREFIX voaf: <{NameSpaces.VOAF}>\n"
	VANN = f"PREFIX vann: <{NameSpaces.VANN}>\n"
	MOKG = "PREFIX mokg: <http://www.arida.ufc.br/metadata-of-knowledge-graph#>\n"
	SEFAZMA = "PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>\n"
	SFZ = "PREFIX sfz: <http://www.sefaz.ma.gov.br/ontology/>\n"
	SFZR = "PREFIX sfzr: <http://www.sefaz.ma.gov.br/resource/>\n"
	RFB = "PREFIX rfb: <http://www.sefaz.ma.gov.br/RFB/ontology/>\n"
	META_EKG = "PREFIX metaekg: <http://www.arida.ufc.br/meta-ekg/resource/>\n"
	PAV = f"PREFIX pav: <{NameSpaces.PAV}>\n"
	PROV = f"PREFIX prov: <{NameSpaces.PROV}>\n"
	# NOVOS
	W3C = RDF + RDFS + OWL + FOAF + VCARD + XSD
	DATASET = W3C + DCAT + DC + DCTERMS + DRM + SCHEMA + PROV + PAV + VEKG + VOAF + VANN + VOID
	ORGANIZATION = W3C + DC + SCHEMA + VEKG + VOSV
	SAVED_QUERY = f"PREFIX sq: <{NameSpaces.SAVED_QUERY}>\n"
	DUBLIN_CORE = DC + DCTERMS
	MAPPINGS = D2RQ + RR
	ALL = W3C + DUBLIN_CORE + MAPPINGS + VOID + DCAT + DRM + TL + VEKG + VOSV +  VSKG + VOAG + VOAF + VANN + SCHEMA + SFZ + SEFAZMA + SFZR + MOKG + DQV
	DATASOURCE = W3C + DUBLIN_CORE + MAPPINGS + DCAT + DRM + VEKG + VOSV + VSKG + VOAG + DQV
	PROVENANCE = RDF + RDFS + VEKG + DRM + DQV + PAV
	EXPORTED_VIEW = RDF + RDFS + VEKG + VOSV + VSKG + DRM + DC + DCTERMS + DQV
	MAPPING = RDF + RDFS + DC + VEKG + VOSV + VSKG + META_EKG
	META_MASHUP = RDF + RDFS + DC + META_EKG + VEKG + VOSV + VSKG
	QUERIES = SAVED_QUERY + RDF + RDFS + FOAF + DC
	COMPETENCE_QUESTION = VEKG + VOSV + VSKG + RDF + RDFS + FOAF + DC

class VoSV:
	def __init__(self):
		"""Classes e propriedades do VoSV (Vobaculary of Semantic View)"""
	P_IS_A = "rdf:type"
	P_LABEL = "rdfs:label"
	P_NAME = "foaf:name"
	P_DOMAIN = "rdfs:domain"
	P_RANGE = "rdfs:range"
	P_COMMENT = "rdfs:comment"
	P_IDENTIFIER = "dc:identifier"
	P_IMAGE = "vekg:image"
	P_DATE = "dc:date"
	P_DESCRIPTION = "dc:description"
	P_DCTERMS_DESCRIPTION = "dcterms:description"
	P_DCTERMS_CREATED = "dcterms:created"
	P_CREATED_AT = "vekg:createdAt"
	P_UPDATED_AT = "vekg:updatedAt"
	P_DELETED_AT = "vekg:deletedAt"
	P_HAS_APPLICATION = "vskg:hasApplication"
	#==========================
	# ORGANIZATION
	#==========================
	C_ORGANIZATION = "schema:Organization" # O vocabulário schema: foi adotado por ter outras propriedades que o foaf: não tem.
	P_ACRONYM = "vekg:acronym"
	#==========================
	# USER
	#==========================
	C_USER = "vosv:User" 
	C_PERSON = "foaf:Person" 
	# PROVENIÊNCIA
	P_PROV_CREATED_BY = "pav:createdBy"
	P_PROV_CREATED_ON = "pav:createdOn"
	P_PROV_IMPORTED_ON = "pav:importedOn"
	P_PROV_RETRIEVED_FROM = "pav:retrievedFrom"
	P_PROV_COMPETENCE = "vosv:competence"
	P_PROV_DELTA_TABLE_NAME = "vosv:deltaTableName"
	P_PROV_HAS_CHARGE = "vosv:hasCharge"
	#==========================
	# FONTE DE DADOS (Datasets)
	#==========================
	C_DATA_SOURCE = "dcat:Dataset" # Gosto de usar este
	C_DATA_ASSET = "drm:DataAsset"
	P_HOMEPAGE = "foaf:homepage"
	P_DATASOURCE_TYPE = "vosv:datasourceType"
	P_FREQUENCY_OF_CHANGE = "voag:frequencyOfChange"
	P_DB_HAS_QUALITY = "dqv:hasQualityMetadata"
	# BANCO DE DADOS RELACIONAL
	C_RDB = "http://rdbs-o#Relational_Database"
	C_RDB_TABLE = "vosv:Table"
	C_RDB_COLUMN = "vosv:Column"
	P_DB_HAS_CONNECTION = "vosv:hasConnection"
	C_CONNECTION = "vosv:Connection"
	P_DB_USERNAME = "d2rq:username"
	P_DB_PASSWORD = "d2rq:password"
	P_DB_HOST = "vosv:host"
	P_DB_JDBC_DRIVER = "d2rq:jdbcDriver"
	P_DB_CONNECTION_URL = "d2rq:jdbcDSN"
	P_DB_CONNECTION_DBNAME = "vosv:databaseName"
	# DOCUMENTO CSV
	C_CSV_FILE = "https://www.ntnu.no/ub/ontologies/csv#CsvDocument"
	C_DATA_SOURCE_PROVENANCE = "vosv:DataSourceProvenance"
	P_HAS_PROVENANCE = "vosv:hasProvenance"
	P_DB_HAS_TABLE = "vosv:hasTable"
	P_DB_HAS_COLUMN = "vosv:hasColumn"
	P_DB_COL_DATATYPE = "vosv:datatype"
	P_DB_COL_NULLABLE = "vosv:nullable"
	P_DB_COL_CARDINALITY = "vosv:cardinality"
	# FILE
	P_FILE_PATH = "vosv:filePath"
	P_FILE_SIZE = "vosv:fileSize"
	P_FILE_CONTENT_TYPE = "vosv:contentType"
	#==========================
	# CARGA DE DADOS
	#==========================
	C_DATA_LOADING = "vosv:DataLoading"
	P_HAS_DATA_LOADING = f'{Prefixies.VOSV}hasDataLoading'
	P_FROM_PROVENANCE = f'{Prefixies.VOSV}fromProvenance'
	# META-MASHUP
	P_MASHU_CLASS = "vskg:mashupClass" 
	P_META_MASHUP_EXPORTED_VIEW_URI = "vskg:exportedViewURI"
	P_META_MASHUP_LOCAL_ONTOLOGY_CLASS = "vskg:localOntologyClass"
	P_META_MASHUP_SQP_COLUMN = "vskg:sqpCol"
	# INDIVIDUALS
	I_NULL = "vekg:Null"
	C_META_EKG = "vskg:MetadataGraphEKG"
	#==========================
	# DATASET
	#==========================
	C_DATASET = "dcat:Dataset"  # Classe para definir as tabelas Delta (parquet)
	C_COLUMN = "vekg:Column"  # Classe para representar uma coluna de um schema de 
	C_VOCABULARY = "voaf:Vocabulary" 
	C_ONTOLOGIZATION = "vosv:Ontologization" 
	C_RDF_TERM = "vosv:RDFTerm" 
	C_RDF_PROPERTY = "vosv:RDFProperty" 
	C_SUGGESTED_PROPERTY = "vosv:SuggestedProperty" 
	C_ONTOLOGY = "owl:Ontology" 
	P_DTYPE = "vosv:dtype" # Diz o tipo de dados da coluna
	P_IS_ACTIVE = "vosv:isActive" # Usada para dizer que uma coluna foi selecionada entre as colunas do respectivo schema
	P_HAS_SCHEMA = "vosv:hasSchema" # Usara para ligar um arquivo a seu esquema de dados
	P_HAS_VOCABULARY = "void:vocabulary" 
	P_HAS_ONTOLOGIZATION = "vosv:hasOntologization" 
	C_DATA_SCHEMA = "drm:DataSchema" 
	P_HAS_COLUMN = "vosv:hasColumn" # Ligar um Schema a suas colunas
	#==========================
	# DELTA TABLE
	#==========================
	C_DELTA_TABLE = "vekg:DeltaTable"  # Classe para definir as tabelas Delta (parquet)
	#==========================
	# ONTOLOGIA DA VISÃO SEMÂNTICA
	#==========================
	C_SEMANTIC_VIEW_ONTOLOGY = "vosv:SemanticViewOntology"
	#==========================
	# VISÃO EXPORTADA
	#==========================
	C_LOCAL_GRAPH = "vosv:LocalGraph"
	C_EXPORTED_VIEW = "vosv:ExportedView"
	C_EXPORTED_SEMANTIC_VIEW = "vosv:ExportedSemanticView"
	C_META_MASHUP = "vskg:MetadataGraphMashup"
	C_MASHUP_VIEW_SPEC = "vskg:MashupViewSpecification"
	C_META_MASHUP_SPARQL_QUERY_PARAMS = "vskg:SparqlQueryParams"
	C_META_MASHUP_SPARQL_QUERY_PARAMS = "vskg:SparqlQueryParams"
	#====================
	# VISÃO DE LIGAÇÃO
	#====================
	C_LINKSET_VIEW = "vosv:LinksetView"
	#====================
	# VISÃO DE UNIFICAÇÃO
	#====================
	C_UNIFICATION_VIEW = "vosv:UnificationView"
	#====================
	# ASSERTIVA DE PROPRIEDADE DE FUSÃO
	#====================
	C_FUSION_VIEW = "vosv:FusionView"
	C_PFA = "vosv:PropertyFusionAssertion"
	P_RDF_PROPERTY = "vosv:rdfProperty"
	P_RDF_TERM = "vosv:rdfTerm"
	P_PFA_FUNCTION = "vosv:function"
	P_GENERALIZATION_CLASS = "vosv:generalizationClass"
	#====================
	# QUESTÃO DE COMPETENCIA
	#====================
	C_COMPETENCE_QUESTION = "vosv:CompetenceQuestion"
	P_SPARQL = "vosv:sparql"
	

class Tbox:
	def __init__(self):
		"""Mantém as classes e propriedades ontológicas"""
	PREFIX_VSKG = "vskg:"
	PREFIX_VEKG = "vekg:"
	PREFIX = "vekg:"
	P_IS_A = "rdf:type"
	P_LABEL = "rdfs:label"
	P_NAME = "foaf:name"
	P_DOMAIN = "rdfs:domain"
	P_RANGE = "rdfs:range"
	P_COMMENT = "rdfs:comment"
	P_IDENTIFIER = "dc:identifier"
	P_IMAGE = "vekg:image"
	P_DATE = "dc:date"
	P_DC_DESCRIPTION = "dc:description"
	P_DCTERMS_DESCRIPTION = "dcterms:description"
	P_DCTERMS_CREATED = "dcterms:created"
	P_CREATED_AT = "vekg:createdAt"
	P_UPDATED_AT = "vekg:updatedAt"
	P_DELETED_AT = "vekg:deletedAt"
	P_HAS_APPLICATION = "vskg:hasApplication"
	#==========================
	# ORGANIZATION
	#==========================
	C_ORGANIZATION = "schema:Organization" # O vocabulário schema: foi adotado por ter outras propriedades que o foaf: não tem.
	P_ACRONYM = "vekg:acronym"
	#==========================
	# USER
	#==========================
	C_USER = f"{PREFIX}User" 
	C_PERSON = "foaf:Person" 
	# PROVENIÊNCIA
	P_PROV_CREATED_BY = "pav:createdBy"
	P_PROV_CREATED_ON = "pav:createdOn"
	P_PROV_IMPORTED_ON = "pav:importedOn"
	P_PROV_RETRIEVED_FROM = "pav:retrievedFrom"
	P_PROV_COMPETENCE = f"{PREFIX}competence"
	P_PROV_DELTA_TABLE_NAME = f"{PREFIX}deltaTableName"
	P_PROV_HAS_CHARGE = f"{PREFIX}hasCharge"
	#==========================
	# FONTE DE DADOS (Datasets)
	#==========================
	C_DATA_SOURCE = "dcat:Dataset" # Gosto de usar este
	C_DATA_ASSET = "drm:DataAsset"
	P_HOMEPAGE = "foaf:homepage"
	P_DATASOURCE_TYPE = f"{PREFIX}datasourceType"
	P_FREQUENCY_OF_CHANGE = "voag:frequencyOfChange"
	P_DB_HAS_QUALITY = "dqv:hasQualityMetadata"
	# BANCO DE DADOS RELACIONAL
	C_RDB = "http://rdbs-o#Relational_Database"
	C_RDB_TABLE = f"{PREFIX}Table"
	C_RDB_COLUMN = f"{PREFIX}Column"
	P_DB_HAS_CONNECTION = f"{PREFIX}hasConnection"
	C_CONNECTION = f"{PREFIX}Connection"
	P_DB_USERNAME = "d2rq:username"
	P_DB_PASSWORD = "d2rq:password"
	P_DB_HOST = f"{PREFIX}host"
	P_DB_JDBC_DRIVER = "d2rq:jdbcDriver"
	P_DB_CONNECTION_URL = "d2rq:jdbcDSN"
	P_DB_CONNECTION_DBNAME = f"{PREFIX}databaseName"
	# DOCUMENTO CSV
	C_CSV_FILE = "https://www.ntnu.no/ub/ontologies/csv#CsvDocument"
	C_DATA_SOURCE_PROVENANCE = f"{PREFIX}DataSourceProvenance"
	P_HAS_PROVENANCE = f"{PREFIX}hasProvenance"
	P_DB_HAS_TABLE = f"{PREFIX}hasTable"
	P_DB_HAS_COLUMN = f"{PREFIX}hasColumn"
	P_DB_COL_DATATYPE = f"{PREFIX}datatype"
	P_DB_COL_NULLABLE = f"{PREFIX}nullable"
	P_DB_COL_CARDINALITY = f"{PREFIX}cardinality"
	# FILE
	P_FILE_PATH = f"{PREFIX}filePath"
	P_FILE_SIZE = f"{PREFIX}fileSize"
	P_FILE_CONTENT_TYPE = f"{PREFIX}contentType"
	#==========================
	# CARGA DE DADOS
	#==========================
	C_DATA_LOADING = f"{PREFIX}DataLoading"
	P_HAS_DATA_LOADING = f'{PREFIX}hasDataLoading'
	P_FROM_PROVENANCE = f'{PREFIX}fromProvenance'
	# META-MASHUP
	P_MASHU_CLASS = "vskg:mashupClass" 
	P_META_MASHUP_EXPORTED_VIEW_URI = "vskg:exportedViewURI"
	P_META_MASHUP_LOCAL_ONTOLOGY_CLASS = "vskg:localOntologyClass"
	P_META_MASHUP_SQP_COLUMN = "vskg:sqpCol"
	# INDIVIDUALS
	I_NULL = "vekg:Null"
	C_META_EKG = "vskg:MetadataGraphEKG"
	#==========================
	# DATASET
	#==========================
	C_DATASET = "dcat:Dataset"  # Classe para definir as tabelas Delta (parquet)
	C_COLUMN = "vekg:Column"  # Classe para representar uma coluna de um schema de 
	C_VOCABULARY = "voaf:Vocabulary" 
	C_ONTOLOGIZATION = f"{PREFIX}Ontologization" 
	C_RDF_TERM = f"{PREFIX}RDFTerm" 
	C_RDF_PROPERTY = f"{PREFIX}RDFProperty" 
	C_SUGGESTED_PROPERTY = f"{PREFIX}SuggestedProperty" 
	C_ONTOLOGY = "owl:Ontology" 
	P_DTYPE = f"{PREFIX}dtype" # Diz o tipo de dados da coluna
	P_IS_ACTIVE = f"{PREFIX}isActive" # Usada para dizer que uma coluna foi selecionada entre as colunas do respectivo schema
	P_HAS_SCHEMA = f"{PREFIX}hasSchema" # Usara para ligar um arquivo a seu esquema de dados
	P_HAS_VOCABULARY = "void:vocabulary" 
	P_HAS_ONTOLOGIZATION = f"{PREFIX}hasOntologization" 
	C_DATA_SCHEMA = "drm:DataSchema" 
	P_HAS_COLUMN = f"{PREFIX}hasColumn" # Ligar um Schema a suas colunas
	#==========================
	# DELTA TABLE
	#==========================
	C_DELTA_TABLE = "vekg:DeltaTable"  # Classe para definir as tabelas Delta (parquet)
	#==========================
	# ONTOLOGIA DA VISÃO SEMÂNTICA
	#==========================
	C_SEMANTIC_VIEW_ONTOLOGY = f"{PREFIX}SemanticViewOntology"
	#==========================
	# VISÃO EXPORTADA
	#==========================
	C_LOCAL_GRAPH = f"{PREFIX}LocalGraph"
	C_EXPORTED_VIEW = f"{PREFIX}ExportedView"
	C_EXPORTED_SEMANTIC_VIEW = f"{PREFIX}ExportedSemanticView"
	C_META_MASHUP = "vskg:MetadataGraphMashup"
	C_MASHUP_VIEW_SPEC = "vskg:MashupViewSpecification"
	C_META_MASHUP_SPARQL_QUERY_PARAMS = "vskg:SparqlQueryParams"
	C_META_MASHUP_SPARQL_QUERY_PARAMS = "vskg:SparqlQueryParams"
	#====================
	# VISÃO DE LIGAÇÃO
	#====================
	C_LINKSET_VIEW = f"{PREFIX}LinksetView"
	#====================
	# VISÃO DE UNIFICAÇÃO
	#====================
	C_UNIFICATION_VIEW = f"{PREFIX}UnificationView"
	#====================
	# ASSERTIVA DE PROPRIEDADE DE FUSÃO
	#====================
	C_FUSION_VIEW = f"{PREFIX}FusionView"
	C_PFA = f"{PREFIX_VSKG}PropertyFusionAssertion"
	P_RDF_PROPERTY = f"{PREFIX}rdfProperty"
	P_RDF_TERM = f"{PREFIX}rdfTerm"
	P_PFA_FUNCTION = f"{PREFIX_VSKG}function"
	P_GENERALIZATION_CLASS = f"{PREFIX_VSKG}generalizationClass"
	#====================
	# QUESTÃO DE COMPETENCIA
	#====================
	C_COMPETENCE_QUESTION = f"{PREFIX_VSKG}CompetenceQuestion"
	P_SPARQL = f"{PREFIX_VSKG}sparql"
	
	


class NamedGraph:
	def __init__(self, repository:str):
		# self.repo = repository
		self.PORT = "7200" if ENVIROMENT == "DEV" else ""
		self.IP = f"https://graphdb.arida.site" if ENVIROMENT == "DEV" else "https://graphdb.arida.site"
		self.repository = f"{self.IP}/repositories/{repository}"
		named_graph = lambda name: f"{self.repository}/rdf-graphs/{name}"

		self.TBOX = named_graph("TBOX")
		self.TBOX_METADATA = named_graph("TBOX_METADATA")
		self.KG_METADATA = named_graph("KG_METADATA")
		self.KG_QUERY = named_graph("KG_QUERY")
		self.KG_COMPETENCE_QUESTION = named_graph("KG_QUESTIONS")
		self.KG_PFA = named_graph("KG_PFA")


class HeadersOnRequests:
	def __init__(self): pass
	GET = 				 {"Accept": "application/sparql-results+json" }
	GET_JSON = 			 { "Accept": "application/json" }
	POST = 				 { "Content-type": "application/rdf+xml", "Accept": "application/json" }
	POST_QUERY =       { "Content-type": "application/json", "Accept": "*/*" }
	POST_KG_METADATA = { "Content-type": "text/turtle", "Accept": "application/json" }