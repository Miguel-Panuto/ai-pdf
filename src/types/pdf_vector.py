from pydantic import BaseModel


class PdfVector(BaseModel):
    user_id: int 
    vectorstore_path: str
    label: str | None
    uuid: str
