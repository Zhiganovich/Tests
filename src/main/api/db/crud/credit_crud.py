from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit
import allure

class CreditCrud:
    @staticmethod
    def credit_by_id(db: Session, id: int) -> Credit | None:
        with allure.step(f"Get credit by id: {id}"):
            credit = db.query(Credit).filter_by(id=id).first()
            allure.attach(f"Find credit by id: {credit}", name="Credit fromDB", attachment_type=allure.attachment_type.TEXT)
        return db.query(Credit).filter_by(account_id=id).first()