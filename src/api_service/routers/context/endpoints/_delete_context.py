from fastapi import HTTPException, Request
from ragit_db.models import Context, ContextFile
from sqlalchemy import select

from ....clients import qdrant
from ....database import db


async def delete_context(request: Request, context_id: str):
    async with db.session() as session:
        context_query = select(Context).where(Context.id == context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")
        context_files = (
            await session.execute(
                select(ContextFile).where(ContextFile.context_id == context_id)
            )
        ).all()
        for context_file in context_files:
            session.delete(context_file)
        await session.flush()
        await session.delete(context)
        qdrant.delete_collection(context_id)
        await session.commit()
        return {"status": True}
