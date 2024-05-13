from typing import List

from fastapi import Request
from ragit_db.models import Project
from sqlalchemy import select

from ....database import db
from .types import TProject


async def get_projects(
    request: Request, limit: int = 10, offset: int = 0
) -> List[TProject]:
    owner_id = request.state.user_id
    async with db.session() as session:
        get_project_query = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .limit(limit)
            .offset(offset)
        )
        get_project_result = (await session.execute(get_project_query)).scalars().all()
        return [
            TProject(
                id=str(project.id),
                readable_id=project.readable_id,
                name=project.name,
                description=project.description,
                owner_id=str(project.owner_id),
            )
            for project in get_project_result
        ]
