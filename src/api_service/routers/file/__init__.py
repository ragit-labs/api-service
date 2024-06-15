from fastapi import APIRouter

from .endpoints import (
    complete_upload,
    delete_file,
    get_context_files,
    get_presigned_url,
    get_project_files,
)

router = APIRouter(tags=["files"])
router.add_api_route(
    "/files/get_presigned_url", endpoint=get_presigned_url, methods=["POST"]
)
router.add_api_route(
    "/files/complete_upload", endpoint=complete_upload, methods=["POST"]
)
router.add_api_route(
    "/project/{project_id}/files", endpoint=get_project_files, methods=["GET"]
)
router.add_api_route("/files/delete", endpoint=delete_file, methods=["POST"])
