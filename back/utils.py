import os
from datetime import datetime
import shutil
import platform
platform.system()
from pathlib import Path
import pandas as pd
import json
import csv
from typing import List
from pydantic import BaseModel, Field
from models.task_output import TriplesMapParsingList
from controllers.r2rml_to_tr.model import TriplesMapParsing
from fastapi import UploadFile
from constants import TXT_TEN_DASHES
# from pydantic. import Optional

TypeOfFilesAllowedForImport = {
	"text/csv": "CSV",
	"text/xls": "XLS",
	"text/xlsx": "XLSX",
	"text/json": "JSON",
	"text/xml": "XML",
}

TypeOfFilesNotAllowedForImport = {
	"text/plain": ".txt",
	"text/x-bibtex": ".bib",
   "application/pdf": ".pdf",
   "application/postscript": ".eps",
   "application/msword": ".doc",
	"image/jpeg": ".jpeg",
	"image/png": ".png",
	"image/svg+xml": ".svg",
	"application/vnd.openxmlformats-officedocument.presentationml.presentation": ".ppt"
}



##################### 
### TASK INPUT READS
##################### 
def read_csv_and_transform_in_input_to_task(csv_path:Path, separator:str=";") -> str: 
	csv_content = ""
	csv_as_df = pd.read_csv(csv_path, sep=separator)
	for row in csv_as_df.to_string():
		csv_content += str(row)
	return csv_content

def read_txt_file(path_file:Path):
	with open(path_file, "r", encoding="utf-8") as file:
		return file.read()

def write_json_after_trigger_output_file(path_file:Path, content):
	with open(path_file, "w", encoding="utf-8") as file_of_trigger:
		file_of_trigger.write(content)


def write_csv_from_pydantic_(path_file:Path, content):
	with open(path_file, "w", encoding="utf-8") as csv_file:
		csv_file.write(content)

# 2. Função para exportar uma lista de modelos Pydantic para CSV
def export_pydantic_to_csv(caminho_arquivo: str, dados: List):
	if not dados:
		return

	
	# Extrai os nomes das colunas a partir do modelo Pydantic
	fieldnames = list(dados[0].model_fields.keys())
	
	with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		
		# Escreve o cabeçalho
		writer.writeheader()
		
		# Escreve os dados serializados
		for item in dados:
			writer.writerow(item.model_dump())

def cut_json_struture(dict_data):
	new_dict = {}
	for key, value_of_key in dict_data.items():
		new_dict[key] = {"description": value_of_key["description"]}
	return new_dict


def get_descriptions_of_a_pydantic_model(dict_model):
	new_dict = ""
	for key, value_of_key in dict_model.items():
		new_dict += "- " + value_of_key["description"] + "\n"
	return new_dict

# json packet
# json.load(): file -> dict
# json.loads(): str -> dict
# json.dumps(): dict -> json object
# json.dump(): dict -> file


def _get_col_dtype(col:pd.Series):
	"""
	Infer datatype of a pandas column, process only if the column dtype is object. 
	input:   col: a pandas Series representing a df column. 
	"""
	if col.dtype == "object":
		# try numeric
		try:
			col_new = pd.to_datetime(col.dropna().unique())
			return col_new.dtype
		except:
			try:
				col_new = pd.to_numeric(col.dropna().unique())
				return col_new.dtype
			except:
				try:
					col_new = pd.to_timedelta(col.dropna().unique())
					return col_new.dtype
				except:
					return "object"
	else:
		return col.dtype

def detect_csv_separetor(csv_file_path):
	print('+ detect_csv_delimiter():')
	count = 0
	lines = ""
	with open(csv_file_path, "r") as csv_file:
		for row in csv_file:
			lines += str(row)
			count += 1
			if count == 1:
				break
	sniffer = csv.Sniffer()
	return sniffer.sniff(lines, delimiters=[",", ";", "\t", "|"]).delimiter
		


DATAFRAME_COLUMN_INDEX = 1
TEMP_DIRECTORY = "temp"
def get_data_schema_from_the_new_imported_csv_file(csv_file: UploadFile):
	print('+ get_csv_schema()')
	try:
		print('+ csv_file:', csv_file.filename)
		with open("temp/" + csv_file.filename, "wb") as buffer:
			shutil.copyfileobj(csv_file.file, buffer)
		
		csv_separetor = detect_csv_separetor("temp/" + csv_file.filename)
		print(f"+ csv_separetor:", csv_separetor)

		df = pd.read_csv("temp/" + csv_file.filename, sep=csv_separetor)
		print('+ df.head()', df.head())


		# infer_type = lambda x: pd.api.types.infer_dtype(x, skipna=True)
		# df.apply(infer_type, axis=0)
		return [{
			"name": f"{col}", 
			"dtype": f"{_get_col_dtype(df[col])}",
			"isActive": False
			} for col in df.dtypes.index]
		
	except Exception as e:
		print('+ error:', e)
		raise Exception(f"Error reading CSV: {e}")
	


def filter_by_language(variable:str, language:str)->str:
	return f"""FILTER(LANG({variable})="{language}" || !LANGMATCHES(LANG({variable}), "*"))"""



def organize_properties_from_query_results(results):
	label, type, image, props  = {}, [], [], {'datatypes':[], 'objects':[]}
	
	for result in results:
		# OBTER O RÓTULO
		if result['p'] == {'type': 'uri', 'value': 'http://www.w3.org/2000/01/rdf-schema#label'}:
			label = result
		# OBTER O TIPO
		elif result['p'] == {'type': 'uri', 'value': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'}:
			type.append(result)
		# OBTER IMAGES
		elif result['p'] == {'type': 'uri', 'value': 'http://www.arida.ufc.br/VEKG#image'}:
			image.append(result)
		# OBTER AS PROPRIEDADES DE DADOS
		elif (result['o']['type'] == 'literal'):
			props['datatypes'].append(result)
		# OBTER AS PROPRIEDADES DE OBJETO
		elif result['o']['type'] == 'uri':
			print('p', result)
			props['objects'].append(result)
	if len(image) > 0:
		return {'label':label, 'type':type, 'image': image, 'props':props}
	else:
		return {'label':label, 'type':type, 'props':props}
	

GRAPHDB_IMPORT_DIRECTORY =  'C:' + os.sep + 'Users'+os.sep + os.getlogin() + os.sep + 'graphdb-import' if platform.system() == "Windows" else '.' + os.sep + 'root' + os.sep + 'graphdb-import'

def save_rdf_file_in_the_graphdb_server(data):
	print("+ save_rdf_file_in_the_graphdb_server()")
	file_name = "create-suggested-terms.trig"
	absolut_path = GRAPHDB_IMPORT_DIRECTORY + os.sep + file_name
	with open(absolut_path, 'w', encoding="utf-8") as file:
		file.write(data)


def delete_file_in_the_graphdb_server(file_name:str):
	if os.path.exists(f"{GRAPHDB_IMPORT_DIRECTORY}{os.sep}{file_name}"):
		os.remove(f"{GRAPHDB_IMPORT_DIRECTORY}{os.sep}{file_name}")




############## 
# LLM STUFFS
############## 

# def fin_relevant_context(question:str, top_k:int=3) -> Optional[str]:
# 	question_embedding = embedding_text(question)
# 	docs = load_all_documents()

# 	if not docs:
# 		return None
	
# 	similarity = [
# 		(doc_id, text, cosine_similarity(question_embedding, emb))
# 		for doc_id, text, emb in docs
# 	]
# 	similarity.sort(key=lambda x: x[2], reverse=True)
# 	top_docs = similarity[:top_k]




######################################## 
# FUNÇÕES DE DEBUG (DEVEM SER REMOVIDAS)
######################################## 
console_log = lambda file, data: f"\n{TXT_TEN_DASHES} {file} {TXT_TEN_DASHES} \n+ {data}"
info = lambda title, data: print(f"[INFO] + {title}: {data}")

def print_json_idented(data:json):
	print(json.dumps(data, indent=2))



def show_csv_file(csv_path):
	df = pd.read_csv(csv_path)
	print(df)