from typing import List

from pydantic import BaseModel, field_validator


class PessoaCreateSchema(BaseModel):
    nome: str
    sobrenome: str
    email: str
    cep: str
    numero: str | None = None
    complemento: str | None = None

    @field_validator("cep", "numero", mode="before")
    @classmethod
    def converter_para_texto(cls, valor):
        if isinstance(valor, (int, float)):
            return str(valor)
        return valor


class PessoaUpdateSchema(PessoaCreateSchema):
    pass


class PessoaResponseSchema(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: str
    cep: str
    numero: str | None = None
    logradouro: str
    complemento: str | None = None
    bairro: str | None = None
    cidade: str
    uf: str

    class Config:
        from_attributes = True


class PessoaListResponseSchema(BaseModel):
    pessoas: List[PessoaResponseSchema]
    total: int


class PessoaGetId(BaseModel):
    id: int
