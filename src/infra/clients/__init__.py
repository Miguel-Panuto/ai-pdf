from .gcp_storage_client import GcpStorageClient
from .ai_client import AIClient


gcp_storage_client: GcpStorageClient
ai_client: AIClient

def instantiate_gcp_storage_client():
    global gcp_storage_client
    gcp_storage_client = GcpStorageClient('ai_faiss_pdf-prod') 

def instantiate_ai_client():
    global ai_client
    ai_client = AIClient()

