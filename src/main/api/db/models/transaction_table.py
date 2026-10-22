from sqlalchemy import Column, Integer, Float, String, DateTime
from src.main.api.db.base import Base


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, unique=True)
    to_account_id = Column(Integer, nullable=False)
    from_account_id = Column(Integer, nullable=False)
    credit_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return (f"id = {self.id}, "
                f"transaction_type = {self.transaction_type}, "
                f"amount = {self.amount}, "
                f"from_account_id = {self.from_account_id}, "
                f"to_account_id = {self.to_account_id}")