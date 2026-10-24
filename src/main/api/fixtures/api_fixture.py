import pytest
from typing import List, Any

from src.main.api.classes.api_manager import ApiManager


@pytest.fixture
def api_manager(created_obj: List[Any]) -> ApiManager:
    return ApiManager(created_obj)