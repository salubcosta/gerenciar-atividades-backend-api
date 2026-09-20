from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from database.database import Session
from models import Registro, Projeto

class RegistroRepository:
    """
    Responsável pelo acesso e manipulação dos dados da tabela registro no BD

    Esta classe encapsula as operações de CRUD

    Repository não contém regras de negócio, apenas operações de banco de dados
    """

    def adicionar_registro(self, descricao: str, projeto_id: int, data = None):
        """
        Cria um novo registro no DB

        Arguments:
            descricao: Descrição do registro
            projeto_id: FK de registro apontando para qual projeto está relacionado
            data: Data que o registro foi cadastrado no BD
        
        Returns:
            Objeto de Registo | None: Retorna o objeto de registro já com mapeamento para trazer o projeto e a categoria
            populada, assim facilita a renderização no frontend. Ou None caso ocorra algum erro.
        """
        with Session() as session:
            registro = Registro(descricao=descricao, projeto_id=projeto_id, data=data)
            try:
                session.add(registro)
                session.commit()

                return (
                    session.query(Registro)
                    .options(
                        joinedload(Registro.projeto).joinedload(Projeto.categoria)
                    ).filter(Registro.id == registro.id).first()
                )
            except IntegrityError:
                session.rollback()
                return None
            except Exception: 
                session.rollback()
                return None
            
    def atualizar(self, registro_id: int, descricao: str):
        """
        Atualiza um registro no DB

        Arguments:
            registro_id: PK do registro
            descricao: Descrição do registro
                
        Returns:
            Objeto de Registo | None: Retorna o objeto de registro já com mapeamento 
            para trazer o projeto e a categoria populada, assim facilita a renderização
            no frontend. Ou None caso ocorra algum erro.
        """
        with Session() as session:
            registro = session.query(Registro).options(
                joinedload(Registro.projeto).joinedload(Projeto.categoria)
            ).filter(Registro.id == registro_id).first()

            if not registro:
                return None
            
            # Só é permitido alterar descricao da atividade
            registro.descricao = descricao

            try:
                session.commit()
                session.refresh(registro)
                return registro
            except IntegrityError:
                session.rollback()
                return None
            except Exception:
                return None
            
    def listar_registros(self, projeto_id: int):
        """
        Responsável por listar todos os Registros

        Return:
            list[Registro]: Retorna uma lista contendo todos os registros já com 
            o projeto e categoria renderizado junto ao registro
        """
        with Session() as session:
            return session.query(Registro).options(
                joinedload(Registro.projeto).joinedload(Projeto.categoria)
                ).filter(Registro.projeto_id == projeto_id).all()
    
    def buscar_registro_por_id(self, registro_id: int):
        """
        Responsável por buscar um registro específico

        Arguments:
            registro_id: PK da tabela registro
        Return:
            Obj(Registro): Retorna um objeto de registro já com 
            o projeto e categoria renderizado junto ao registro
        """
        with Session() as session:
            return session.query(Registro).options(
                joinedload(Registro.projeto).joinedload(Projeto.categoria)
            ).filter(Registro.id == registro_id).first()
        
    def deletar_registro(self, registro_id: int):
        """
        Responsável por deletar um registro pelo id

        Arguments:
            registro_id: PK da tabela registro

        Return:
            count: Retona a quantidade de registros afetados. Como estamos deletando por id,
            caso encontre o registro, será retornado 1, caso não encontre, retorna 0.
        """
        with Session() as session:
            count = session.query(Registro).filter(Registro.id == registro_id).delete()
            session.commit()
            return count