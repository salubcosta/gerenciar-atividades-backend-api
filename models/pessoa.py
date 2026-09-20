from sqlalchemy import Column, Integer, String
from database.database import Base


class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    cep = Column(String(9), nullable=False)
    numero = Column(String(20), nullable=True)
    logradouro = Column(String(200), nullable=False)
    complemento = Column(String(200), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)

    def __init__(
        self,
        nome: str,
        sobrenome: str,
        email: str,
        cep: str,
        numero: str | None,
        logradouro: str,
        complemento: str,
        bairro: str,
        cidade: str,
        uf: str,
    ):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.cep = cep
        self.numero = numero
        self.logradouro = logradouro
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
