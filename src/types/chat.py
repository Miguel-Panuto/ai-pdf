from pydantic import BaseModel


class Chat(BaseModel):
    user_id: int 
    pdf_id: int 
    name: str
    uuid: str

class ChatFinded(BaseModel):
    name: str
    uuid: str
    chat_id: int
    pdf: dict
