from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify
from schemas import (
    RegistroCreateSchema,
    RegistroUpdateSchema,
    RegistroResponseSchema,
    RegistroListResponseSchema,
    RegistroProjetoGetId,
    RegistroGetId
)
from services.registro_service import RegistroService

registro_bp = APIBlueprint("registro", __name__, url_prefix="/registros")
registro_tag = Tag(name="Registros", description="Endpoints para trabalhar com registros")
service = RegistroService()

@registro_bp.post("/", tags=[registro_tag], responses={"200": RegistroResponseSchema})
def adicionar_registro(body: RegistroCreateSchema):
    return service.adicionar(form=body)

@registro_bp.put("/<int:id>", tags=[registro_tag], responses={"200": RegistroResponseSchema})
def atualizar_registro(path: RegistroGetId, body: RegistroUpdateSchema):
    return service.atualizar(registro_id=path.id, body=body)

@registro_bp.get("/projeto/<int:projeto_id>", tags=[registro_tag], responses={"200": RegistroListResponseSchema})
def listar_registros(path: RegistroProjetoGetId):
    return service.listar(projeto_id=path.projeto_id)

@registro_bp.get("/<int:id>", tags=[registro_tag], responses={"200": RegistroResponseSchema})
def buscar_registro(path: RegistroGetId):
    return service.buscar_por_id(path.id)
    
@registro_bp.delete("/<int:id>", tags=[registro_tag])
def deletar_registro(path: RegistroGetId):
    return service.deletar(registro_id=path.id)
    