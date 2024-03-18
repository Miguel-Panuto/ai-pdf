from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Request, Header, Depends

from src.app.chat.get_chat_usecase import GetChatUsecase
from src.app.chat.list_chats_usecase import ListChatsUsecase
from src.app.chat.update_chat_usecase import UpdateChatUsecase
from src.container import Container
from src.interfaces.http.types.chat_requests import ChatCreation, ChatMessage, ChatUpdate
from src.interfaces.http.types.chat_responses import ChatResponse, ChatResponsePdf, ChatResponsePdfMessage, SendMessageResponse


router = APIRouter(
    prefix="/api/chat",
    tags=["ai", "chat"],
    responses={403: {"description": "Unauthorized"}},
)

@router.post('/', response_model=ChatResponse)
@inject
async def create_chat(
        request: Request,
        x_auth_token: Annotated[str, Header()],
        body: ChatCreation,
        create_new_chat_usecase = Depends(Provide[Container.create_new_chat_usecase])
):
    user_id = request.state.user_id
    res = create_new_chat_usecase.execute(user_id, body.name, body.pdf_id)
    return res


@router.get('/', response_model=list[ChatResponsePdf])
@inject
async def get_chats(
        request: Request, 
        x_auth_token: Annotated[str, Header()],
        name: str | None = None,
        label: str | None = None,
    list_chats_usecase: ListChatsUsecase = Depends(Provide[Container.list_chats_usecase])
):
    user_id = request.state.user_id
    res = list_chats_usecase.execute(user_id, name, label)
    return res


@router.put('/{chat_id}', response_model=ChatResponsePdf)
@inject
async def update_chat(
        request: Request, 
        x_auth_token: Annotated[str, Header()],
        chat_id: str,
        body: ChatUpdate,
    update_chat_usecase: UpdateChatUsecase = Depends(Provide[Container.update_chat_usecase])
):
    user_id = request.state.user_id
    res = update_chat_usecase.execute(user_id, chat_id, body.name, body.pdf_id)
    return res

@router.get('/{chat_id}', response_model=ChatResponsePdfMessage)
@inject
async def get_chat(
        request: Request, 
        x_auth_token: Annotated[str, Header()],
        chat_id: str,
    get_chat_usecase: GetChatUsecase = Depends(Provide[Container.get_chat_usecase])
):
    user_id = request.state.user_id
    res = get_chat_usecase.execute(chat_id, user_id)
    return res

@router.post('/{chat_id}/message', response_model=SendMessageResponse)
@inject
async def send_message(
        request: Request, 
        x_auth_token: Annotated[str, Header()],
        chat_id: str,
        body: ChatMessage,
        send_new_message_usecase = Depends(Provide[Container.send_new_message_usecase])
):
    user_id = request.state.user_id
    res = send_new_message_usecase.execute(chat_id, body.message, user_id)
    return res
