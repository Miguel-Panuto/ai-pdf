from src.infra.clients.ai_client import AIClient
from src.infra.database.repositories.chat_repository import ChatRepository


class GetChatUsecase:
    def __init__(self, chat_repository: ChatRepository, ai_client: AIClient):
        self.chat_repository = chat_repository
        self.ai_client = ai_client

    def execute(self, chat_id: str, user_id: int):
        call_name = "[GetChatUsecase][execute]"
        print(f"{call_name} - Getting chat: {chat_id} for user: {user_id}")
        chat = self.chat_repository.find_by_uuid(user_id, chat_id)
        if type(chat.chat_id) is not int:
            raise ValueError("Chat not found")
        print(f"{call_name} - Chat found: {chat.chat_id}")
        chat_messages = self.ai_client.get_chat_messages(chat.chat_id) # type: ignore
        return {
            'chat': {
                'name': chat.name,
                'uuid': chat.uuid,
                'pdf': chat.pdf
            },
            'messages': chat_messages
        }
