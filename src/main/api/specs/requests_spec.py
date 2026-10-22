# Здесь храним реквест хидеры
import requests

from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestsSpec:
    # base_url = "http://localhost:4111"
    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        login_request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_request.model_dump(),
            headers=RequestsSpec.base_headers()
        )
        if response.status_code == 200:
            login_response = LoginUserResponse(**response.json())
            token = login_response.token
            headers = RequestsSpec.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        raise Exception("Failed to login")