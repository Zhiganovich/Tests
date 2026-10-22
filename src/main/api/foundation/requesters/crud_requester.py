import requests
import allure
from requests import Response
from typing import Optional
from src.main.api.configs.config import Config
from src.main.api.foundation.https_requester import HttpRequester
from src.main.api.models.base_model import BaseModel


class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel]) -> Response:
        body = model.model_dump() if model is not None else None

        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url}"):
            allure.attach(str(body), name="Request body", attachment_type=allure.attachment_type.JSON)

        response = requests.post(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}",
            json=body,
            headers=self.request_spec
        )

        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url}"):
            allure.attach(str(response.text), "Response body", allure.attachment_type.JSON)

        self.response_spec(response)
        return response

    def delete(self, user_id):
        response = requests.delete(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response