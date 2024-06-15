# from qdrant_client import QdrantClient

from ..settings import settings
from .s3 import S3Client
from .discord import DiscordClient

# qdrant = QdrantClient(settings.QDRANT_SERVER_URI, api_key=settings.QDRANT_SERVER_SECRET)
s3_client = S3Client(
    settings.S3_BUCKET,
    settings.S3_URI,
    "blr1",
    settings.S3_KEY,
    settings.S3_SECRET,
)

discord_client = DiscordClient(token=settings.DISCORD_BOT_TOKEN)

__all__ = ["qdrant", "s3_client", "discord_client"]
