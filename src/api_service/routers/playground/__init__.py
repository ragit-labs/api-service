from fastapi import APIRouter

from .endpoints import (
    chat,
    create_playground_,
    get_chat_history,
    get_playground,
    get_playgrounds,
)

router = APIRouter(tags=["playground"])
router.add_api_route("/playground/{playground_id}/chat", chat, methods=["POST"])
router.add_api_route("/playground/{playground_id}", get_playground, methods=["GET"])
router.add_api_route("/playground/create", create_playground_, methods=["POST"])
router.add_api_route(
    "/playground/{playground_id}/chat", get_chat_history, methods=["GET"]
)
router.add_api_route(
    "/project/{project_id}/playgrounds", get_playgrounds, methods=["GET"]
)
