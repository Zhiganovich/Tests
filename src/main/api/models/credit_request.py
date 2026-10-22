from pydantic import BaseModel

class CreditRequest(BaseModel):
    accountId: int
    amount: float
    termMonths: int