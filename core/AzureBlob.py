from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings
from core.config import settings
import uuid
import os

class AzureBlobService:
    def __init__(self):
        self.connection_string = settings.AzureConnection_string
        self.container_name = "doctres-files"
        self.service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.service_client.get_container_client(self.container_name)
 
        try:
            self.container_client.create_container(public_access='blob')  
        except Exception:
            pass  

    def upload_file(self, file_data: bytes, content_type: str, original_filename: str) -> dict:
        unique_name = f"{uuid.uuid4()}_{original_filename}"

        blob_client: BlobClient = self.container_client.get_blob_client(unique_name)

        blob_client.upload_blob(
            file_data,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type)
        )

        blob_url = f"https://{self.service_client.account_name}.blob.core.windows.net/{self.container_name}/{unique_name}"

        return {
            "blob_url": blob_url,
            "blob_name": unique_name
        }

    def delete_blob(self, blob_name: str) -> bool:
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.delete_blob()
        return True
    
    
AzureBlobObj = AzureBlobService()

