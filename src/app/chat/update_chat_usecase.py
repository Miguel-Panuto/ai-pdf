from src.infra.database.repositories.chat_repository import ChatRepository
from src.infra.database.repositories.pdf_vector_repository import PdfVectorRepository


class UpdateChatUsecase:
    def __init__(self, chat_repository: ChatRepository, pdf_vector_repository: PdfVectorRepository):
        self.chat_repository = chat_repository
        self.pdf_vector_repository = pdf_vector_repository

    def execute(self, user_id: int, chat_id: str, name: str | None = None, pdf_uuid: str | None = None):
        if not name and not pdf_uuid:
            return {'error': 'Nothing to update'}

        update_stmt = 'SET '
        if pdf_uuid:
            pdf_id = self.pdf_vector_repository.get_id_by_uuid(str(pdf_uuid), user_id)
            update_stmt += f'pdf_id = {pdf_id},'
        if name: 
            update_stmt += f"name = '{name}' "
        return self.chat_repository.update(user_id, chat_id, update_stmt)

