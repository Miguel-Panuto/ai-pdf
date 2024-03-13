from src.infra.database.repositories.pdf_vector_repository import PdfVectorRepository


class GetPdfsUseCase:
    def __init__(self,  pdf_vector_repository: PdfVectorRepository ):
        self.pdf_vector_repository = pdf_vector_repository

    def execute(self, user_id: int, label: str | None):
        call_name = '[GetPdfsUseCase][execute]'
        print(f'{call_name} - Getting user pdfs for user_id: {user_id}')
        return self.pdf_vector_repository.get_user_pdf(user_id, label)
