from repositories import RegistroRepository, ProjetoRepository
from schemas import RegistroCreateSchema, RegistroUpdateSchema, RegistroResponseSchema

repository = RegistroRepository()

class RegistroService:
    """
    Camada responsável pela lógica de negócio relacionada aos registros.

    O service atua como intermediário entre as rotas da API e o repository,
    aplicando validações e regras antes de acessar o banco de dados.
    """

    def adicionar(self, form: RegistroCreateSchema):
        """
        Adiciona um novo registro de atividade
        
        Arguments:
            form: Dados enviados pelo cliente

        Returns:
            JSON: retorna uma mensagem informando:
                1 - mensagem de erro caso não exista projeto para o registro, 404
                2 - mensagem de erro caso ocorra algum conflito, 409
                3 - mensagem de sucesso, status code 200

        """
        repo_projeto = ProjetoRepository()
        projeto = repo_projeto.buscar_por_id(form.projeto_id)
        if not projeto:
            return {"erro": "Projeto não encontrado"}, 404
        
        resultado = repository.adicionar_registro(
            descricao=form.descricao,
            projeto_id=form.projeto_id,
        )
        if not resultado:
            return {"erro": "Erro ao criar registro"}, 409
        return RegistroResponseSchema.model_validate(resultado).model_dump(), 200

    def atualizar(self, registro_id: int, body: RegistroUpdateSchema):
        """
        Atualiza a descrição de um registro
        
        Arguments:
            registro_id: PK da tabela registro 
            body: dados enviados pelo cliente
            
        Returns:
            JSON: retorna mensagem informando:
                1 - Projeto não foi encontrado, 404
                2 - Registro não foi encontrado, 404
                3 - Mensagem de sucesso com registro atualizado, 200
        """        
        resultado = repository.atualizar(
            registro_id=registro_id,
            descricao=body.descricao
        )
        if not resultado:
            return {"erro": "Registro não encontrado"}, 404
        return RegistroResponseSchema.model_validate(resultado).model_dump(), 200

    def listar(self, projeto_id: int):
        """
        Lista todos os registros de um projeto
        
        Arguments:
            projeto_id: PK da tabela projeto

        Returns:
            JSON: Contendo a chave de registros com uma lista de registros e 
            uma chave total contendo a quantidade de registros retornados.

        """
        registros = repository.listar_registros(projeto_id=projeto_id)
        return {
            "registros": [RegistroResponseSchema.model_validate(r).model_dump() for r in registros],
            "total": len(registros)
        }, 200

    def buscar_por_id(self, registro_id: int):
        """
        Busca um registro pelo ID
        
        Arguments:
            registro_id: PK da tabela de registro

        Returns:
            JSON: contendo mensagem de erro caso não encontre o registor, 404, 
            ou um objeto de registro com seus relacionamentos populados, 200.
        """
        resultado = repository.buscar_registro_por_id(registro_id=registro_id)
        if not resultado:
            return {"erro": "Registro não encontrado"}, 404
        return RegistroResponseSchema.model_validate(resultado).model_dump(), 200

    def deletar(self, registro_id: int):
        """
        Deleta um registro pelo ID
        
        Arguments:
            registro_id: PK da tabela registro

        Returns:
            JSON: mensagem informando erro, 404, caso não encontre registro
            ou mensagem de registro deletado com sucesso e status code 200

        """
        count = repository.deletar_registro(registro_id=registro_id)
        if not count:
            return {"erro": "Registro não encontrado"}, 404
        return {"mensagem": "Registro deletado com sucesso"}, 200