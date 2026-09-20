from repositories import CategoriaRepository
from schemas import CategoriaCreateSchema, CategoriaUpdateSchema, CategoriaResponseSchema, CategoriaGetId

repository = CategoriaRepository()

class CategoriaService:
    """
    Camada responsável pela lógica de negócio relacionada às categoria.

    O service atua como intermediário entre as rotas da API e o repository,
    aplicando validações e regras antes de acessar o banco de dados.
    """
     
    def criar(self, form: CategoriaCreateSchema):
        """
        Cria uma nova categoria
        
        Arguments:
            form: dados enviados pelo cliente

        Returns:
            JSON: Contendo mensagem de erro, com status code 409 (conflito)
            ou recurso criado com status code 200
        """
        resultado = repository.criar_categoria(nome=form.nome)
        if not resultado:
            # https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Reference/Status#respostas_de_erro_do_cliente 
            # 409 = conflito
            return {"erro": "Categoria já existe ou dados inválidos"}, 409 
        return CategoriaResponseSchema.model_validate(resultado).model_dump(), 200
    
    def atualizar(self, id: int, body: CategoriaUpdateSchema):
        """
        Atualiza uma categoria pelo ID
        
        Arguments:
            id: PK da tabela categoria
            body: dados enviados pelo cliente

        Returns:
            JSON: Contendo mensagem de erro caso não econtre a categoria 
            e objeto de categoria respeitando o CategoriaResponseSchema
        """
        resultado = repository.atualizar(categoria_id=id, nome=body.nome)
        if not resultado:
            return {"erro": "Categoria não encontrada"}, 404
        return CategoriaResponseSchema.model_validate(resultado).model_dump(), 200
    
    def listar(self):
        """
        Lista todas as categorias
        
        Returns:
            JSON: Contendo a chave de categoria com uma lista de categorias e 
            uma chave total contendo a quantidade de categorias retornada.
        """
        categorias = repository.listar_categorias()
        return {
            "categorias": [CategoriaResponseSchema.model_validate(c).model_dump() for c in categorias],
            "total": len(categorias)
        }, 200
    
    def buscar_por_id(self, categoria_id: int):
        """
        Busca uma categoria pelo ID
        
        Arguments:
            categoria_id: PK da tabela categoria
        
        Returns:
            JSON: Contendo mensagem de erro caso não encontra da categoria
            ou o objeto de categoria respeitando o CategoriaResponseSchema
        """
        resultado = repository.buscar_por_id(categoria_id=categoria_id)
        if not resultado:
            return {"erro": "Categoria não encontrada"}, 404
        return CategoriaResponseSchema.model_validate(resultado).model_dump(), 200
    
    def deletar(self, categoria_id: int):
        """
        Deleta uma categoria pelo ID
        
        Arguments:
            categoria_id: PK da tabela de categoria
        
        Returns:
            JSON: Retorna mensagem de erro caso:
                1 - a categoria não exista, status code 404
                2 - há projetos dependentes, status code, 409
                3 - mensagem de sucesso, status code, 200.
        """
        count = repository.deletar_categoria(categoria_id=categoria_id)
        if count == 0:
            return {"erro": "Categoria não encontrada"}, 404
        elif count == 99:
            return {"erro": "Essa categoria possui projetos filhos"}, 409
        return {"mensagem": "Categoria deletada com sucesso"}, 200