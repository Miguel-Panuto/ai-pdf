from pydantic import BaseModel

from src.interfaces.http.types.pdf_responses import PdfModel 

class ChatResponse(BaseModel):
    name: str
    uuid: str

class ChatResponsePdf(ChatResponse):
    pdf: PdfModel

class AiReply(BaseModel):
    content: str
    additional_kwargs: dict
    type: str
    name: str | None
    id: str | None
    example: bool

class ChatResponsePdfMessage(BaseModel):
    chat: ChatResponsePdf
    messages: list[AiReply]

class SendMessageResponse(BaseModel):
    question: str
    answer: str
    chat_history: list[AiReply] | None
