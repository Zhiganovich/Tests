from pydantic import BaseModel


class DepositRequest(BaseModel):
    accountId: int
    amount: float

