from sqlalchemy import Column, Integer, Float, String
from src.main.api.db.base import Base



class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, unique=True)
    number = Column(String, nullable=False)
    balance = Column(Float, nullable=False)

    def __repr__(self):
        return f"Account(id={self.id}, user_id={self.user_id}, balance={self.balance})"