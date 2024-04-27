from .types import ProjectsContextRequest, ContextRequest
from fastapi import HTTPException
from api_service.database import db
from sqlalchemy import select
from db.models import Context

async def get_project_contexts(data: ProjectsContextRequest):
    if not data.project_id:
        raise HTTPException(status_code=400, detail="project_id is not in the request.")
    async with db.session() as session:
        context_query = select(Context).where(Context.project_id == data.project_id)
        contexts = (await session.execute(context_query)).scalars().all()
        return contexts


async def get_context(data: ContextRequest):
    if not data.context_id:
        raise HTTPException(status_code=400, detail="context_id is not in the request.")
    async with db.session() as session:
        context_query = select(Context).where(Context.id == data.context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        return context