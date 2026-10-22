import requests
from requests import Response
from http import HTTPStatus

from src.main.api.models.credit_request import CreditRequest
from src.main.api.requests.requester import Requester
from src.main.api.models.credit_response import CreditResponse


class CreateCreditRequester(Requester):
    def post(self, credit_request: CreditRequest) -> CreditResponse | Response:
        url = f"{self.base_url}/api/credit/request"
        response = requests.post(
            url=url,
            json=credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code == HTTPStatus.CREATED:
            return CreditResponse(**response.json())
        return response
