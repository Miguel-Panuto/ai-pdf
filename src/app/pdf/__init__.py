from .new_pdf_embedding_usecase import NewPdfEmbeddingUsecase
from .get_pdfs_usecase import GetPdfsUseCase 
from .find_relative_quotes_usecase import FindRelativeQuotesUsecase

new_pdf_embedding_usecase: NewPdfEmbeddingUsecase
find_relative_quotes_usecase: FindRelativeQuotesUsecase
get_pdfs_usecase: GetPdfsUseCase

def instantiate_new_pdf_embedding_usecase():
    from src.infra.database.repositories import pdf_vector_repository 
    from src.infra.clients import ai_client, gcp_storage_client
    global new_pdf_embedding_usecase
    new_pdf_embedding_usecase = NewPdfEmbeddingUsecase(ai_client, gcp_storage_client, pdf_vector_repository)

def instantiate_get_pdfs_usecase():
    from src.infra.database.repositories import pdf_vector_repository
    global get_pdfs_usecase
    get_pdfs_usecase = GetPdfsUseCase(pdf_vector_repository)

def instantiate_find_relative_quotes_usecase():
    from src.infra.database.repositories import pdf_vector_repository
    from src.infra.clients import ai_client, gcp_storage_client
    global find_relative_quotes_usecase
    find_relative_quotes_usecase = FindRelativeQuotesUsecase(ai_client, gcp_storage_client, pdf_vector_repository)

def unload_new_pdf_embedding_usecase():
    global new_pdf_embedding_usecase
    new_pdf_embedding_usecase = None # type: ignore

def unload_get_pdfs_usecase():
    global get_pdfs_usecase
    get_pdfs_usecase = None # type: ignore

def unload_find_relative_quotes_usecase():
    global find_relative_quotes_usecase
    find_relative_quotes_usecase = None # type: ignore
