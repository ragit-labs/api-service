from fastapi import APIRouter

from .endpoints import get_user, login, signup

router = APIRouter(tags=["auth", "login"])
router.add_api_route("/auth/signup", endpoint=signup, methods=["POST"])
router.add_api_route("/auth/login", endpoint=login, methods=["POST"])
router.add_api_route("/auth/get", endpoint=get_user, methods=["GET"])
