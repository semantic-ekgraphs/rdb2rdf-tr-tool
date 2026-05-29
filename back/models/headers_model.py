from pydantic import BaseModel

class HeadersModel(BaseModel):
	"""Modelo de cabeçalho de requisição para receber o nome do repositório e o idioma desejado."""
	# Toda requisição deve ter
	repository: str = "EKG_SIGRAFO"
	language:   str = "pt"