import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///uav.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'minio:9000')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'miniouser')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'miniopw123')
    MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME', 'uav-images')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
    DEBUG = os.environ.get('DEBUG', False)
