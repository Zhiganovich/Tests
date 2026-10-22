from pydantic import BaseModel

class CreateAccountResponse(BaseModel):
    id: int
    number: str
    balance: float 