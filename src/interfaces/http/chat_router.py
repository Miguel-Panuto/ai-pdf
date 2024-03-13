from typing import Annotated

from fastapi import APIRouter, Request, Header
from pydantic import BaseModel

from src.app.chat import (
    instantiate_create_new_chat_usecase,
    instantiate_list_chats_usecase,
    instantiate_update_chat_usecase,
    instantiate_send_new_message_usecase,
    instantiate_get_chat_usecase
)

class ChatCreation(BaseModel):
    name: str
    pdf_id: str

class ChatUpdate(BaseModel):
    name: str | None
    pdf_id: str | None

class ChatMessage(BaseModel):
    message: str

router = APIRouter(
    prefix="/api/chat",
    tags=["ai", "chat"],
    responses={404: {"description": "Not found"}},
)

@router.post('/')
async def create_chat(request: Request, x_auth_token: Annotated[str, Header()], body: ChatCreation):
    instantiate_create_new_chat_usecase()
    from src.app.chat import create_new_chat_usecase
    user_id = request.state.user_id
    res = create_new_chat_usecase.execute(user_id, body.name, body.pdf_id)
    return res


@router.get('/')
async def get_chats(
        request: Request, 
        x_auth_token: Annotated[str, Header()],
        name: str | None = None,
        label: str | None = None
):
    instantiate_list_chats_usecase()
    from src.app.chat import list_chats_usecase 
    user_id = request.state.user_id
    res = list_chats_usecase.execute(user_id, name, label)
    return res


@router.put('/{chat_id}')
async def update_chat(
        request: Request, 
        x_auth_token: Annotated[str, Header()],
        chat_id: str,
        body: ChatUpdate
):
    instantiate_update_chat_usecase()
    from src.app.chat import update_chat_usecase
    user_id = request.state.user_id
    res = update_chat_usecase.execute(user_id, chat_id, body.name, body.pdf_id)
    return res

@router.get('/{chat_id}')
async def get_chat(
        request: Request, 
        x_auth_token: Annotated[str, Header()],
        chat_id: str,
):
    instantiate_get_chat_usecase()
    from src.app.chat import get_chat_usecase
    user_id = request.state.user_id
    res = get_chat_usecase.execute(chat_id, user_id)
    return res

@router.post('/{chat_id}/message')
async def send_message(
        request: Request, 
        x_auth_token: Annotated[str, Header()],
        chat_id: str,
        body: ChatMessage
):
    instantiate_send_new_message_usecase()
    from src.app.chat import send_new_message_usecase
    user_id = request.state.user_id
    res = send_new_message_usecase.execute(chat_id, body.message, user_id)
    return res
