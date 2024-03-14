from dotenv import load_dotenv
from src.infra.database.repositories import instantiate_pdf_vector_repository, instantiate_user_repository, instantiate_chat_repository

from src.interfaces.http.server import start_server 

from src.infra.database import instantiate_database_engine
from src.infra.clients import instantiate_gcp_storage_client, instantiate_ai_client

import asyncio
import sys
from os import environ
from paths import PROJECT_ROOT 


def create_gcp_keys():
    gcp_json_plain = environ.get('GCP_KEYS_JSON')
    with open('gcp-keys.json', 'w', encoding='utf-8') as f:
        if gcp_json_plain is None:
            print('GCP_KEYS_JSON is not set')
            return
        f.write(gcp_json_plain)

def main():
    sys.path.insert(1, PROJECT_ROOT)
    load_dotenv()
    create_gcp_keys()

    instantiate_database_engine()
    instantiate_gcp_storage_client()
    instantiate_ai_client()
    instantiate_pdf_vector_repository()
    instantiate_user_repository()
    instantiate_chat_repository()

    asyncio.run(start_server()) # type: ignore


if __name__ == "__main__":
    main()
