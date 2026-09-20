from sqlalchemy.exc import IntegrityError
from database.database import Session
from models import Categoria, Projeto

class CategoriaRepository:
    """
    Responsável pelo acesso e manipulação dos dados da tabela categoria no BD

    Esta classe encapsula as operações de CRUD

    Repository não contém regras de negócio, apenas operações de banco de dados
    """

    def criar_categoria(self, nome: str) -> Categoria:
        """
        Cria uma nova categoria no DB

        Arguments:
            nome: Nome da categoria
        
        Returns:
            Cateogoria | None: Retorna o objeto categoria ou None caso ocorra algum erro.
        """
        with Session() as session:
            categoria = Categoria(nome=nome)
            try:
                session.add(categoria)
                session.commit()

                # Evitar erro de detachedInstanceError
                session.refresh(categoria)
                return categoria
            except IntegrityError:
                session.rollback()
                return None
            except Exception:
                return None
        
    def atualizar(self, categoria_id: int,  nome: str):
        """
        Atualiza uma categoria no BD

        Arguments:
            categoria_id: PK da categoria
            nome: Novo nome da categoria
            
        Returns:
            Cateogoria | None: Retorna o objeto categoria ou None caso ocorra algum erro.
        """
        with Session() as session:
            categoria = session.query(Categoria).filter(Categoria.id == categoria_id).first()

            if not categoria:
                return None
            
            categoria.nome = nome

            try:
                session.commit()
                session.refresh(categoria)
                return categoria
            except IntegrityError:
                session.rollback()
                return None
            except Exception:
                return None

    def listar_categorias(self):
        """
        Responsável por listar todas as categorias

        Return:
            list[Categoria]: Return uma lista contendo todas as categorias
        """
        with Session() as session:
            return session.query(Categoria).all()
    
    def buscar_por_id(self, categoria_id: int):
        """
        Responsável por buscar categoria por id

        Arguments:
            categoria_id: PK de categoria

        Return:
            Categoria: Retorna a primeira ocorrência de categoria por id
        """
        with Session() as session:
            return session.query(Categoria).filter(Categoria.id == categoria_id).first()
        
    def deletar_categoria(self, categoria_id: int):
        """
        Responsável por deletar uma categoria pelo id

        Arguments:
            categoria_id: PK de categoria

        Return:
            count: retornar 99, caso exista algum projeto dependente da categoria. Senão,
            retorna 0, caso a categoria não exista ou 1, caso exista.
        """
        with Session() as session:
            projeto = session.query(Projeto).filter(Projeto.categoria_id == categoria_id).first()
            if projeto:
                return 99
            
            categoria = session.query(Categoria).filter(Categoria.id == categoria_id).first()

            if not categoria:
                return 0
            session.delete(categoria)
            session.commit()
            return 1