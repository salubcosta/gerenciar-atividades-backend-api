from repositories import ProjetoRepository, CategoriaRepository
from schemas import ProjetoCreateSchema, ProjetoUpdateSchema, ProjetoResponseSchema

repository = ProjetoRepository()

class ProjetoService:
    """
    Camada responsável pela lógica de negócio relacionada aos Projetos.

    O service atua como intermediário entre as rotas da API e o repository,
    aplicando validações e regras antes de acessar o banco de dados.
    """

    def criar(self, form: ProjetoCreateSchema):
        """
        Cria um novo projeto

        Arguments:
            form (ProjetoCreateSchema): Dados enviados pelo cliente

        Returns:
            Json: Retorna mensagem de erro caso não encontre a categoria ou
            retorna o objeto projeto já populado com um objeto de categoria
        """
        repo_categoria = CategoriaRepository()
        categoria = repo_categoria.buscar_por_id(form.categoria_id)
        if not categoria:
            return {"erro": "Categoria não encontrada"}, 404
        
        resultado = repository.criar_projeto(
            nome=form.nome,
            descricao=form.descricao,
            categoria_id=form.categoria_id
        )
        if not resultado:
            return {"erro": "Projeto já existe ou dados inválidos"}, 400
        return ProjetoResponseSchema.model_validate(resultado).model_dump(), 200
    
    def atualizar(self, id: int, body: ProjetoUpdateSchema):
        """
        Atualiza um projeto pelo ID
        
        Arguments:
            id: PK de projeto
            body (ProjetoUpdateSchema): Dados enviados pelo cliente

        Returns:
            Json: Retorna mensagem de erro caso não encontre a categoria ou
            retorna o objeto projeto já populado com um objeto de categoria
        """
        repo_categoria = CategoriaRepository()
        categoria = repo_categoria.buscar_por_id(categoria_id=body.categoria_id)

        if not categoria:
            return {"erro": "Categoria não encontrada"}, 404

        resultado = repository.atualizar(
            projeto_id=id,
            nome=body.nome,
            descricao=body.descricao,
            categoria_id=body.categoria_id
        )
        if not resultado:
            return {"erro": "Projeto não encontrado"}, 404
        return ProjetoResponseSchema.model_validate(resultado).model_dump(), 200
    
    def listar(self):
        """
        Lista todos os projetos

        Returns:
            Json: Retorna objeto projeto já populado com um objeto de categoria
        """
        projetos = repository.listar_projetos()
        return {
            "projetos": [ProjetoResponseSchema.model_validate(p).model_dump() for p in projetos],
            "total": len(projetos)
            }, 200
        
    def buscar_por_id(self, projeto_id: int):
        """
        Busca um projeto pelo ID
        
        Arguments:
            projeto_id: PK de projeto

        Returns:
            Json: Retorna mensagem de erro caso não encontre o projeto ou
            retorna o objeto projeto já populado com um objeto de categoria
        """
        resultado = repository.buscar_por_id(projeto_id=projeto_id)
        if not resultado:
            return {"erro": "Projeto não encontrado"}, 404
        return ProjetoResponseSchema.model_validate(resultado).model_dump(), 200

    def deletar(self, projeto_id: int):
        """
        Deleta um projeto pelo ID
        
        Arguments:
            projeto_id: PK de projeto

        Returns:
            Json: Retorna mensagem de erro caso não encontre o projeto ou
            retorna uma mensagem de sucesso para o projeto excluído
        """
        count = repository.deletar_projeto(projeto_id=projeto_id)
        if not count:
            return {"erro": "Projeto não encontrado"}, 404
        return {"mensagem": "Projeto deletado com sucesso"}, 200