import pytest
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.db.crud.credit_crud import CreditCrud as Credit
from src.main.api.db.crud.account_crud import AccountDb as Account

@pytest.mark.api
class TestUserRepay:
    def test_user_repay(self, api_manager, create, db_session):
        created_user = create()
        create_account_response = api_manager.user_steps.create_account(created_user)

        credit_request = CreditRequest(accountId=create_account_response.id, amount=5000, termMonths=12)
        credit_response = api_manager.user_steps.credit_request(credit_request,
                                                                created_user,
                                                                ResponseSpec.created_code(),
                                                                validate_response=True)

        repay_credit_request = CreditRepayRequest(creditId=credit_response.creditId,
                                                  accountId=create_account_response.id,
                                                  amount=5000
                                                  )
        repay_credit_response = api_manager.user_steps.credit_repay(repay_credit_request,
                                                                    created_user,
                                                                    ResponseSpec.success_code(),
                                                                    validate_response=True
                                                                    )

        assert repay_credit_response.creditId == repay_credit_request.creditId
        assert repay_credit_response.amountDeposited == repay_credit_request.amount

        credit_from_db = Credit.credit_by_id(db_session, credit_response.id)
        assert credit_from_db.balance == 0

        account_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert account_from_db.balance == 0


    @pytest.mark.parametrize(
        "amount",
        [
            (1234),
            (4999),
            (15001),
            (16532),
        ]
    )
    @pytest.mark.negative
    def test_user_repay_invalid(self, amount, api_manager, create, db_session):
        created_user = create()
        create_account_response = api_manager.user_steps.create_account(created_user)

        credit_request = CreditRequest(accountId=create_account_response.id, amount=5000, termMonths=12)
        credit_response = api_manager.user_steps.credit_request(credit_request,
                                                                created_user,
                                                                ResponseSpec.created_code(),
                                                                validate_response=True)
        assert credit_request.amount == credit_response.amount
        assert credit_request.amount == credit_response.balance

        repay_credit_request = CreditRepayRequest(creditId=credit_response.creditId,
                                                  accountId=create_account_response.id,
                                                  amount=amount
                                                  )
        api_manager.user_steps.credit_repay(repay_credit_request,
                                            created_user,
                                            ResponseSpec.unprocessable_code(),
                                            validate_response=False
                                            )

        credit_from_db = Credit.credit_by_id(db_session, credit_response.id)
        assert credit_from_db.amount == credit_response.amount

        account_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert account_from_db.balance == credit_request.amount