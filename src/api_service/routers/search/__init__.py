import io
from uuid import uuid4

from ragit_db.enums import UploadStatus
from ragit_db.models import Context, File
from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select
from unstructured.partition.pdf import partition_pdf

from api_service.clients import qdrant, s3_client
from api_service.database import db

from .types import SearchRequest

router = APIRouter(tags=["search", "context"])


@router.post("/search")
async def search(request: Request, data: SearchRequest):
    async with db.session() as session:
        context_query = select(Context).where(Context.id == data.context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")

        qdrant.search(
            collection_name=str(context.id),
            query=data.query,
            top_k=data.top_k,
        )
