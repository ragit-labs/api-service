from fastapi import APIRouter

from .endpoints import (
    discord_chat
)

router = APIRouter(tags=["discord", "chat"])
router.add_api_route(
    "/chat/discord", endpoint=discord_chat, methods=["POST"]
)
