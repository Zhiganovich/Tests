import pytest
from typing import Callable
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.generators.factory import CreateUserFactory


@pytest.fixture
def create(api_manager: ApiManager) -> Callable:
    def create_user() -> CreateUserRequest:
        create_user_request = CreateUserFactory.build()
        api_manager.admin_steps.create_user(create_user_request)
        return create_user_request
    return create_user