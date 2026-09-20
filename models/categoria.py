from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

class Categoria(Base):
    __tablename__ = "categoria"

    id      =   Column(Integer, primary_key=True)
    nome    =   Column(String(100), unique=True, nullable=False)

    # Relacionamento: Infomando para sqlalchemy que a tabela categoria, possui relacionamento com projetos
    
    # back_populates - cria uma referência bidirecional. Então a partir da categoria, 
    # eu consigo buscar um projeto. Exemplo: categoria.projetos e projeto.categoria.nome
    projetos=   relationship("Projeto", back_populates="categoria")

    def __init__(self, nome: str):
        """
        Responsável pela tabela de Categoria

        Arguments:
            id: pk da tabela categoria
            nome: nome da categoria
        
        Relationship:
            projetos: Todo projeto está relacionado com alguma categoria, Exemplo: Leitura, Curso, Certificação e etc.
        """
        self.nome = nome