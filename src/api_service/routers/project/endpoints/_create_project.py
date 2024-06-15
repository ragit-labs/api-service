from fastapi import HTTPException, Request
from ragit_db.models import Project
from sqlalchemy import select

from ....database import db
from .types import CreateProjectRequest
from ....utils.misc import sanitize_string


async def create_project(request: Request, data: CreateProjectRequest):

    if not data.name:
        raise HTTPException(status_code=400, detail="name is not in the request.")
    
    owner_id = request.state.user_id

    async with db.session() as session:
        get_project_query = select(Project).where(
            Project.owner_id == owner_id, Project.name == data.name
        )
        get_project_result = (
            await session.execute(get_project_query)
        ).scalar_one_or_none()
        if get_project_result is not None:
            raise HTTPException(
                status_code=409,
                detail=f"Project by the name {data.name} already exists in this project.",
            )

        try:
            new_project = Project(
                name=data.name,
                description=data.description or "",
                owner_id=owner_id,
                readable_id=sanitize_string(data.name).lower(),
            )
            session.add(new_project)
            await session.flush()
            await session.refresh(new_project)
            project_id = new_project.id
            await session.commit()
            return {"id": str(project_id)}
        except Exception as ex:
            raise HTTPException(
                status_code=500, detail=f"Could not create project. Error: {str(ex)}"
            )
