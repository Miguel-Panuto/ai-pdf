from google.cloud import storage
from google.oauth2 import service_account

from os import environ

class GcpStorageClient:
    def __init__(self, bucket_name: str):
        keys = environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        credentials = service_account.Credentials.from_service_account_file(keys)
        client = storage.Client(credentials=credentials)
        self.bucket = client.get_bucket(bucket_name)


    def download_file(self, file_name: str, destination: str):
        call_name = '[gcp_storage_client][download_file]'
        print(f'{call_name} with file_name: {file_name} and destination: {destination}')
        blob = self.bucket.blob(file_name)
        blob.download_to_filename(destination)

    def upload_file(self, file_name: str, origin: str):
        call_name = '[gcp_storage_client][upload_file]'
        print(f'{call_name} with file_name: {file_name} and destination: {origin}')
        blob = self.bucket.blob(file_name)
        blob.upload_from_filename(origin)
