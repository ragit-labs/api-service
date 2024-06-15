from fastapi import APIRouter

from .endpoints import (
    chat_rentomojo
)

router = APIRouter(tags=["demo", "chat"])
router.add_api_route(
    "/demo/chat/1", endpoint=chat_rentomojo, methods=["POST"]
)
