from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps


class ApiManger:
    def __init__(self, created_obj):
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps()