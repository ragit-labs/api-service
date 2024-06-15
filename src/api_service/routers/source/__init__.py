from fastapi import APIRouter

from .endpoints import (
    complete_upload,
    get_presigned_url,
    get_project_sources,
    add_webpages
)

router = APIRouter(tags=["sources"])
router.add_api_route(
    "/source/file/get_presigned_url", endpoint=get_presigned_url, methods=["POST"]
)
router.add_api_route(
    "/source/file/complete_upload", endpoint=complete_upload, methods=["POST"]
)
router.add_api_route(
    "/project/{project_id}/sources", endpoint=get_project_sources, methods=["GET"]
)
router.add_api_route(
    "/source/webpage/add", endpoint=add_webpages, methods=["POST"]
)
# router.add_api_route("/files/delete", endpoint=delete_file, methods=["POST"])
