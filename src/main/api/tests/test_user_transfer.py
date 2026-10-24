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
        account_data_second_user = create_account()

        transfer_user_request = TransferUserFactory.build(fromAccountId=funded_account["account"].id,
                                                          toAccountId=account_data_second_user["account"].id)
        transfer_user_response = api_manager.user_steps.user_transfer(transfer_user_request,
                                                                      funded_account["user"],
                                                                      ResponseSpec.success_code(),
                                                                      validate_response=True)
        assert transfer_user_response.fromAccountIdBalance == pytest.approx(
            funded_account["deposit_response"].balance - transfer_user_request.amount
        ), "API: Неверный баланс отправителя после перевода"

        account_from_db_first = Account.account_by_id(db_session, funded_account["account"].id)
        assert account_from_db_first.balance == pytest.approx(
            funded_account["deposit_response"].balance - transfer_user_request.amount
        ), "DB: Неверный баланс отправителя после перевода"

        account_from_db_second = Account.account_by_id(db_session, account_data_second_user["account"].id)
        assert account_from_db_second.balance == pytest.approx(
            transfer_user_request.amount
        ), "DB: Неверный баланс получателя после перевода"


    @pytest.mark.negative
    def test_make_transfer_invalid(self, api_manager: ApiManager, funded_account: Dict, db_session: Session) -> None:
        transfer_user_request = TransferUserFactory.build(fromAccountId=funded_account["account"].id,
                                                          toAccountId=99999)

        api_manager.user_steps.user_transfer(transfer_user_request,
                                                funded_account["user"],
                                                ResponseSpec.not_found_code(),
                                                validate_response=False)

        account_from_db_first = Account.account_by_id(db_session, funded_account["account"].id)
        assert account_from_db_first.balance == funded_account["deposit_response"].balance, \
            "DB: После отклонённого перевода баланс отправителя не должен измениться"