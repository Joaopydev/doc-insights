from abc import ABC, abstractmethod


class JWTPort(ABC):

    @abstractmethod
    def signin_access_token(self, user_id: str):
        pass

    @abstractmethod
    def validate_access_token(self, token: str):
        pass
