import pytest
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.credit_request import CreditRequest
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.db.crud.credit_crud import CreditCrud as Credit
from src.main.api.db.crud.account_crud import AccountDb as Account

@pytest.mark.api
class TestUserMakeCredit:
    def test_create_credit_user(self, api_manager, create, db_session):
        created_user = create()
        create_account_response = api_manager.user_steps.create_account(created_user)

        credit_request = CreditRequest(accountId=create_account_response.id, amount=5000, termMonths=12)
        credit_response = api_manager.user_steps.credit_request(credit_request,
                                                                created_user,
                                                                ResponseSpec.created_code(),
                                                                validate_response=True)
        assert credit_request.amount == credit_response.amount
        assert credit_request.amount == credit_response.balance

        account_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert account_from_db.balance == credit_request.amount

        credit_from_db = Credit.credit_by_id(db_session, credit_response.id)
        assert credit_from_db.amount == credit_response.amount
        assert credit_from_db.term_months == credit_request.termMonths

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
    def test_create_credit_invalid(self, amount, api_manager, create, db_session):
        created_user = create()
        create_account_response = api_manager.user_steps.create_account(created_user)

        credit_request = CreditRequest(accountId=create_account_response.id, amount=amount, termMonths=12)
        api_manager.user_steps.credit_request(credit_request,
                                              created_user,
                                              ResponseSpec.bad_code(),
                                              validate_response=False
                                              )

        account_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert account_from_db.balance == 0