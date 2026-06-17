import bcrypt

from src.identity.application.ports.password_hasher import (
    PasswordHasher as PasswordHasherInterface
)


class PasswordHasher(PasswordHasherInterface):

    def hash(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(8))

    def verify(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
