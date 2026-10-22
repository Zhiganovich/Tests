from abc import ABC, abstractmethod
from typing import Callable, Dict
from src.main.api.models.base_model import BaseModel

class Requester(ABC):
    def __init__(self, requests_spec: Dict[str, str], response_spec: Callable):
        self.base_url = requests_spec["base_url"]
        self.headers = requests_spec["headers"]
        self.response_spec = response_spec


    @abstractmethod
    def post(self, model: BaseModel):
        ...