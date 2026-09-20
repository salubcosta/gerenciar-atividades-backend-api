from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify
from schemas import (
    ProjetoCreateSchema,
    ProjetoUpdateSchema,
    ProjetoResponseSchema,
    ProjetoListResponseSchema,
    ProjetoGetId
)
from services import ProjetoService

projeto_bp = APIBlueprint("projeto", __name__, url_prefix="/projetos")
projeto_tag = Tag(name="Projetos", description="Endpoints para trabalhar com projetos")
service = ProjetoService()

@projeto_bp.post("/", tags=[projeto_tag], responses={"200": ProjetoResponseSchema})
def criar_projeto(body: ProjetoCreateSchema):
    return service.criar(body)
    
@projeto_bp.put("/<int:id>", tags=[projeto_tag], responses={"200": ProjetoResponseSchema})
def atualizar_projeto(path: ProjetoGetId, body: ProjetoUpdateSchema):
    return service.atualizar(id=path.id, body=body)
    
@projeto_bp.get("/", tags=[projeto_tag], responses={"200": ProjetoListResponseSchema})
def listar_projetos():
    return service.listar()

@projeto_bp.get("/<int:id>", tags=[projeto_tag], responses={"200": ProjetoResponseSchema})
def buscar_projeto(path: ProjetoGetId):
    return service.buscar_por_id(projeto_id=path.id)
    
@projeto_bp.delete("/<int:id>", tags=[projeto_tag])
def deletar_projeto(path: ProjetoGetId):
    return service.deletar(path.id)
    