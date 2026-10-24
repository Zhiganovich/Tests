import pytest
from typing import List, Any

from src.main.api.steps.admin_steps import AdminSteps


@pytest.fixture
def created_obj() -> List[Any]:
    users: List[Any]=[]
    yield users
    for user in users:
        if user.id:
            AdminSteps(users).delete_user(user.id)