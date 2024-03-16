from pydantic import BaseModel


class ChatCreation(BaseModel):
    name: str
    pdf_id: str

class ChatUpdate(BaseModel):
    name: str | None
    pdf_id: str | None

class ChatMessage(BaseModel):
    message: str
