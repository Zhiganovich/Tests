from typing import Callable, Dict
import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.db.crud.account_crud import AccountDb as Account
from src.main.api.models.generators.factory import TransferUserFactory

@pytest.mark.api
class TestTransfer:
    def test_make_transfer(self, api_manager: ApiManager, create_account: Callable, funded_account: Dict, db_session: Session) -> None:
        first_user_data = funded_account["user"]
        first_user = funded_account["account"]
        account_data_second_user = create_account()
        second_user = account_data_second_user["account"]
        initial_balance = funded_account["deposit_response"].balance

        transfer_user_request = TransferUserFactory.build(fromAccountId=first_user.id,
                                                          toAccountId=second_user.id)
        transfer_user_response = api_manager.user_steps.user_transfer(transfer_user_request,
                                                                      first_user_data,
                                                                      ResponseSpec.success_code(),
                                                                      validate_response=True)
        assert transfer_user_response.fromAccountIdBalance == pytest.approx(
            initial_balance - transfer_user_request.amount
        ), "API: Неверный баланс отправителя после перевода"

        account_from_db_first = Account.account_by_id(db_session, first_user.id)
        assert account_from_db_first.balance == pytest.approx(
            initial_balance - transfer_user_request.amount
        ), "DB: Неверный баланс отправителя после перевода"

        account_from_db_second = Account.account_by_id(db_session, second_user.id)
        assert account_from_db_second.balance == pytest.approx(
            transfer_user_request.amount
        ), "DB: Неверный баланс получателя после перевода"



    @pytest.mark.negative
    def test_make_transfer_invalid(self, api_manager: ApiManager, funded_account: Dict, db_session: Session) -> None:
        user_data = funded_account["user"]
        account_data = funded_account["account"]

        transfer_user_request = TransferUserFactory.build(fromAccountId=account_data.id,
                                                          toAccountId=99999)

        api_manager.user_steps.user_transfer(transfer_user_request,
                                                user_data,
                                                ResponseSpec.not_found_code(),
                                                validate_response=False)

        account_from_db_first = Account.account_by_id(db_session, account_data.id)
        assert account_from_db_first.balance == funded_account["deposit_response"].balance, \
            "DB: После отклонённого перевода баланс отправителя не должен измениться"