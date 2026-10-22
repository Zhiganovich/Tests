import pytest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.db.crud.account_crud import AccountDb as Account


@pytest.mark.api
class TestCreateUser:
    def test_create_deposite(self, api_manager, create, db_session):
        created_user = create()
        create_account_response = api_manager.user_steps.create_account(created_user)

        deposit_request = DepositRequest(accountId=create_account_response.id, amount=1001.1)
        response = api_manager.user_steps.deposit_account(deposit_request,
                                                          created_user,
                                                          ResponseSpec.success_code(),
                                                          validate_response=True
                                                          )
        assert response.balance == deposit_request.amount

        acc_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert acc_from_db.balance == deposit_request.amount

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
    def test_deposite_check_invalid(self, amount, api_manager, create, db_session):
        created_user = create()
        create_account_response = api_manager.user_steps.create_account(created_user)

        deposit_request = DepositRequest(accountId=create_account_response.id, amount=amount)
        api_manager.user_steps.deposit_account(deposit_request,
                                               created_user,
                                               ResponseSpec.bad_code(),
                                               validate_response=False
                                               )

        acc_from_db = Account.account_by_id(db_session, create_account_response.id)
        assert acc_from_db.balance == 0

