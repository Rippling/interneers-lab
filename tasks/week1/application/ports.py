from abc import ABC, abstractmethod
from domain.user import User  # Imports from the core

class UserRepositoryPort(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> User:
        pass