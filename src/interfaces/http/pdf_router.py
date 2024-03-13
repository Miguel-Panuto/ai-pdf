from typing import Annotated 

from fastapi import APIRouter, Form, File, Request, Header
from pydantic import BaseModel

from src.app.pdf import instantiate_find_relative_quotes_usecase, instantiate_get_pdfs_usecase, instantiate_new_pdf_embedding_usecase, unload_find_relative_quotes_usecase, unload_new_pdf_embedding_usecase, unload_get_pdfs_usecase

router = APIRouter(
    prefix="/api/pdf",
    tags=["ai", "pdf"],
    responses={404: {"description": "Not found"}},
)

class QuoteModel(BaseModel):
    quote: str

@router.post("/upload")
async def upload_pdf(
        request: Request,
        x_auth_token: Annotated[str, Header()],
        file: Annotated[bytes, File()],
        label: Annotated[str | None, Form()] = None,
        tags: Annotated[str | None, Form()] = None
):
    instantiate_new_pdf_embedding_usecase()
    from src.app.pdf import new_pdf_embedding_usecase
    user_id = request.state.user_id
    res = new_pdf_embedding_usecase.execute(file, user_id, label, tags)
    unload_new_pdf_embedding_usecase()
    return res

@router.get('/')
async def get_pdfs(request: Request, x_auth_token: Annotated[str, Header()], label: str | None = None):
    instantiate_get_pdfs_usecase()
    from src.app.pdf import get_pdfs_usecase
    user_id = request.state.user_id
    res = get_pdfs_usecase.execute(user_id, label)
    unload_get_pdfs_usecase()
    return res

@router.post('/relative_quotes/{pdf_id}')
async def get_relative_quotes(request: Request, x_auth_token: Annotated[str, Header()], pdf_id: str, body: QuoteModel):
    call_name = "[router][get_relative_quotes]"
    print(f"{call_name} - Getting relative quotes")
    instantiate_find_relative_quotes_usecase()
    from src.app.pdf import find_relative_quotes_usecase
    user_id = request.state.user_id
    res = find_relative_quotes_usecase.execute(user_id, pdf_id, body.quote)
    unload_find_relative_quotes_usecase()
    return res
