from sqlalchemy import Integer, Float, DateTime, Column
from src.main.api.db.base import Base



class Credit(Base):
    __tablename__ = 'credit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, unique=True)
    amount = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    balance = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"id = {self.id}, account = {self.account_id}, amount = {self.amount}, balance = {self.balance}"