from fastapi import APIRouter

from .endpoints import get_project_for_user

router = APIRouter(tags=["project"])

# router.add_api_route("/project/create", endpoint=create_project, methods=["POST"])
router.add_api_route("/project/get", endpoint=get_project_for_user, methods=["GET"])
# router.add_api_route("/project/get/{project_id}", endpoint=get_project, methods=["GET"])
