from src.infra.database.repositories.user_repository import UserRepository
from src.infra.database.repositories.pdf_vector_repository import PdfVectorRepository
from src.infra.database.repositories.chat_repository import ChatRepository


user_repository: UserRepository 
pdf_vector_repository: PdfVectorRepository 
chat_repository: ChatRepository

def instantiate_user_repository():
    from src.infra.database import database_engine
    global user_repository
    user_repository = UserRepository(database_engine)

def instantiate_pdf_vector_repository():
    from src.infra.database import database_engine
    global pdf_vector_repository
    pdf_vector_repository = PdfVectorRepository(database_engine)

def instantiate_chat_repository():
    from src.infra.database import database_engine
    global chat_repository
    chat_repository = ChatRepository(database_engine)

def unload_repositories():
    global user_repository
    global pdf_vector_repository
    global chat_repository
    user_repository = None  # type: ignore
    pdf_vector_repository = None # type: ignore
    chat_repository = None # type: ignore
