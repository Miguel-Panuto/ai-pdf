from os import path, remove
from pydantic import BaseModel

from src.infra.database.repositories.pdf_vector_repository import PdfVectorRepository

from src.infra.clients.ai_client import AIClient
from src.infra.clients.gcp_storage_client import GcpStorageClient

from paths import PROJECT_ROOT

import shutil
import re

from src.utils.decorators import cleanup_tmp_files

class QuotesReturn(BaseModel):
    page_content: str
    metadata: list
    type: str


class FindRelativeQuotesUsecase:
    def __init__(self, ai_client: AIClient, gcp_storage_client: GcpStorageClient, pdf_vector_repository: PdfVectorRepository):
        self.ai_client = ai_client
        self.gcp_storage_client = gcp_storage_client
        self.pdf_vector_repository = pdf_vector_repository

    def _delete_tmp_files(self, path_saved: str):
        if path.isdir(path_saved):
            shutil.rmtree(path_saved)
        if path.isfile(f"{path_saved}.zip"):
            remove(f"{path_saved}.zip")

    def _format_quotes(self, quotes: list[QuotesReturn]) -> list[QuotesReturn]:
        quotes_return = []
        for quote in quotes:
            content = quote.page_content
            content = content.replace('-\n', '').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ')
            content = re.sub(r'\. (?=[A-Z])', '. ', content)
            quotes_return.append({
                'quote': content,
            })

        return quotes_return

    def _download_vectorstore(self, uuid: str, user_id: int) -> str:
        call_name = "[find_relative_quotes_usecase][_download_vectorstore]"
        vectorstore_path = self.pdf_vector_repository.get_pdf_vectorstore(uuid, user_id)
        print(f"{call_name} - Downloading vectorstore")
        tmp_folder = path.join(PROJECT_ROOT, "tmp")
        self.gcp_storage_client.download_file(f'{vectorstore_path}', f'{tmp_folder}/{vectorstore_path}.zip')
        shutil.unpack_archive(f'{tmp_folder}/{vectorstore_path}.zip', f'{tmp_folder}/{vectorstore_path}')
        return f'{tmp_folder}/{vectorstore_path}'


    @cleanup_tmp_files
    def execute(self, user_id: int, uuid: str, quote: str):
        call_name = "[find_relative_quotes_usecase][execute]"
        print(f"{call_name} - Getting pdf vectorstore path")
        self.vectorstore_path = self._download_vectorstore(uuid, user_id)
        quote_retrieved: list[QuotesReturn] = self.ai_client.quote_similarity(self.vectorstore_path, quote)
        return self._format_quotes(quote_retrieved)
