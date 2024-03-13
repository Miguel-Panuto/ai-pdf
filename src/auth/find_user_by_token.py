from src.infra.database.repositories import instantiate_user_repository, unload_repositories

def execute(token: str) -> int:
    from src.infra.database.repositories import user_repository
    call_name = '[find_user_by_token][execute]'
    print(f'{call_name} - Finding user by token: {token}')
    user_id = user_repository.get_user_by_token(token) # type: ignore
    return user_id 
