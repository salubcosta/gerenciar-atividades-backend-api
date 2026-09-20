import re

import requests

from repositories import PessoaRepository
from schemas import (
    PessoaCreateSchema,
    PessoaResponseSchema,
    PessoaUpdateSchema,
)


repository = PessoaRepository()
VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"


class PessoaService:
    def _buscar_endereco(self, cep: str):
        cep_limpo = re.sub(r"\D", "", cep)
        if len(cep_limpo) != 8:
            return None

        try:
            resposta = requests.get(VIACEP_URL.format(cep=cep_limpo), timeout=5)
            resposta.raise_for_status()
            endereco = resposta.json()
        except (requests.RequestException, ValueError):
            return None

        if endereco.get("erro"):
            return None

        return {
            "cep": endereco.get("cep", cep_limpo),
            "logradouro": endereco.get("logradouro", ""),
            "complemento": endereco.get("complemento") or None,
            "bairro": endereco.get("bairro") or None,
            "cidade": endereco.get("localidade", ""),
            "uf": endereco.get("uf", ""),
        }

    def _montar_dados(self, dados: PessoaCreateSchema | PessoaUpdateSchema):
        endereco = self._buscar_endereco(dados.cep)
        if not endereco:
            return None

        return {
            "nome": dados.nome,
            "sobrenome": dados.sobrenome,
            "email": dados.email,
            "numero": dados.numero,
            **endereco,
            "complemento": dados.complemento or endereco["complemento"],
        }

    def criar(self, form: PessoaCreateSchema):
        dados = self._montar_dados(form)
        if not dados:
            return {"erro": "CEP inválido ou não encontrado"}, 400

        pessoa = repository.criar(dados)
        if not pessoa:
            return {"erro": "E-mail já cadastrado ou dados inválidos"}, 409
        return PessoaResponseSchema.model_validate(pessoa).model_dump(), 201

    def atualizar(self, pessoa_id: int, body: PessoaUpdateSchema):
        dados = self._montar_dados(body)
        if not dados:
            return {"erro": "CEP inválido ou não encontrado"}, 400

        pessoa = repository.atualizar(pessoa_id, dados)
        if not pessoa:
            return {"erro": "Pessoa não encontrada ou e-mail já cadastrado"}, 404
        return PessoaResponseSchema.model_validate(pessoa).model_dump(), 200

    def listar(self):
        pessoas = repository.listar()
        return {
            "pessoas": [PessoaResponseSchema.model_validate(pessoa).model_dump() for pessoa in pessoas],
            "total": len(pessoas),
        }, 200

    def buscar_por_id(self, pessoa_id: int):
        pessoa = repository.buscar_por_id(pessoa_id)
        if not pessoa:
            return {"erro": "Pessoa não encontrada"}, 404
        return PessoaResponseSchema.model_validate(pessoa).model_dump(), 200

    def deletar(self, pessoa_id: int):
        if not repository.deletar(pessoa_id):
            return {"erro": "Pessoa não encontrada"}, 404
        return {"mensagem": "Pessoa deletada com sucesso"}, 200
