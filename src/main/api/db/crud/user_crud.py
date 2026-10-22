from sqlalchemy.orm import Session
from src.main.api.db.models.user_table import User
import allure

class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        with allure.step(f"Get user with username: {username}"):
            user = db.query(User).filter_by(username=username).first()
            allure.attach(f"Find user with username: {user}", name="User from DB", attachment_type=allure.attachment_type.TEXT)
        return user