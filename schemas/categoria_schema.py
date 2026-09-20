from pydantic import BaseModel
from typing import List

class CategoriaCreateSchema(BaseModel):
    nome: str 

class CategoriaUpdateSchema(BaseModel):
    nome: str

class CategoriaResponseSchema(BaseModel):
    id: int
    nome: str 

    # Permite que os modelos leiam dados diretamente dos atributos do objeto
    # em vez de apenas consultas em dicionário
    class Config:
        from_attributes = True

class CategoriaGetId(BaseModel):
    id: int

class CategoriaListResponseSchema(BaseModel):
    categorias: List[CategoriaResponseSchema]