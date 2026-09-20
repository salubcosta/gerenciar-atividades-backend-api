from pydantic import BaseModel
from typing import List

from schemas import CategoriaResponseSchema

class ProjetoCreateSchema(BaseModel):
    nome: str
    descricao: str
    categoria_id: int

class ProjetoUpdateSchema(BaseModel):
    nome: str
    descricao: str
    categoria_id: int

class ProjetoResponseSchema(BaseModel):
    id: int
    nome: str
    descricao: str
    categoria: CategoriaResponseSchema

    class Config:
        from_attributes = True

class ProjetoListResponseSchema(BaseModel):
    projetos: List[ProjetoResponseSchema]

class ProjetoGetId(BaseModel):
    id: int