from pydantic import BaseModel


class User(BaseModel):
    username: str
    role: str

class LoginUserResponse(BaseModel):
    token: str
    user: User