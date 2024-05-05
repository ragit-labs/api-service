from fastapi import HTTPException, Request
from ragit_db.models import Context
from sqlalchemy import select

from api_service.clients import qdrant
from api_service.database import db


async def get_documents(
    request: Request, context_id: str, limit: int = 10, offset: int = 0
):
    async with db.session() as session:
        context_query = select(Context).where(Context.id == context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")
        docs = qdrant.scroll(
            collection_name=context_id, limit=limit, offset=offset, with_payload=True
        )
        return docs
