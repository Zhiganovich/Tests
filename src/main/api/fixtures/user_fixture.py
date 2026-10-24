import pytest
from typing import Callable, Dict
from src.main.api.classes.api_manager import ApiManager
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.models.generators.factory import CreateCreditFactory, DepositAccountFactory


@pytest.fixture
def create_account(api_manager: ApiManager, create: Callable) -> Callable:
    def create_acc():
        create_user = create()
        created_account = api_manager.user_steps.create_account(create_user)
        return {
            "user": create_user,
            "account": created_account
        }
    return create_acc

@pytest.fixture
def create_credit(api_manager: ApiManager, create_account: Callable) -> Dict:
    account_data = create_account()
    user_data = account_data["user"]
    create_account_response = account_data["account"]
    create_credit_request = CreateCreditFactory.build(accountId=create_account_response.id)
    created_credit_response = api_manager.user_steps.credit_request(
                                                        credit_request=create_credit_request,
                                                        created_user=user_data,
                                                        response_spec=ResponseSpec.created_code(),
                                                        validate_response=True
                                                        )
    return {
        "user": user_data,
        "account": create_account_response,
        "credit_response": created_credit_response,
        "credit_request": create_credit_request
    }

@pytest.fixture
def funded_account(api_manager: ApiManager, create_account: Callable) -> Dict:
    account_data = create_account()
    user_data = account_data["user"]
    create_account_response = account_data["account"]
    deposit_account_request = DepositAccountFactory.build(accountId=create_account_response.id)
    deposit_account_response = api_manager.user_steps.deposit_account(
                                                        deposit_request=deposit_account_request,
                                                        created_user=user_data,
                                                        response_spec=ResponseSpec.success_code(),
                                                        validate_response=True
                                                        )
    return {
        "user": user_data,
        "account": create_account_response,
        "deposit_response": deposit_account_response,
        "deposit_request": deposit_account_request
    }