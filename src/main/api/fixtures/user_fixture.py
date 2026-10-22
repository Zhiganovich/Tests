import pytest


@pytest.fixture
def create_account(api_manager, create):
    def create_acc():
        create_user = create()
        created_account = api_manager.user_steps.create_account()
        return created_account
    return create_acc
