"""
MinIO storage service for managing file uploads.
"""
from minio import Minio
from minio.error import S3Error
from io import BytesIO
import logging
from config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """Service for managing file storage in MinIO."""
    
    def __init__(self):
        """Initialize MinIO client."""
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        self._ensure_buckets_exist()
    
    def _ensure_buckets_exist(self):
        """Ensure required buckets exist."""
        for bucket_name in [settings.MINIO_BUCKET_CONTRACTS, settings.MINIO_BUCKET_REPORTS]:
            try:
                if not self.client.bucket_exists(bucket_name):
                    self.client.make_bucket(bucket_name)
                    logger.info(f"Created bucket: {bucket_name}")
            except S3Error as e:
                logger.error(f"Error checking/creating bucket {bucket_name}: {str(e)}")
    
    def upload_file(self, file_path: str, bucket_name: str, object_name: str) -> str:
        """
        Upload a file to MinIO.
        
        Args:
            file_path: Local file path
            bucket_name: Target bucket name
            object_name: Object name in bucket
            
        Returns:
            Object path/URL
            
        Raises:
            Exception: If upload fails
        """
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
            logger.info(f"Uploaded {object_name} to {bucket_name}")
            return f"{bucket_name}/{object_name}"
        except S3Error as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise Exception(f"Failed to upload file: {str(e)}")
    
    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> bool:
        """
        Download a file from MinIO.
        
        Args:
            bucket_name: Source bucket name
            object_name: Object name in bucket
            file_path: Local file path to save to
            
        Returns:
            True if successful
            
        Raises:
            Exception: If download fails
        """
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            logger.info(f"Downloaded {object_name} from {bucket_name}")
            return True
        except S3Error as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise Exception(f"Failed to download file: {str(e)}")
    
    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        """
        Delete a file from MinIO.
        
        Args:
            bucket_name: Bucket name
            object_name: Object name
            
        Returns:
            True if successful
        """
        try:
            self.client.remove_object(bucket_name, object_name)
            logger.info(f"Deleted {object_name} from {bucket_name}")
            return True
        except S3Error as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise Exception(f"Failed to delete file: {str(e)}")
