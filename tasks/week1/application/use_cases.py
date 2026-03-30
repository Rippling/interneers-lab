from application.ports import UserRepositoryPort
from domain.user import User

class GetUserUseCase:
    def __init__(self, db_port: UserRepositoryPort):
        self.db_port = db_port

    def execute(self, user_id: int) -> User:
        user = self.db_port.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} does not exist.")
        return user