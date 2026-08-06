from typing import Optional
from src.shared.application.ports.jwt_port import JWTPort

from src.errors.types.access_token_not_provided import AccesTokenNotProvided
from src.errors.types.invalid_access_token import InvalidAccessToken


class AuthenticationMiddleware:

    def __init__(self, jwt_port: JWTPort):
        self.jwt_port = jwt_port

    def handle(self, headers: dict, query_params: dict = None) -> str:
        token = self._extract_token(headers, query_params)

        if token is None:
            raise AccesTokenNotProvided("Access token not provided.")

        user_id = self.jwt_port.validate_access_token(token=token)

        if not user_id:
            raise InvalidAccessToken("Invalid access token.")

        return user_id


    def _extract_token(self, headers: dict, query_params: dict) -> Optional[str]:
        token = None
        authorization = headers.get("authorization")

        if authorization:
            token = authorization.split(" ")[1]

        elif query_params:
            token = query_params.get("token")

        return token
