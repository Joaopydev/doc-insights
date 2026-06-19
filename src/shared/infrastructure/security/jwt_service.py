from datetime import datetime, timezone, timedelta
import jwt

from src.shared.application.ports.jwt_port import JWTPort
from src.main.config.settings import settings


class JWTService(JWTPort):

    def signin_access_token(self, user_id: str):
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "iss": "SecurityService",
            "iat": int(now.timestamp()),
            "exp": now + timedelta(days=3)
        }

        return jwt.encode(
            payload=payload,
            key=settings.jwt_private_key,
            algorithm="RS256"
        )


    def validate_access_token(self, token: str):
        try:
            payload_data = jwt.decode(
                jwt=token,
                key=settings.jwt_public_key,
                algorithms=["RS256"],
                issuer="SecurityService"
            )

            return payload_data.get("user_id")
        except jwt.exceptions.PyJWTError:
            return None
