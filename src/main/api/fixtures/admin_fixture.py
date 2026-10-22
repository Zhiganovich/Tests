import pytest

from src.main.api.models.generators.factory import CreateUserFactory


@pytest.fixture
def create(api_manager):
    def create_user():
        create_user_request = CreateUserFactory.build()
        api_manager.admin_steps.create_user(create_user_request)
        return create_user_request
    return create_user