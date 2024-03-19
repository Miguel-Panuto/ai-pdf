from io import BytesIO
from os import path, remove

from PyPDF2 import PdfReader
from uuid import uuid4 as v4
from fastapi import UploadFile
from langchain.text_splitter import CharacterTextSplitter

from src.infra.database.repositories.pdf_vector_repository import PdfVectorRepository

from src.infra.clients.ai_client import AIClient
from src.infra.clients.gcp_storage_client import GcpStorageClient

from paths import PROJECT_ROOT
from src.types.pdf_vector import PdfVector

import shutil

from src.utils.decorators import cleanup_tmp_files


import pdf_processor

class NewPdfEmbeddingUsecase:
    def __init__(self, ai_client: AIClient, gcp_storage_client: GcpStorageClient, pdf_vector_repository: PdfVectorRepository):
        self.ai_client = ai_client
        self.gcp_storage_client = gcp_storage_client
        self.pdf_vector_repository = pdf_vector_repository

    def _pages_to_text(self, pdf: bytes) -> str:
        return pdf_processor.process_pdf(pdf)

    def _text_to_chunks(self, text: str) -> list[str]:
        text_splitter = CharacterTextSplitter(separator=".", chunk_size=4000, chunk_overlap=200, length_function=len)
        chunks = text_splitter.split_text(text)
        return chunks

    def _delete_tmp_files(self, path_saved: str):
        if path.isdir(path_saved):
            shutil.rmtree(path_saved)
        if path.isfile(f"{path_saved}.zip"):
            remove(f"{path_saved}.zip")

    def execute(self, pdf: UploadFile, user_id: int, label: str | None):
        call_name = '[new_pdf_embedding_usecase][execute]'
        pdf_bytes = pdf.file.read()
        chunks = self._text_to_chunks(self._pages_to_text(pdf_bytes))

        print(f'{call_name} just created the chunks')
        if not label:
            label = pdf.filename.split(".")[0] # type: ignore
        if len(label) > 30:
            label = label[:30]
        vectorstore = self.ai_client.create_embedding(chunks)
        uuid = str(v4())
        file_name = f'{label}_{uuid}.faiss'
        print(f"{call_name} just created the vectorstore")

        tmp_folder = path.join(PROJECT_ROOT, 'tmp')
        path_to_save = path.join(tmp_folder, file_name)
        vectorstore.save_local(path_to_save)
        self.vectorstore_path = path_to_save
        print(f"{call_name} just saved the vectorstore")
        shutil.make_archive(path_to_save, 'zip', path_to_save)
        self.gcp_storage_client.upload_file(file_name, f"{path_to_save}.zip")

        db = self.pdf_vector_repository.create_relation(
            PdfVector(user_id=user_id, label=label, uuid=uuid, vectorstore_path=file_name)
        )

        return {"message": "vectorstore just created", "relation": db}
