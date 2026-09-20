from sqlalchemy.exc import IntegrityError

from database.database import Session
from models import Pessoa


class PessoaRepository:
    def criar(self, dados: dict):
        with Session() as session:
            pessoa = Pessoa(**dados)
            try:
                session.add(pessoa)
                session.commit()
                session.refresh(pessoa)
                return pessoa
            except IntegrityError:
                session.rollback()
                return None
            except Exception:
                session.rollback()
                return None

    def atualizar(self, pessoa_id: int, dados: dict):
        with Session() as session:
            pessoa = session.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
            if not pessoa:
                return None

            for campo, valor in dados.items():
                setattr(pessoa, campo, valor)

            try:
                session.commit()
                session.refresh(pessoa)
                return pessoa
            except IntegrityError:
                session.rollback()
                return None
            except Exception:
                session.rollback()
                return None

    def listar(self):
        with Session() as session:
            return session.query(Pessoa).all()

    def buscar_por_id(self, pessoa_id: int):
        with Session() as session:
            return session.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

    def deletar(self, pessoa_id: int):
        with Session() as session:
            pessoa = session.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
            if not pessoa:
                return False
            session.delete(pessoa)
            session.commit()
            return True
