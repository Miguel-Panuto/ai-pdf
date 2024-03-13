from src.infra.database.repositories.pdf_vector_repository import PdfVectorRepository
from src.infra.database.repositories.chat_repository import ChatRepository
from src.types.chat import Chat
from uuid import uuid4 as v4

class CreateNewChatUsecase:
    def __init__(self, chat_repository: ChatRepository, pdf_vector_repository: PdfVectorRepository):
        self.chat_repository = chat_repository
        self.pdf_vector_repository = pdf_vector_repository

    def execute(self,  user_id: int, name: str, pdf_uuid: str):
        call_name = '[CreateNewChatUsecase][execute]'
        print(f'{call_name} - Creating new chat for user: {user_id}')
        pdf_id = self.pdf_vector_repository.get_id_by_uuid(pdf_uuid, user_id)
        chat = Chat(user_id=user_id, pdf_id=pdf_id, name=name, uuid=str(v4()))
        return self.chat_repository.create(chat)
