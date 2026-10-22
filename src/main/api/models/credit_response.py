from pydantic import BaseModel

class CreditResponse(BaseModel):
    id: int
    amount: float
    termMonths: int
    balance: float
    creditId: int