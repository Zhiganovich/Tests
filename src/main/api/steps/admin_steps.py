from requests import Response
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.specs.requests_spec import RequestsSpec
from src.main.api.specs.response_spec import ResponseSpec
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest) -> CreateUserResponse:
        response = ValidateCrudRequester(
            request_spec=RequestsSpec.auth_headers(username="admin", password="123456"),
            endpoint=Endpoint.ADMIN_CREATE_USER,
            response_spec=ResponseSpec.success_code()
        ).post(create_user_request)

        self.created_obj.append(response)

        return response

    def delete_user(self, user_id: int) -> Response | None:
        CrudRequester(
            request_spec=RequestsSpec.auth_headers(username="admin", password="123456"),
            endpoint=Endpoint.ADMIN_DELETE_USER,
            response_spec=ResponseSpec.success_code()
            ).delete(user_id)

