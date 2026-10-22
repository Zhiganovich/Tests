import requests
from requests import Response
from http import HTTPStatus

from src.main.api.requests.requester import Requester
from src.main.api.models.credit_repay_response import CreditRepayResponse

class RepayRequester(Requester):
    def post(self, credit_repay_request) -> CreditRepayResponse | Response:
        url=f"{self.base_url}/api/credit/repay"
        response = requests.post(
            url=url,
            json=credit_repay_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)
        if response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED):
            return CreditRepayResponse(**response.json())
        return response