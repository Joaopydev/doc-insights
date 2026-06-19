import bcrypt

from src.identity.application.ports.password_hasher import (
    PasswordHasher as PasswordHasherInterface
)


class PasswordHasher(PasswordHasherInterface):

    def hash(self, password: str) -> str:
        return bcrypt.hashpw(
            password=password.encode("utf-8"),
            salt=bcrypt.gensalt(8),
        ).decode("utf-8")

    def verify(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8")
        )
