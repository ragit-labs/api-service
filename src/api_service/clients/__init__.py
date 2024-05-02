from qdrant_client import QdrantClient

from api_service.settings import settings

from .s3 import S3Client

qdrant = QdrantClient(settings.QDRANT_SERVER_URI, api_key=settings.QDRANT_SERVER_SECRET)
s3_client = S3Client(
    "ragit-file-uploads",
    settings.S3_URI,
    "blr1",
    settings.S3_KEY,
    settings.S3_SECRET,
)

__all__ = ["qdrant", "s3_client"]
