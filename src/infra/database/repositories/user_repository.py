from pydantic import BaseModel

from src.infra.database.database_engine import DatabaseEngine


class UserDatabase(BaseModel):
    id: str
    email: str
    username: str


class UserRepository:
    def __init__(self, database_engine: DatabaseEngine):
        self.db = database_engine

    def create_user(self, user: UserDatabase):
        call_name = '[UserRepository][create_user]'
        print(f'{call_name} - Creating user: {user}')
        user_db = self.db.sql_one(
            f'INSERT INTO aidpdf.user (email, username, uuid) VALUES ({user.email}, {user.username}, {user.id}) RETURNING *')
        return {
            'id': user_db[0],
            'email': user_db[1],
            'username': user_db[2]
        }

    def get_user_by_token(self, token: str) -> int:
        call_name = '[UserRepository][get_user_by_token]'
        print(f'{call_name} - Getting user by token: {token}')
        (user_id, *_) = self.db.sql_one(
            f"SELECT user_id FROM aipdf.tokens WHERE token_sequence = '{token}'")
        return int(user_id)
