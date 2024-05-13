from typing import List

from fastapi import HTTPException, Request
from ragit_db.models import Context
from sqlalchemy import select

from ....clients import qdrant
from ....database import db
from .types import TDocument


async def get_documents(
    request: Request,
    context_id: str,
    offset: str = None,
    limit: int = 10,
) -> List[TDocument]:
    async with db.session() as session:
        context_query = select(Context).where(Context.id == context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")
        docs = qdrant.scroll(
            collection_name=context_id, limit=limit, offset=offset, with_payload=True
        )
        return [
            TDocument(
                id=doc.id,
                context_id=context.id,
                file_id=doc.payload["file_id"],
                document=doc.payload["document"],
                file_name=doc.payload["file_name"],
                file_type=doc.payload["file_type"],
            )
            for doc in docs[0]
        ]
