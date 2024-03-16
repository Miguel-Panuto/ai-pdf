from pydantic import BaseModel

class PdfModel(BaseModel):
    label: str
    uuid: str

class PdfCreation(BaseModel):
    message: str
    relation: PdfModel

class QuoteModelReturn(BaseModel):
    quote_relative: str
