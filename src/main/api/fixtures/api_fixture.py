import pytest
from typing import List, Any

from src.main.api.classes.api_manager import ApiManger


@pytest.fixture
def api_manager(created_obj: List[Any]):
    return ApiManger(created_obj)