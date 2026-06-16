from src.shared.application.ports.jwt_port import JWTPort

from src.errors.types.access_token_not_provided import AccesTokenNotProvided
from src.errors.types.invalid_access_token import InvalidAccessToken


class AuthenticationMiddleware:

    def __init__(self, jwt_port: JWTPort):
        self.jwt_port = jwt_port

    def handle(self, headers: dict):
        authorization = headers.get("authorization")

        if authorization is None:
            raise AccesTokenNotProvided("Access token not provided.")

        token = authorization.split(" ")[1]
        user_id = self.jwt_port.validate_access_token(token=token)

        if not user_id:
            raise InvalidAccessToken("Invalid access token.")

        return user_id
