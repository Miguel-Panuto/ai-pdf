from os import path, remove

from src.infra.clients.gcp_storage_client import GcpStorageClient
from src.infra.clients.ai_client import AIClient
from src.infra.database.repositories.chat_repository import ChatRepository

from paths import PROJECT_ROOT

import shutil

from src.utils.decorators import cleanup_tmp_files

class SendNewMessageUseCase:
    def __init__(self, ai_client: AIClient, chat_repository: ChatRepository, gcp_storage_client: GcpStorageClient):
        self.ai_client = ai_client
        self.chat_repository = chat_repository
        self.gcp_storage_client = gcp_storage_client

    def _download_vectorstore(self, vectorstore_path) -> str:
        call_name = "[SendNewMessageUseCase[_download_vectorstore]"
        print(f"{call_name} - Downloading vectorstore")
        tmp_folder = path.join(PROJECT_ROOT, "tmp")
        self.gcp_storage_client.download_file(f'{vectorstore_path}', f'{tmp_folder}/{vectorstore_path}.zip')
        shutil.unpack_archive(f'{tmp_folder}/{vectorstore_path}.zip', f'{tmp_folder}/{vectorstore_path}')
        return f'{tmp_folder}/{vectorstore_path}'

    def _delete_tmp_files(self, path_saved: str):
        if path.isdir(path_saved):
            shutil.rmtree(path_saved)
        if path.isfile(f"{path_saved}.zip"):
            remove(f"{path_saved}.zip")

    @cleanup_tmp_files
    def execute(self, chat_uuid: str, message: str, user_id: int):
        call_name = '[SendNewMessageUseCase][execute]'
        print(f'{call_name} - Start')
        chat = self.chat_repository.find_vectorstore_and_id(user_id, chat_uuid)
        self.vectorstore_path = self._download_vectorstore(chat['vectorstore'])
        result = self.ai_client.send_new_message(chat['id'], message, self.vectorstore_path)
        return result
