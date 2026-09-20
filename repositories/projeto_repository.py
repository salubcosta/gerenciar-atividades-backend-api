from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from database.database import Session
from models import Projeto

class ProjetoRepository:
    """
    Responsável pelo acesso e manipulação dos dados da tabela projeto no BD

    Esta classe encapsula as operações de CRUD

    Repository não contém regras de negócio, apenas operações de banco de dados
    """

    def criar_projeto(self, nome: str, descricao: str, categoria_id: int):
        """
        Cria um novo projeto no DB

        Arguments:
            nome: Nome do projeto
            descricao: Descrição do projeto
            categoria_id; ID da categoria relacionada com o projeto
        
        Returns:
            Projeto | None: Retorna o objeto projeto já com mapeamento para trazer a categoria
            populada ou None caso ocorra algum erro.
        """
        with Session() as session:
            projeto = Projeto(nome=nome, descricao=descricao, categoria_id=categoria_id)
            try:
                session.add(projeto)
                session.commit()

                return (
                    session.query(Projeto)
                    .options(joinedload(Projeto.categoria))
                    .filter(Projeto.id == projeto.id)
                    .first()
                )
            except IntegrityError:
                session.rollback()
                return None
            except Exception: 
                session.rollback()
                return None
    
    def atualizar(self, projeto_id: int, nome: str, descricao: str, categoria_id: int):
        """
        Atualiza um projeto no BD

        Arguments:
            projeto_id: PK do projeto
            nome: Novo nome do projeto
            descricao: Nova descrição do projeto
            categoria_id: FK de categoria 

        Returns:
            Projeto | None: Retorna o objeto projeto já com mapeamento para trazer a categoria
            populada ou None caso ocorra algum erro.
        """
        with Session() as session:
            projeto = session.query(Projeto).filter(Projeto.id == projeto_id).first()

            if not projeto:
                return None
            
            projeto.nome = nome
            projeto.descricao = descricao
            projeto.categoria_id = categoria_id
            try:
                session.commit()
                return (
                session.query(Projeto)
                    .options(joinedload(Projeto.categoria))
                    .filter(Projeto.id == projeto.id)
                    .first()
                )
            except IntegrityError:
                session.rollback()
                return None
            except Exception:
                session.rollback()
                return None

    def listar_projetos(self):
        """
        Responsável por listar todos os Projetos

        Return:
            list[Projeto]: Returna uma lista contendo todos os projetos
        """
        with Session() as session:
            return session.query(Projeto).options(joinedload(Projeto.categoria)).all()
        
    def buscar_por_id(self, projeto_id: int):
        """
        Responsável por buscar projeto por id

        Arguments:
            projeto_id: PK do projeto

        Return:
            Projeto: Retorna o primeiro match de projeto e popula objeto categoria para facilitar a leitura
        """
        with Session() as session:
            return session.query(Projeto).options(joinedload(Projeto.categoria)).filter(Projeto.id == projeto_id).first()
    
    def deletar_projeto(self, projeto_id: int):
        """
        Responsável por deletar um projeto pelo id

        Arguments:
            projeto_id: PK do projeto

        Return:
            count: Retona a quantidade de registros afetados. Como estamos deletando por id,
            caso encontre registro. Retorna 1, caso não encontre, retorna 0.
        """
        with Session() as session:
            projeto = session.query(Projeto).filter(Projeto.id == projeto_id).first()

            if not projeto:
                return 0
            
            session.delete(projeto)
            session.commit()
            return 1
            