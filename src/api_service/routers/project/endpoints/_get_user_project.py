from fastapi import HTTPException, Request
from ragit_db.models import Project
from sqlalchemy import select

from ....database import db
from .types import TProject


async def get_project_for_user(request: Request) -> TProject:
    async with db.session() as session:
        get_project_query = select(Project).where(Project.owner_id == request.state.user_id)
        get_project_result = (
            await session.execute(get_project_query)
        ).scalar_one_or_none()
        print(get_project_result)
        if get_project_result is None:
            raise HTTPException(
                status_code=404, detail=f"No Project Found."
            )
        return TProject(
            id=str(get_project_result.id),
            name=get_project_result.name,
            description=get_project_result.description,
            owner_id=str(get_project_result.owner_id),
        )
