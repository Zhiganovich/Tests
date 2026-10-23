import pytest
from sqlalchemy.orm import Session
from typing import Callable
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.db.crud.account_crud import AccountDb as Account
from src.main.api.models.generators.factory import DepositAccountFactory

@pytest.mark.api
class TestCreateUser:
    def test_create_deposite(self, api_manager: ApiManager, create_account: Callable, db_session: Session) -> None:
        account_data = create_account()
        user_data = account_data["user"]
        create_account_response = account_data["account"]

        deposit_request = DepositAccountFactory.build(accountId=create_account_response.id)
        response = api_manager.user_steps.deposit_account(deposit_request,
                                                          user_data,
                                                          ResponseSpec.success_code(),
                                                          validate_response=True
                                                          )
        assert response.balance == deposit_request.amount, \
            "API: Баланс не соответствует внесенной сумме"

        acc_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert acc_from_db.balance == deposit_request.amount, \
            "DB: Баланс не соответсвует внесенной сумме"

    @pytest.mark.parametrize(
        "amount",
        [
            (999.9),
            (123),
            (9000.1),
            (12342)
        ]
    )
    @pytest.mark.negative
    def test_deposite_check_invalid(self, amount: int | float, api_manager: ApiManager, create_account: Callable, db_session: Session) -> None:
        account_data = create_account()
        user_data = account_data["user"]
        create_account_response = account_data["account"]

        deposit_request = DepositRequest(accountId=create_account_response.id, amount=amount)
        api_manager.user_steps.deposit_account(deposit_request,
                                               user_data,
                                               ResponseSpec.bad_code(),
                                               validate_response=False
                                               )

        acc_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert acc_from_db.balance == 0, \
            "DB: после отклонённого пополнения баланс должен остаться равен 0"