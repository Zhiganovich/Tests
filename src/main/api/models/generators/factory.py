import rstr
from polyfactory.factories.pydantic_factory import ModelFactory
from src.main.api.models.create_user_request import CreateUserRequest

class CreateUserFactory(ModelFactory[CreateUserRequest]):
    role = "ROLE_CREDIT_SECRET"

    @classmethod
    def username(cls) -> str:
        return rstr.xeger(r"[A-Za-z]{3}[0-9]{5}")

    @classmethod
    def password(cls) -> str:
        return rstr.xeger(r"[A-Z]{2}[a-z]{1}[@_!]{3}[0-9]{3}")