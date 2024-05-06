from fastapi import HTTPException, Request
from qdrant_client.models import FieldCondition, Filter, FilterSelector, MatchValue
from ragit_db.models import Context, ContextFile
from sqlalchemy import select

from ....clients import qdrant
from ....database import db
from .types import DeleteFileRequest


async def remove_file(request: Request, context_id: str, data: DeleteFileRequest):
    async with db.session() as session:
        context_query = select(Context).where(Context.id == context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")
        context_file_query = select(ContextFile).where(
            ContextFile.context_id == context_id,
            ContextFile.file_id == data.file_id,
        )
        context_file = (await session.execute(context_file_query)).scalar_one_or_none()
        if not context_file:
            raise HTTPException(
                status_code=404, detail="This file is not linked to this context."
            )
        await session.delete(context_file)
        qdrant.delete(
            collection_name=context_id,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="file_id", match=MatchValue(value=str(data.file_id))
                        )
                    ]
                )
            ),
            wait=True,
        )
        await session.commit()
        return {"status": True}
