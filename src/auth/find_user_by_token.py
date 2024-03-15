from src.infra.database.repositories.user_repository import UserRepository
from src.infra.database.database_engine import DatabaseEngine

def execute(token: str) -> int:
    user_repository = UserRepository(DatabaseEngine())
    call_name = '[find_user_by_token][execute]'
    print(f'{call_name} - Finding user by token: {token}')
    user_id = user_repository.get_user_by_token(token) # type: ignore
    return user_id 
