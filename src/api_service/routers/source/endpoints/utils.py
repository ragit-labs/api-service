from ragit_db.models import Source
from sqlalchemy import select

from ....database import db


async def get_project_sources(project_id: str):
    async with db.session() as session:
        source_query = select(Source).where(Source.project_id == project_id)
        sources = (await session.execute(source_query)).scalars().all()
        return sources
