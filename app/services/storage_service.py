from b2sdk.v2 import InMemoryAccountInfo, B2Api
from typing import BinaryIO, Dict, Any
import uuid
import os

from app.core.config import settings

class StorageService:
    def __init__(self):
        self.info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.info)
        try:
            self.b2_api.authorize_account(
                "production",
                settings.B2_KEY_ID,
                settings.B2_APPLICATION_KEY
            )
            self.bucket = self.b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)
        except Exception as e:
            print(f"Failed to authorize B2: {e}")
            raise e

    def upload_file(self, file: BinaryIO, filename: str) -> Dict[str, Any]:
        """
        Upload a file to Backblaze B2 using Native API.
        Returns a dictionary with 'url' and 'key'.
        """
        try:
            # Generate a unique key
            ext = os.path.splitext(filename)[1]
            key = f"{uuid.uuid4()}{ext}"
            
            # Determine content type
            content_type = "application/octet-stream"
            if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
                content_type = "image/jpeg"
            elif filename.lower().endswith(".png"):
                content_type = "image/png"

            # Upload
            file.seek(0)
            content = file.read()
            
            uploaded_file = self.bucket.upload_bytes(
                content,
                key,
                content_type=content_type
            )

            # Construct URL
            # Use the download URL from account info
            download_url = self.info.get_download_url()
            # Format: https://f005.backblazeb2.com/file/<bucket_name>/<key>
            url = f"{download_url}/file/{settings.B2_BUCKET_NAME}/{key}"
            
            return {"url": url, "key": key}

        except Exception as e:
            print(f"Error uploading to B2: {e}")
            raise e

    def delete_file(self, file_key: str) -> bool:
        """
        Delete a file from Backblaze B2.
        """
        try:
            file_version = self.bucket.get_file_info_by_name(file_key)
            self.bucket.delete_file_version(file_version.id_, file_key)
            return True
        except Exception as e:
            print(f"Error deleting from B2: {e}")
            return False
            
    def download_file(self, file_key: str) -> tuple[bytes, str]:
        """
        Download a file from Backblaze B2.
        Returns a tuple of (file_content, content_type).
        """
        import tempfile
        import os

        try:
            # Get file info to determine content type
            file_info = self.bucket.get_file_info_by_name(file_key)
            
            # Create a temporary file to store the download
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name

            try:
                # Download the file to the temporary path
                self.bucket.download_file_by_name(file_key).save_to(temp_path)
                
                # Read the file content
                with open(temp_path, 'rb') as f:
                    file_content = f.read()
                
                return file_content, file_info.content_type
                
            finally:
                # Clean up the temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            print(f"Error downloading from B2: {e}")
            raise e
