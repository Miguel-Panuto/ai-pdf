from pydantic import BaseModel

class QuoteModel(BaseModel):
    quote: str
