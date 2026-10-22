from pydantic import BaseModel

class CreditRepayRequest(BaseModel):
    creditId: int # Айдишник кредита из запроса на создание кредита
    accountId: int
    amount: float
