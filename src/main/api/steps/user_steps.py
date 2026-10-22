from src.main.api.foundation.endpoint import Endpoint
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_user_request import TransferUserRequest
from src.main.api.specs.requests_spec import RequestsSpec
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester


class UserSteps:
    def create_account(self, created_user):
        response = ValidateCrudRequester(
            request_spec=RequestsSpec.auth_headers(username=created_user.username, password=created_user.password),
            endpoint=Endpoint.USER_CREATE_ACCOUNT,
            response_spec=ResponseSpec.created_code()
        ).post(None)

        return response

    def deposit_account(self, deposit_request: DepositRequest,
                        created_user,
                        response_spec,
                        validate_response: bool=True):
        if validate_response:
            response = ValidateCrudRequester(
                request_spec=RequestsSpec.auth_headers(username=created_user.username, password=created_user.password),
                endpoint=Endpoint.USER_DEPOSIT,
                response_spec=response_spec
            ).post(deposit_request)

            return response


        response = CrudRequester(
            request_spec=RequestsSpec.auth_headers(username=created_user.username, password=created_user.password),
            endpoint=Endpoint.USER_DEPOSIT,
            response_spec=response_spec
        ).post(deposit_request)

        return response

    def credit_request(self, credit_request: CreditRequest,
                       created_user,
                       response_spec,
                       validate_response: bool=True):
        if validate_response:
            response = ValidateCrudRequester(
                request_spec=RequestsSpec.auth_headers(username=created_user.username, password=created_user.password),
                endpoint=Endpoint.USER_CREDIT_REQUEST,
                response_spec=response_spec
            ).post(credit_request)

            return response

        response = CrudRequester(
            request_spec=RequestsSpec.auth_headers(username=created_user.username, password=created_user.password),
            endpoint=Endpoint.USER_CREDIT_REQUEST,
            response_spec=response_spec
        ).post(credit_request)

        return response

    def user_transfer(self, transfer_user_request: TransferUserRequest,
                      created_user,
                      response_spec,
                      validate_response: bool=True):
        if validate_response:
            response = ValidateCrudRequester(
                request_spec=RequestsSpec.auth_headers(username=created_user.username, password=created_user.password),
                endpoint=Endpoint.USER_TRANSFER,
                response_spec=response_spec
            ).post(transfer_user_request)

            return response

        response = CrudRequester(
            request_spec=RequestsSpec.auth_headers(username=created_user.username, password=created_user.password),
            endpoint=Endpoint.USER_TRANSFER,
            response_spec=response_spec
        ).post(transfer_user_request)

        return response

    def credit_repay(self, credit_repay_request: CreditRepayRequest,
                     created_user,
                     response_spec,
                     validate_response: bool=True):
        if validate_response:
            response = ValidateCrudRequester(
                request_spec=RequestsSpec.auth_headers(username=created_user.username, password=created_user.password),
                endpoint=Endpoint.USER_REPAY_CREDIT,
                response_spec=response_spec
            ).post(credit_repay_request)

            return response

        response = CrudRequester(
            request_spec=RequestsSpec.auth_headers(username=created_user.username, password=created_user.password),
            endpoint=Endpoint.USER_REPAY_CREDIT,
            response_spec=response_spec
        ).post(credit_repay_request)

        return response