from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Projeto(Base):
    __tablename__ = "projeto"

    id          =   Column(Integer, primary_key=True)
    nome        =   Column(String(100), unique=True, nullable=False)
    descricao   =   Column(String(500), nullable=False)
    categoria_id=   Column(Integer, ForeignKey("categoria.id"), nullable=False)

    # Relacionamentos: Infomando para sqlalchemy que a tabela projeto, possui relacionamento com: categoria e registros
    
    # cascade=all, delete-orpahn está documentado em https://docs.sqlalchemy.org/en/21/orm/cascades.html
    # O projeto possui relacionamento com Registro (de atividades), registro depende de projeto, sendo
    # assim, ao deletar projeto, deverá ser informado que os registros daquele projeto também deverão 
    # ser deletado.
    categoria   =   relationship("Categoria", back_populates="projetos")
    registros   =   relationship("Registro", back_populates="projeto", cascade="all, delete-orphan")

    def __init__(self, nome: str, descricao: str, categoria_id: int):
        """
        Responsável por mapear tabela de Projetos

        Arguments:
            id: pk da tabela projeto
            nome: nome do projeto
            descricao: descrição do projeto
            categoria_id: Chave estrangeira da tabela categoria(id)
        
        Relationship:
            categoria: Todo projeto está obrigatoriamente relacionado a alguma categoria
            registros: Todo projeto pode guardar um conjunto de atividades
        """
        self.nome = nome
        self.descricao = descricao
        self.categoria_id = categoria_id
