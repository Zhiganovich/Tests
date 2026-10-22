from http import HTTPStatus
from requests import Response
import requests

from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.requests.requester import Requester


class LoginUserRequester(Requester):
    def post(self, login_user_request: LoginUserRequest) -> LoginUserResponse | Response:
        url=f"{self.url}/auth/token/login"
        response = requests.post(
            url=url,
            json=login_user_request.model_dump(),
            headers=self.headers
        )
        self.request_model(response)
        if response.status_code in (HTTPStatus.CREATED, HTTPStatus.ACCEPTED):
            return LoginUserResponse(**response.json())
        return response