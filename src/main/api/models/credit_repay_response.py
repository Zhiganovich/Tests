from pydantic import BaseModel

class CreditRepayResponse(BaseModel):
    creditId: int
    amountDeposited: float