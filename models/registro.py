from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Registro(Base):
    __tablename__ = "registro"

    id          = Column(Integer, primary_key=True)
    descricao   = Column(String(500), nullable=False)
    data        = Column(DateTime, default=datetime.now, nullable=False)
    projeto_id  = Column(Integer, ForeignKey("projeto.id"), nullable=False)

    # Relacionamento: Infomando para sqlalchemy que a tabela registro, possui relacionamento com projeto
    projeto     = relationship("Projeto", back_populates="registros")

    def __init__(self, descricao: str, projeto_id: int, data: DateTime = None):
        """
        Responsável por mapear tabela de Registro

        Arguments:
            id: pk da tabela registro
            descricao: breve descrição do registro
            data: Data e hora que o registro foi inserido
            projeto_id: Chave estrangeira da tabela projeto(id)
    
        Relationship:
            projeto: Os registros obrigatoriamente dependem de um projeto
        """
        self.descricao = descricao
        self.projeto_id = projeto_id
        self.data = data or datetime.now()