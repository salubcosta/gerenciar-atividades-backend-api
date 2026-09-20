from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from schemas import ProjetoResponseSchema

class RegistroCreateSchema(BaseModel):
    descricao: str
    projeto_id: int

class RegistroUpdateSchema(BaseModel):
    descricao: str

class RegistroResponseSchema(BaseModel):
    id: int
    descricao: str
    projeto_id: int
    projeto: ProjetoResponseSchema
    data: datetime

    class Config:
        from_attributes = True

class RegistroListResponseSchema(BaseModel):
    registros: List[RegistroResponseSchema]

class RegistroProjetoGetId(BaseModel):
    projeto_id: int

class RegistroGetId(BaseModel):
    id: int