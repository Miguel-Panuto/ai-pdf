from .create_new_chat_usecase import CreateNewChatUsecase
from .list_chats_usecase import ListChatsUsecase
from .update_chat_usecase import UpdateChatUsecase
from .send_new_message_usecase import SendNewMessageUseCase
from .get_chat_usecase import GetChatUsecase

create_new_chat_usecase: CreateNewChatUsecase
list_chats_usecase: ListChatsUsecase
update_chat_usecase: UpdateChatUsecase
send_new_message_usecase: SendNewMessageUseCase
get_chat_usecase: GetChatUsecase

def instantiate_create_new_chat_usecase():
    from src.infra.database.repositories import chat_repository
    from src.infra.database.repositories import pdf_vector_repository 
    global create_new_chat_usecase
    create_new_chat_usecase = CreateNewChatUsecase(chat_repository, pdf_vector_repository)

def instantiate_list_chats_usecase():
    from src.infra.database.repositories import chat_repository
    global list_chats_usecase
    list_chats_usecase = ListChatsUsecase(chat_repository)

def instantiate_update_chat_usecase():
    from src.infra.database.repositories import chat_repository
    from src.infra.database.repositories import pdf_vector_repository
    global update_chat_usecase
    update_chat_usecase = UpdateChatUsecase(chat_repository, pdf_vector_repository)

def instantiate_send_new_message_usecase():
    from src.infra.clients import ai_client, gcp_storage_client
    from src.infra.database.repositories import chat_repository
    global send_new_message_usecase
    send_new_message_usecase = SendNewMessageUseCase(ai_client, chat_repository, gcp_storage_client)

def instantiate_get_chat_usecase():
    from src.infra.clients import ai_client
    from src.infra.database.repositories import chat_repository
    global get_chat_usecase
    get_chat_usecase = GetChatUsecase(chat_repository, ai_client)


def unload_create_new_chat_usecase():
    global create_new_chat_usecase
    create_new_chat_usecase = None # type: ignore

def unload_list_chats_usecase():
    global list_chats_usecase
    list_chats_usecase = None # type: ignore

def unload_update_chat_usecase():
    global update_chat_usecase
    update_chat_usecase = None # type: ignore

def unload_send_new_message_usecase():
    global send_new_message_usecase
    send_new_message_usecase = None # type: ignore

def unload_get_chat_usecase():
    global get_chat_usecase
    get_chat_usecase = None # type: ignore
