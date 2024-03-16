from dependency_injector import containers, providers
from os import environ

# database
from src.infra.database.database_engine import DatabaseEngine
from src.infra.database.repositories.chat_repository import ChatRepository
from src.infra.database.repositories.pdf_vector_repository import PdfVectorRepository 
from src.infra.database.repositories.user_repository import UserRepository

# external services
from src.infra.clients.ai_client import AIClient
from src.infra.clients.gcp_storage_client import GcpStorageClient

# app
# chat
from src.app.pdf.new_pdf_embedding_usecase import NewPdfEmbeddingUsecase
from src.app.pdf.get_pdfs_usecase import GetPdfsUseCase
from src.app.pdf.find_relative_quotes_usecase import FindRelativeQuotesUsecase
# chat
from src.app.chat.create_new_chat_usecase import CreateNewChatUsecase
from src.app.chat.list_chats_usecase import ListChatsUsecase
from src.app.chat.get_chat_usecase import GetChatUsecase
from src.app.chat.update_chat_usecase import UpdateChatUsecase
from src.app.chat.send_new_message_usecase import SendNewMessageUseCase


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['.interfaces.http.chat_router', '.interfaces.http.pdf_router'])
    config = providers.Configuration()

    # Database
    database_engine = providers.Factory(DatabaseEngine)

    # Repositories
    pdf_vector_repository = providers.Factory(PdfVectorRepository, database_engine=database_engine)
    user_repository = providers.Factory(UserRepository, database_engine=database_engine)
    chat_repository = providers.Factory(ChatRepository, database_engine=database_engine)


    # External Services
    gcp_storage_client = providers.Singleton(GcpStorageClient, bucket_name=environ.get('GCP_BUCKET_NAME', 'ai-pdf-api_faiss'))
    ai_client = providers.Singleton(AIClient)


    # App # PDF
    new_pdf_embedding_usecase = providers.Factory(
        NewPdfEmbeddingUsecase,
        pdf_vector_repository=pdf_vector_repository,
        ai_client=ai_client,
        gcp_storage_client=gcp_storage_client
    )
    get_pdfs_usecase = providers.Factory(GetPdfsUseCase, pdf_vector_repository=pdf_vector_repository)
    find_relative_quotes_usecase = providers.Factory(
        FindRelativeQuotesUsecase,
        pdf_vector_repository=pdf_vector_repository,
        gcp_storage_client=gcp_storage_client,
        ai_client=ai_client
    )

    # Chat
    create_new_chat_usecase = providers.Factory(
        CreateNewChatUsecase,
        chat_repository=chat_repository,
        pdf_vector_repository=pdf_vector_repository
    )
    list_chats_usecase = providers.Factory(ListChatsUsecase, chat_repository=chat_repository)
    get_chat_usecase = providers.Factory(GetChatUsecase, chat_repository=chat_repository, ai_client=ai_client)
    update_chat_usecase = providers.Factory(
        UpdateChatUsecase, chat_repository=chat_repository, pdf_vector_repository=pdf_vector_repository
    )
    send_new_message_usecase = providers.Factory(
        SendNewMessageUseCase,
        chat_repository=chat_repository,
        ai_client=ai_client,
        gcp_storage_client=gcp_storage_client
    )

