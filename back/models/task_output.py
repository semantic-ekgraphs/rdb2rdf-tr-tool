from typing import Optional, List
from pydantic import BaseModel, Field

# ==========================================
# 1. DEFINING OUTPUT MODELS WITH Pydantic
# ==========================================
# Estrutura de dados de uma Regra de Transformação
class TransformationRuleModel(BaseModel):
   identifier:      str = Field(..., description="Identificador da regra de transformação. Exemplo 'tr_<relação_pivô>_<número_sequencial>'.")
   tr_type:         str = Field(..., description="Tipo de transformação: CTR, Local-DTR, Path-DTR ou OTR.")
   formula:         str = Field(..., description="A formula regra de transformação (TR) final gerada.")
   relational_path: str = Field(..., description="O caminho relacional posicionado como o último termo do corpo da regra.")


class TriplesMapParsing(BaseModel):
   triples_map_name:  str = Field(..., description="Name of the TriplesMap analyzed.")
   sql_logical_table: str = Field(..., description="Logical table or extracted SQL query. SQL Source.")
   pivot_relation:    str = Field(..., description="Identified pivot relation.")
   # mapping_type:    str = Field(..., description="Mapping type: CTR, Local-DTR, Path-DTR, OTR, or derived-pivot case.")
   entity_preserving: bool = Field(..., description="Classify if is Entity-preseving or Non-entity-preserving.")
   generated_trs:     List[TransformationRuleModel] = Field(..., description="Gererated Transformation Rules")

class TriplesMapParsingList(BaseModel):
   parsings: List[TriplesMapParsing]


# ==========================================
# 1. DEFINIÇÃO DOS MODELOS DE SAÍDA COM Pydantic
# ==========================================

# class TriplesMapAnalysis(BaseModel):
#    triples_map_name: str = Field(..., description="Nome do R2RML TriplesMap analisado.")
#    sql_logical_table: str = Field(..., description="Tabela lógica ou consulta SQL extraída.")
#    identified_pivot_relation: str = Field(..., description="Relação pivô identificada.")
#    mapping_type: str = Field(..., description="Tipo do mapeamento: CTR, Local-DTR, Path-DTR, OTR ou derived-pivot case.")
#    entity_preserving_classification: str = Field(..., description="Classificação de preservação de entidade.")
#    justification: str = Field(..., description="Justificativa da classificação e do pivô.")
#    proposed_adaptation: Optional[str] = Field(None, description="Adaptação proposta (ex: criação de pseudo-pivô), se necessária.")


class FinalTransformationRuleOutput(BaseModel):
   triples_map_name: str = Field(..., description="Nome do TriplesMap.")
   tr_id: str = Field(..., description="Identificador da regra de transformação.")
   final_transformation_rule: str = Field(..., description="A regra de transformação (TR) final gerada formalmente.")
   relational_path_as_last_term: str = Field(..., description="O caminho relacional posicionado como o último termo do corpo da regra.")
   validation_status: str = Field(..., description="Status final de validação do mapeamento.")



