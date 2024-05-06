from fastapi import APIRouter

from .endpoints import chat, get_chat_history, get_playground

router = APIRouter(tags=["playground"])
router.add_api_route("/playground/{playground_id}/chat", chat, methods=["POST"])
router.add_api_route("/playground/{playground_id}", get_playground, methods=["GET"])
router.add_api_route(
    "/playground/{playground_id}/chat", get_chat_history, methods=["GET"]
)
