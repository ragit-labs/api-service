from fastapi import HTTPException, Request
from ragit_db.models import Project
from sqlalchemy import select
from .types import TProject

from ....database import db


async def get_project(request: Request, project_id: str) -> TProject:
    async with db.session() as session:
        get_project_query = select(Project).where(
            Project.owner_id == request.state.user_id,
            Project.readable_id == project_id.lower(),
        )
        get_project_result = (
            await session.execute(get_project_query)
        ).scalar_one_or_none()
        if get_project_result is None:
            raise HTTPException(
                status_code=404, detail=f"Project with id {project_id} not found."
            )
        return TProject(
            id=str(get_project_result.id),
            readable_id=get_project_result.readable_id,
            name=get_project_result.name,
            description=get_project_result.description,
            owner_id=str(get_project_result.owner_id),
        )
