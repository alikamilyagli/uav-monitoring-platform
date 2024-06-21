import logging
import io
from minio import Minio
from minio.error import S3Error

logger = logging.getLogger(__name__)

class MinioUtils:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

    def create_bucket(self, bucket_name):
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
            return True
        except S3Error as e:
            logger.error(f"MinIO error creating bucket: {e}")
            return False

    def upload_image(self, bucket_name, object_name, image_data):
        try:
            if not self.create_bucket(bucket_name):
                return False
            image_data.seek(0)
            self.client.put_object(bucket_name, object_name, image_data, length=image_data.getbuffer().nbytes)
            return True
        except S3Error as e:
            logger.error(f"MinIO error uploading image: {e}")
            return False

    def get_image_url(self, bucket_name, object_name):
        try:
            return self.client.presigned_get_object(bucket_name, object_name)
        except S3Error as e:
            logger.error(f"MinIO error getting image URL: {e}")
            return None
