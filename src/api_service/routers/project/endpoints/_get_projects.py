from fastapi import Request
from ragit_db.models import Project
from sqlalchemy import select

from api_service.database import db


async def get_projects(request: Request, limit: int = 10, offset: int = 0):
    owner_id = request.state.user_id
    async with db.session() as session:
        get_project_query = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .limit(limit)
            .offset(offset)
        )
        get_project_result = (await session.execute(get_project_query)).scalars().all()
        return get_project_result
