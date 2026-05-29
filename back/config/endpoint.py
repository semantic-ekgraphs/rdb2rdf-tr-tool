import os
from dotenv import load_dotenv
from constants import TXT_TEN_DASHES
load_dotenv()

ENVIROMENT = os.getenv("DEPLOY")
print('ENVIROMENT', ENVIROMENT)
linha = len(TXT_TEN_DASHES + " ACCESS " + TXT_TEN_DASHES)
console = lambda x: f"\n{'-'*linha}\n{TXT_TEN_DASHES} ACCESS {TXT_TEN_DASHES}\n{'-'*linha}\n+ {x}"
HEADERS_IMPORT = {"content-type": "application/json"}
get_url_import_server = lambda x: f"http://localhost:7200/rest/repositories/{x}/import/server" #local


class Endpoint:
	def __init__(self, repository:str=None):
		self.IP =     f"http://localhost" if ENVIROMENT == "DEV" else "https://graphdb.arida.site"
		self.PORT =   "7200" if ENVIROMENT == "DEV" else ""
		self.SERVER =       f"{self.IP}:{self.PORT}"
		self.MAIN =         f"{self.SERVER}/repositories/{repository}"
		self.VEKG =         f"{self.SERVER}/repositories/VEKG"
		self.REPOSITORIES = f"{self.SERVER}/repositories"
		self.QUERY =        f"{self.SERVER}/rest/sparql/saved-queries"   