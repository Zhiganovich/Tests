import pytest
from src.main.api.models.transfer_user_request import TransferUserRequest
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountDb as Account

@pytest.mark.api
class TestTransfer:
    def test_make_transfer(self, api_manager, create, db_session):
        created_first_user = create()
        create_account_first_response = api_manager.user_steps.create_account(created_first_user)

        created_second_user = create()
        create_account_second_response = api_manager.user_steps.create_account(created_second_user)

        deposit_request = DepositRequest(accountId=create_account_first_response.id, amount=1001.1)
        api_manager.user_steps.deposit_account(deposit_request,
                                               created_first_user,
                                               ResponseSpec.success_code(),
                                               validate_response=True
                                               )

        transfer_user_request = TransferUserRequest(fromAccountId=create_account_first_response.id,
                                                    toAccountId=create_account_second_response.id,
                                                    amount=500.75
                                                    )
        transfer_user_response = api_manager.user_steps.user_transfer(transfer_user_request,
                                                                      created_first_user,
                                                                      ResponseSpec.success_code(),
                                                                      validate_response=True)
        assert transfer_user_response.fromAccountIdBalance == 500.35

        account_from_db_first = Account.account_by_id(db_session, create_account_first_response.id)
        assert account_from_db_first.balance == 500.35

        account_from_db_second = Account.account_by_id(db_session, create_account_second_response.id)
        assert account_from_db_second.balance == 500.75



    @pytest.mark.negative
    def test_make_transfer_invalid(self, api_manager, create, db_session):
        created_user = create()
        create_account_first_response = api_manager.user_steps.create_account(created_user)

        deposit_request = DepositRequest(accountId=create_account_first_response.id, amount=1001.1)
        api_manager.user_steps.deposit_account(deposit_request,
                                               created_user,
                                               ResponseSpec.success_code(),
                                               validate_response=True
                                               )

        transfer_user_request = TransferUserRequest(fromAccountId=create_account_first_response.id,
                                                    toAccountId=9999999,
                                                    amount=500.75
                                                    )
        api_manager.user_steps.user_transfer(transfer_user_request,
                                                created_user,
                                                ResponseSpec.not_found_code(),
                                                validate_response=False)

        account_from_db_first = Account.account_by_id(db_session, create_account_first_response.id)
        assert account_from_db_first.balance == deposit_request.amount