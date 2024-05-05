from fastapi import HTTPException, Request
from ragit_db.models import Project
from sqlalchemy import select

from api_service.database import db


async def get_project_by_uuid(request: Request, project_id: str):
    async with db.session() as session:
        get_project_query = select(Project).where(Project.id == project_id)
        get_project_result = (
            await session.execute(get_project_query)
        ).scalar_one_or_none()
        if get_project_result is None:
            raise HTTPException(
                status_code=404, detail=f"Project with id {project_id} not found."
            )
        return get_project_result
