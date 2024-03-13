from dotenv import load_dotenv
from sys import argv
from src.infra.database.repositories import instantiate_pdf_vector_repository, instantiate_user_repository, instantiate_chat_repository

from src.interfaces.http.server import start_server 

from src.infra.database import instantiate_database_engine
from src.infra.clients import instantiate_gcp_storage_client, instantiate_ai_client

import asyncio
import sys
from paths import PROJECT_ROOT 



def main():
    sys.path.insert(1, PROJECT_ROOT)

    is_dev = False

    for arg in argv:
        if arg == '--dev-mode':
            is_dev = True

    load_dotenv()
    instantiate_database_engine()
    instantiate_gcp_storage_client()
    instantiate_ai_client()
    instantiate_pdf_vector_repository()
    instantiate_user_repository()
    instantiate_chat_repository()

    asyncio.run(start_server()) # type: ignore


if __name__ == "__main__":
    main()
