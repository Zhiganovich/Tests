from sqlalchemy.orm import Session
from src.main.api.db.models.account_table import Account
import allure


class AccountDb:
    @staticmethod
    def account_by_id(db: Session, id: int) -> Account | None:
        with allure.step(f"Get account by id: {id}"):
            account = db.query(Account).filter_by(id=id).first()
            allure.attach(f"Find account: {account}",name="Account from DB", attachment_type=allure.attachment_type.TEXT)
        return account