from dataclasses import dataclass
from typing import Type, Optional
from enum import Enum

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transfer_user_request import TransferUserRequest
from src.main.api.models.transfer_user_response import TransferUserResponse
from src.main.api.models.credit_response import CreditResponse


@dataclass
class EndpointConfig:
    url: str
    request_model: Optional[Type[BaseModel]] = None
    response_model: Optional[Type[BaseModel]] = None

class Endpoint(Enum):
    LOGIN_USER = EndpointConfig(
        url="/api/auth/token/login",
        request_model=LoginUserRequest,
        response_model=LoginUserResponse
    )

    ADMIN_CREATE_USER = EndpointConfig(
        url="/api/admin/create",
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfig(
        url="/api/admin/users",
    )

    USER_CREATE_ACCOUNT = EndpointConfig(
        url="/api/account/create",
        response_model=CreateAccountResponse
    )

    USER_DEPOSIT = EndpointConfig(
        url="/api/account/deposit",
        request_model=DepositRequest,
        response_model=DepositResponse
    )

    USER_TRANSFER = EndpointConfig(
        url="/api/account/transfer",
        request_model=TransferUserRequest,
        response_model=TransferUserResponse
    )

    USER_CREDIT_REQUEST = EndpointConfig(
        url="/api/credit/request",
        request_model=CreditRequest,
        response_model=CreditResponse
    )

    USER_REPAY_CREDIT = EndpointConfig(
        url="/api/credit/repay",
        request_model=CreditRepayRequest,
        response_model=CreditRepayResponse
    )