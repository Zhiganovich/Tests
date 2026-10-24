from typing import Dict
import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.db.crud.credit_crud import CreditCrud as Credit
from src.main.api.db.crud.account_crud import AccountDb as Account

@pytest.mark.api
class TestUserRepay:
    def test_user_repay(self, api_manager: ApiManager, create_credit: Dict, db_session: Session) -> None:
        repay_credit_request = CreditRepayRequest(creditId=create_credit["credit_response"].creditId,
                                                  accountId=create_credit["account"].id,
                                                  amount=create_credit["credit_request"].amount
                                                  )
        repay_credit_response = api_manager.user_steps.credit_repay(repay_credit_request,
                                                                    create_credit["user"],
                                                                    ResponseSpec.success_code(),
                                                                    validate_response=True
                                                                    )

        assert repay_credit_response.creditId == repay_credit_request.creditId, \
            "API: Переданный id кредита отличается от полученного"
        assert repay_credit_response.amountDeposited == repay_credit_request.amount, \
            "API: Сумма погашения в ответе не соответствует отправленной"

        credit_from_db = Credit.credit_by_id(db_session, create_credit["credit_response"].id)
        assert credit_from_db.balance == 0, \
            "DB: После полного погашения задолженность по кредиту должна быть равна 0"

        account_from_db = Account.account_by_id(db_session, create_credit["account"].id)
        assert account_from_db.balance == 0, \
            "DB: После погашения кредита баланс не равен 0"


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
    def test_user_repay_invalid(self, amount: int, api_manager: ApiManager, create_credit: Dict, db_session: Session) -> None:
        credit_before_repay = Credit.credit_by_id(db_session, create_credit["credit_response"].id)
        balance_before_repay = credit_before_repay.balance

        repay_credit_request = CreditRepayRequest(creditId=create_credit["credit_response"].creditId,
                                                  accountId=create_credit["account"].id,
                                                  amount=amount
                                                  )
        api_manager.user_steps.credit_repay(repay_credit_request,
                                            create_credit["user"],
                                            ResponseSpec.unprocessable_code(),
                                            validate_response=False
                                            )

        db_session.refresh(credit_before_repay)
        assert credit_before_repay.balance == balance_before_repay, \
            "DB: После отклонённого погашения задолженность по кредиту не должна измениться"


        account_from_db = Account.account_by_id(db_session, create_credit["account"].id)
        assert account_from_db.balance == create_credit["credit_request"].amount, \
            "DB: После отклонённого погашения баланс счёта не должен измениться"