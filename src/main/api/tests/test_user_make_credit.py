import pytest
from typing import Callable
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.credit_request import CreditRequest
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.db.crud.credit_crud import CreditCrud as Credit
from src.main.api.db.crud.account_crud import AccountDb as Account
from src.main.api.models.generators.factory import CreateCreditFactory

@pytest.mark.api
class TestUserMakeCredit:
    def test_create_credit_user(self, api_manager: ApiManager, create_account: Callable, db_session: Session) -> None:
        account_data = create_account()
        user_data = account_data["user"]
        create_account_response = account_data["account"]

        credit_request = CreateCreditFactory.build(accountId=create_account_response.id)
        credit_response = api_manager.user_steps.credit_request(credit_request,
                                                                user_data,
                                                                ResponseSpec.created_code(),
                                                                validate_response=True)
        assert credit_request.amount == credit_response.amount, \
            "API: Сумма выданного кредита не соответствует запрошенной"
        assert credit_request.amount == credit_response.balance, \
            "API: Баланс не равен запрашиваемой сумме кредита"

        account_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert account_from_db.balance == credit_request.amount, \
            "DB: Баланс не равен запрашиваемой сумме кредита"

        credit_from_db = Credit.credit_by_id(db_session, credit_response.id)
        assert credit_from_db.amount == credit_response.amount, \
            "DB: Сумма кредита не совпадает с ответом API"
        assert credit_from_db.term_months == credit_request.termMonths, \
            "DB: Количество месяцев для выплаты кредита отличается от переданного"

    @pytest.mark.parametrize(
        "amount",
        [
            (1234),
            (4999.99),
            (15000.01),
            (123123)
        ]
    )
    @pytest.mark.negative
    def test_create_credit_invalid(self, amount: int | float, api_manager: ApiManager, create_account: Callable, db_session: Session) -> None:
        account_data = create_account()
        user_data = account_data["user"]
        create_account_response = account_data["account"]

        credit_request = CreditRequest(accountId=create_account_response.id, amount=amount, termMonths=12)
        api_manager.user_steps.credit_request(credit_request,
                                              user_data,
                                              ResponseSpec.bad_code(),
                                              validate_response=False
                                              )

        account_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert account_from_db.balance == 0, \
            "DB: После отклоненного кредита, баланс должен равняться 0"