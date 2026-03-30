from application.ports import UserRepositoryPort
from domain.user import User

class SQLiteUserAdapter(UserRepositoryPort):
    def __init__(self):
        self.fake_db = {
            1: User(1, "Alice"),
            2: User(2, "Bob")
        }

    def get_user(self, user_id: int) -> User:
        return self.fake_db.get(user_id)