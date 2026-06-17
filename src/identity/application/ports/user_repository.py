from abc import ABC, abstractmethod

from src.identity.domain.entities.user import UserIdentity

class UserRepository(ABC):

    @abstractmethod
    def insert_user(self, user: UserIdentity):
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> UserIdentity:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserIdentity:
        pass
