from pydantic import BaseModel

class DepositResponse(BaseModel):
    id: int
    balance: float
