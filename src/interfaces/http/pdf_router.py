from typing import Annotated

from fastapi import APIRouter, Depends, Form, File, Request, Header
from fastapi.responses import JSONResponse

from dependency_injector.wiring import inject, Provide

from src.app.pdf.new_pdf_embedding_usecase import NewPdfEmbeddingUsecase
from src.interfaces.http.types.pdf_requests import QuoteModel

from src.container import Container

router = APIRouter(
    prefix="/api/pdf",
    tags=["ai", "pdf"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload")
@inject
async def upload_pdf(
        request: Request,
        x_auth_token: Annotated[str, Header()],
        file: Annotated[bytes, File()],
        label: Annotated[str | None, Form()] = None,
        tags: Annotated[str | None, Form()] = None,
        new_pdf_embedding_usecase: NewPdfEmbeddingUsecase = Depends(Provide[Container.new_pdf_embedding_usecase]),
):
    user_id = request.state.user_id
    res = new_pdf_embedding_usecase.execute(file, user_id, label, tags)
    return JSONResponse(content=res, status_code=201)

@router.get('/')
@inject
async def get_pdfs(
        request: Request,
        x_auth_token: Annotated[str, Header()],
        label: str | None = None,
        get_pdfs_usecase = Depends(Provide[Container.get_pdfs_usecase])
):
    user_id = request.state.user_id
    res = get_pdfs_usecase.execute(user_id, label)
    return JSONResponse(content=res, status_code=200)

@router.post('/relative_quotes/{pdf_id}')
@inject
async def get_relative_quotes(
        request: Request,
        x_auth_token: Annotated[str, Header()],
        pdf_id: str,
        body: QuoteModel,
        find_relative_quotes_usecase = Depends(Provide[Container.find_relative_quotes_usecase])
):
    user_id = request.state.user_id
    res = find_relative_quotes_usecase.execute(user_id, pdf_id, body.quote)
    return JSONResponse(content=res, status_code=200)
