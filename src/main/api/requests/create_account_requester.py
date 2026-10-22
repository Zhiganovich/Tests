import requests
from http import HTTPStatus
from requests import Response

from src.main.api.requests.requester import Requester
from src.main.api.models.create_account_response import CreateAccountResponse

class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountResponse | Response:
        url=f"{self.base_url}/api/account/create"
        response = requests.post(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in (HTTPStatus.CREATED, HTTPStatus.OK):
            return CreateAccountResponse(**response.json())
        return response