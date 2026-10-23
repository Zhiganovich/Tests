import random
import rstr
from polyfactory.factories.pydantic_factory import ModelFactory
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_user_request import TransferUserRequest


class CreateUserFactory(ModelFactory[CreateUserRequest]):
    role = "ROLE_CREDIT_SECRET"

    @classmethod
    def username(cls) -> str:
        return rstr.xeger(r"[A-Za-z]{3}[0-9]{5}")

    @classmethod
    def password(cls) -> str:
        return rstr.xeger(r"[A-Z]{2}[a-z]{1}[@_!]{3}[0-9]{3}")

class CreateCreditFactory(ModelFactory[CreditRequest]):
    @classmethod
    def amount(cls) -> float:
        return round(random.uniform(5000, 15000), 2)

    @classmethod
    def termMonths(cls) -> int:
        return random.randint(1, 60)

class DepositAccountFactory(ModelFactory[DepositRequest]):
    @classmethod
    def amount(cls) -> float:
        return round(random.uniform(1000, 9000), 2)

class TransferUserFactory(ModelFactory[TransferUserRequest]):
    @classmethod
    def amount(cls) -> float:
        return round(random.uniform(500, 999), 2)
