from fastapi import Request
from ragit_db.models import Context
from sqlalchemy import select

from api_service.database import db


async def get_project_contexts(request: Request, project_id: str):
    async with db.session() as session:
        context_query = select(Context).where(Context.project_id == project_id)
        contexts = (await session.execute(context_query)).scalars().all()
        return contexts


async def get_context_by_readable_id(
    request: Request, project_id: str, readable_id: int
):
    async with db.session() as session:
        context_query = select(Context).where(
            Context.project_id == project_id, Context.readable_id == readable_id
        )
        context = (await session.execute(context_query)).scalar_one_or_none()
        return context
