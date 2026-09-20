from flask_openapi3 import APIBlueprint, Tag

from schemas import (
    PessoaCreateSchema,
    PessoaGetId,
    PessoaListResponseSchema,
    PessoaResponseSchema,
    PessoaUpdateSchema,
)
from services import PessoaService


pessoa_bp = APIBlueprint("pessoa", __name__, url_prefix="/pessoas")
pessoa_tag = Tag(name="Pessoas", description="Endpoints para gerenciar meus dados")
service = PessoaService()


@pessoa_bp.post("/", tags=[pessoa_tag], responses={"201": PessoaResponseSchema})
def criar_pessoa(body: PessoaCreateSchema):
    return service.criar(body)


@pessoa_bp.put("/<int:id>", tags=[pessoa_tag], responses={"200": PessoaResponseSchema})
def atualizar_pessoa(path: PessoaGetId, body: PessoaUpdateSchema):
    return service.atualizar(path.id, body)


@pessoa_bp.get("/", tags=[pessoa_tag], responses={"200": PessoaListResponseSchema})
def listar_pessoas():
    return service.listar()


@pessoa_bp.get("/<int:id>", tags=[pessoa_tag], responses={"200": PessoaResponseSchema})
def buscar_pessoa(path: PessoaGetId):
    return service.buscar_por_id(path.id)


@pessoa_bp.delete("/<int:id>", tags=[pessoa_tag])
def deletar_pessoa(path: PessoaGetId):
    return service.deletar(path.id)
