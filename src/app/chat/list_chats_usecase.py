from src.infra.database.repositories.chat_repository import ChatRepository

class ListChatsUsecase:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    def execute(self, user_id: int, name: str | None = None, pdf_label: str | None = None):
        call_name = '[CreateNewChatUsecase][execute]'
        print(f'{call_name} - Creating new chat for user: {user_id}')
        return self.chat_repository.list_chats(user_id, name, pdf_label)
