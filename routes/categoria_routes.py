from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify
from schemas import (
    CategoriaCreateSchema, 
    CategoriaUpdateSchema, 
    CategoriaResponseSchema, 
    CategoriaListResponseSchema,
    CategoriaGetId
)

from services import CategoriaService

categoria_bp = APIBlueprint("categoria", __name__, url_prefix="/categorias")
categoria_tag = Tag(name="Categorias", description="Endpoints para trabalhar com categorias")
service = CategoriaService()

@categoria_bp.post("/", tags=[categoria_tag], responses={"200": CategoriaResponseSchema})
def criar_categoria(body: CategoriaCreateSchema):
    return service.criar(form=body)

@categoria_bp.put("/<int:id>", tags=[categoria_tag], responses={"200": CategoriaResponseSchema})
def atualizar_categoria(path: CategoriaGetId, body: CategoriaUpdateSchema):
    return service.atualizar(id=path.id, body=body)

@categoria_bp.get("/", tags=[categoria_tag], responses={"200": CategoriaListResponseSchema})
def listar_categorias():
    return service.listar()

@categoria_bp.get("/<int:id>", tags=[categoria_tag], responses={"200": CategoriaResponseSchema})
def buscar_categoria(path: CategoriaGetId):
    return service.buscar_por_id(path.id)

@categoria_bp.delete("/<int:id>", tags=[categoria_tag])
def deletar_categoria(path: CategoriaGetId):
    return service.deletar(path.id)
    