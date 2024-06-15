from fastapi import APIRouter, Depends

from ...dependencies.auth import login_required
from .endpoints import get_user, login, signup, auth_discord

router = APIRouter(tags=["auth"])
router.add_api_route("/auth/signup", endpoint=signup, methods=["POST"])
router.add_api_route("/auth/login", endpoint=login, methods=["POST"])
router.add_api_route(
    "/auth/get",
    endpoint=get_user,
    methods=["GET"],
    dependencies=[Depends(login_required)],
)
router.add_api_route("/auth/discord", endpoint=auth_discord, methods=["POST"])
