import os
from fastapi import HTTPException, status
import requests
from constants import Prefixies_SPARQL, HeadersOnRequests
from dotenv import load_dotenv
from constants import HeadersOnRequests
from constants import TXT_TEN_DASHES
from config.endpoint import Endpoint
load_dotenv()

ENVIROMENT = os.getenv("DEPLOY")
print('ENVIROMENT', ENVIROMENT)
linha = len(TXT_TEN_DASHES + " ACCESS " + TXT_TEN_DASHES)
console = lambda x: f"\n{'-'*linha}\n{TXT_TEN_DASHES} ACCESS {TXT_TEN_DASHES}\n{'-'*linha}\n+ {x}"
HEADERS_IMPORT = {"content-type": "application/json"}
get_url_import_server = lambda x: f"http://localhost:7200/rest/repositories/{x}/import/server" #local



class NamedGraphRepository:
	def __init__(self, repository:str, language:str): 
		self.this = "NamedGraphRepository"
		self.repo = repository
		self.lang = language
		self.endpoint = Endpoint(repository).MAIN

	def __find_resource_by_class_and_label(self, classe:str, label:str):
		try:
			print(console(f'__find_resource_by_class_and_label()'))
			sparql = f"""SELECT DISTINCT ?s 
			WHERE {{ 
			?s rdf:type {classe}; 
			rdfs:label "{label}"@{self.lang}.
			}}"""

			print('+ sparql: ', sparql)
			r = requests.get(self.endpoint, params={'query': Prefixies_SPARQL.ALL + sparql}, headers=HeadersOnRequests.GET)
			print('+ response', r.text)
			if((r.status_code == 200 or r.status_code == 201 or r.status_code == 204) 
				and len(r.json()['results']['bindings']) > 0):
				return {"code": 200, "message": "Existe"}
			else:
				return {"code": 200, "message": "Não Existe"}
		except Exception as err:
			return err

	def create_resource(self, query, classe:str, label:str):
		"""Função genérica para criar recursos. 
        Primeiro, verifica se o recurso da classe já existe com o label.
		---
		Parameters:
		-classe: uma classa da ontologia da visão semântica
		-label: o rótulo do recurso
		"""
		try:
			print(console(f'{self.this} create_resource()'))
			existe = self.__find_resource_by_class_and_label(classe, label)
			print('+ EXIST:', existe)
			if (existe["message"] == "Existe"):
				raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Um recurso dessa classe com esse label já existe!")
			
			r = requests.post(self.endpoint + "/statements", params=query, headers=HeadersOnRequests.POST)
			print('resposta', r)
			if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
				return {"code": 204, "message": "Criado com Sucesso!"}
			else:
				raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi criado!")
		except Exception as err:
			return err

	def create_resource_and_return_it(self, query, classe:str, label:str):
		"""Função genérica para criar recursos e retornar o recurso criado. 
        Primeiro, verifica se o recurso da classe já existe com o label.
		---
		Parameters:
		-classe: uma classa da ontologia da visão semântica
		-label: o rótulo do recurso
		"""
		try:
			print(console(f'{self.this}\n+ create_resource_and_return_it()'))
			# existe = find_resource_by_class_and_label(classe, label, self.repo, self.endpoint)
			# if (len(existe) > 0):
			# 	raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Um recurso dessa classe com esse label já existe!")
			
			r = requests.post(self.endpoint + "/statements", params=query, headers=HeadersOnRequests.POST)
			print('+ resposta:', r)
			if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
				# new_resource = find_resource_by_class_and_label(classe, label, self.repo, self.endpoint)
				return {"code": 204, "message": "Criado com Sucesso!"}
			# , "resource": new_resource[0]}
			else:
				raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi criado!")
		except Exception as err:
			return err  
		

	def retrieve_resources(self, query):
		"""Função genérica. 
        Entrada: sparql. Saída: json."""
		try:
			print(console(f'{self.this}.retrieve_resources()'))
			print('+ endpoint:', self.endpoint)
			result = requests.get(self.endpoint, params=query, headers=HeadersOnRequests.GET)
			print("+ result.status_code: ", result)
			if result.status_code == 200:
				return result.json()['results']['bindings']
		except Exception as err:
			return err
	
	def update_resource(self, query):
		try:
			print(console(f'{self.this}.update_resource()'))
			r = requests.post(self.endpoint + "/statements", params=query, headers=HeadersOnRequests.POST)
			print('\n+ response', r)
			if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
				return {"code": 204, "message": "Alterado com Sucesso!"}
			else:
				return {"code": 400, "message": "Não foi alterado!"}
		except Exception as err:
			return err
		
	def delete_resource(self, query):
		try:
			print(console(f'{self.this}.delete_resource()'))
			r = requests.post(self.endpoint + "/statements", params=query, headers=HeadersOnRequests.POST)
			print('\ response', r.status_code)
			if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
				return {"code": 204, "message": "Deletado com Sucesso!"}
			else:
				return {"code": 400, "message": "Não foi deletado!"}
		except Exception as err:
			return err

	def execute_sparql_query(self, query):
		"""Função genérica. 
        Entrada: sparql. Saída: json[]."""
		try:
			print(console(f'{self.this}\n+ execute_sparql_query()'))
			# print('+ query', query["query"])
			result = requests.get(self.endpoint, params=query, headers=HeadersOnRequests.GET)
			return result.json()['results']['bindings']
		except Exception as err:
			return err

	def execute_insert_sparql_query(self, query):
		"""Função genérica. 
        Entrada: sparql. Saída: json[]."""
		try:
			print(console(f'{self.this}\n+ execute_insert_sparql_query()'))
			r = requests.post(self.endpoint + "/statements", params=query, headers=HeadersOnRequests.POST)
			print('+ result:\n', r)
			print('+ result:\n', r.text)
			if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
				return {"code": 204, "message": "Criado com Sucesso!"}
			else:
				return {"code": 400, "message": "Não foi criado!"}
		except Exception as err:
			return err

	def check_if_rdf_file_exists_in_import_server_repository(self):
		try:
			message = None
			response_get = requests.get(get_url_import_server(self.repo), headers=HEADERS_IMPORT)
			for rdf in response_get.json():  # Aqui, tem-se todos os arquivos que estão na pasta graphdb-import
				# if (rdf["name"] == "create-suggested-terms.trig" and rdf['status'] == 'NONE'):
				# print('...', rdf['name'])
				if (rdf["name"] == "create-suggested-terms.trig"):
					message = {"message":True, "status": response_get.status_code}
					break
				else:
					message = {"message":False, "status": response_get.status_code}
			return message
		except Exception as err:
			print('ee', err)


	def import_rdf_file_from_graphdb_server_to_respository(self):
		"""Depois que o arquivo é montado e salvo, ele precisa ser importado pra dentro do repositório dos timelines."""
		response_post = ''
		try:
			print(console("+ import_rdf_file_from_graphdb_server_to_respository()"))
			body = f'{{ "fileNames": ["create-suggested-terms.trig"] }}'
			response_post = requests.post(get_url_import_server(self.repo), headers=HEADERS_IMPORT, data=body)
			print(f'+ response import rdf file: {response_post.status_code}')
			if response_post.status_code == 202:
				# delete_file_in_the_graphdb_server("create-suggested-terms.trig")
				return {"message":"Importado com Sucesso!", "status": response_post.status_code}
		except Exception as err:
			print('ee', err)

	def checking_if_exists(self, uri:str):
		try:
			print(console(f'+ checking_if_exists()'))
			sparql = Prefixies_SPARQL.ALL + \
			f"""SELECT * WHERE {{ 
			{{ <{uri}> ?p ?o . }}
			UNION
			{{ ?s ?p <{uri}> . }}
			}} LIMIT 1"""
			print('+ sparql: ', sparql)
			query = {'update': sparql}
			r = requests.get(self.endpoint, params=query, headers=HeadersOnRequests.GET)
			if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
				return {"code": 200, "message": "Existe", 'R': r.json()}
			else:
				return {"code": 200, "message": "Não Existe"}
		except Exception as err:
			return err