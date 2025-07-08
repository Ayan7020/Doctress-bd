from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings , generate_blob_sas , BlobSasPermissions
from core.config import settings
from datetime import datetime, timedelta
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
        
        sas_token = self.generate_blob_sas_url(unique_name)

        blob_url = f"https://{self.service_client.account_name}.blob.core.windows.net/{self.container_name}/{unique_name}?{sas_token}"

        return {
            "blob_url": blob_url,
            "blob_name": unique_name
        }

    def generate_blob_sas_url(self,blob_name: str, expiry_minutes=60):
        sas_token = generate_blob_sas(
            account_name=self.service_client.account_name,
            container_name=self.container_name,
            blob_name=blob_name,
            account_key=settings.AzureKey,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes)
        )
        return sas_token
    
    def delete_blob(self, blob_name: str) -> bool:
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.delete_blob()
        return True
    
    
AzureBlobObj = AzureBlobService()

