from typing import Annotated

from fastapi import APIRouter, Depends, Form, File, Request, Header, UploadFile
from fastapi.responses import JSONResponse

from dependency_injector.wiring import inject, Provide

from src.app.pdf.find_relative_quotes_usecase import FindRelativeQuotesUsecase
from src.app.pdf.get_pdfs_usecase import GetPdfsUseCase
from src.app.pdf.new_pdf_embedding_usecase import NewPdfEmbeddingUsecase
from src.interfaces.http.types.pdf_requests import QuoteModel

from src.container import Container
from src.interfaces.http.types.pdf_responses import PdfCreation, PdfModel, QuoteModelReturn 

router = APIRouter(
    prefix="/api/pdf",
    tags=["ai", "pdf"],
    responses={403: {"description": "Unauthorized"}},
)


@router.post("/upload", response_model=PdfCreation)
@inject
async def upload_pdf(
        request: Request,
        x_auth_token: Annotated[str, Header()],
        file: Annotated[UploadFile, File()],
        label: Annotated[str | None, Form()] = None,
        new_pdf_embedding_usecase: NewPdfEmbeddingUsecase = Depends(Provide[Container.new_pdf_embedding_usecase]),
):
    if file.content_type != 'application/pdf':
        return JSONResponse(content={"detail": "Invalid file type"}, status_code=400)
    user_id = request.state.user_id
    res = new_pdf_embedding_usecase.execute(file, user_id, label)
    return JSONResponse(content=res, status_code=201)

@router.get('/', response_model=list[PdfModel])
@inject
async def get_pdfs(
        request: Request,
        x_auth_token: Annotated[str, Header()],
        label: str | None = None,
        get_pdfs_usecase: GetPdfsUseCase = Depends(Provide[Container.get_pdfs_usecase])
):
    user_id = request.state.user_id
    res = get_pdfs_usecase.execute(user_id, label)
    return JSONResponse(content=res, status_code=200)

@router.post('/relative_quotes/{pdf_id}', response_model=list[QuoteModelReturn])
@inject
async def get_relative_quotes(
        request: Request,
        x_auth_token: Annotated[str, Header()],
        pdf_id: str,
        body: QuoteModel,
    find_relative_quotes_usecase: FindRelativeQuotesUsecase = Depends(Provide[Container.find_relative_quotes_usecase])
):
    user_id = request.state.user_id
    res = find_relative_quotes_usecase.execute(user_id, pdf_id, body.quote)
    return JSONResponse(content=res, status_code=200)
