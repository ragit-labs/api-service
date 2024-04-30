from api_service.database import db
from sqlalchemy import select
from db.models import Context

async def get_project_contexts(project_id: str):
    async with db.session() as session:
        context_query = select(Context).where(Context.project_id == project_id)
        contexts = (await session.execute(context_query)).scalars().all()
        return contexts


async def get_context_by_readable_id(project_id: str, readable_id: int):
    async with db.session() as session:
        context_query = select(Context).where(Context.project_id == project_id, Context.readable_id == readable_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        return context
