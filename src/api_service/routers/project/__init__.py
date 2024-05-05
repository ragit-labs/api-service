from fastapi import APIRouter

from .endpoints import create_project, get_project, get_project_by_uuid, get_projects

router = APIRouter(tags=["project"])

router.add_api_route("/project/create", endpoint=create_project, methods=["POST"])
router.add_api_route("/project/get", endpoint=get_projects, methods=["GET"])
router.add_api_route("/project/get/{project_id}", endpoint=get_project, methods=["GET"])
router.add_api_route(
    "/project/getbyuuid/{project_id}", endpoint=get_project_by_uuid, methods=["GET"]
)
