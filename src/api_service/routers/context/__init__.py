from fastapi import APIRouter

from .endpoints import (
    add_file,
    create_context,
    delete_context,
    get_context_by_readable_id,
    get_documents,
    get_project_contexts,
    remove_file,
    search_documents,
)

router = APIRouter(tags=["context"])
router.add_api_route("/context/create", endpoint=create_context, methods=["POST"])
router.add_api_route(
    "/project/{project_id}/context/{readable_id}",
    endpoint=get_context_by_readable_id,
    methods=["GET"],
)
router.add_api_route(
    "/project/{project_id}/contexts", endpoint=get_project_contexts, methods=["GET"]
)
router.add_api_route(
    "/context/{context_id}/add_file", endpoint=add_file, methods=["POST"]
)
router.add_api_route(
    "/context/{context_id}/remove_file", endpoint=remove_file, methods=["POST"]
)
router.add_api_route(
    "/context/{context_id}/documents", endpoint=get_documents, methods=["GET"]
)
router.add_api_route(
    "/context/{context_id}", endpoint=delete_context, methods=["DELETE"]
)
# router.add_api_route("/context/search", endpoint=search_documents, methods=["POST"])
