from qdrant_client import QdrantClient
from api_service.settings import settings
from .s3 import S3Client
from celery.app import Celery

qdrant = QdrantClient(settings.QDRANT_SERVER_URI)
s3_client = S3Client(
    "ragit-file-uploads",
    settings.S3_URI,
    "blr1",
    settings.S3_KEY,
    settings.S3_SECRET,
)

broker_uri = "redis://localhost:6379"

celery_app = Celery(__name__, broker=broker_uri, backend=broker_uri)

__all__ = ["qdrant", "s3_client", "celery_app"]
