from http import HTTPStatus
from requests import Response


class ResponseSpec:
    @staticmethod
    def success_code():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def created_code():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    @staticmethod
    def bad_code():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod
    def not_found_code():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text
        return confirm

    @staticmethod
    def unprocessable_code():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text
        return confirm