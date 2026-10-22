from http import HTTPStatus
import requests

from requests import Response

from src.main.api.models.transfer_user_request import TransferUserRequest
from src.main.api.models.transfer_user_response import TransferUserResponse
from src.main.api.requests.requester import Requester


class TransferUserRequester(Requester):
    def post(self, transfer_user_request: TransferUserRequest) -> TransferUserResponse | Response:
         url = f'{self.base_url}/api/account/transfer'
         response = requests.post(
             url=url,
             json=transfer_user_request.model_dump(),
             headers=self.headers
         )
         self.response_spec(response)
         if response.status_code == HTTPStatus.OK:
             return TransferUserResponse(**response.json())
         return response