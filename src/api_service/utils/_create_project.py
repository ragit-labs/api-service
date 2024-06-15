from fastapi import HTTPException
from ragit_db.models import Project

from ..database import db


async def create_project(project_name: str, owner_id: str) -> str:
    async with db.session() as session:
        try:
            new_project = Project(
                name=project_name,
                description="",
                owner_id=owner_id
            )
            session.add(new_project)
            await session.flush()
            await session.refresh(new_project)
            project_id = new_project.id
            await session.commit()
            return str(project_id)
        except Exception as ex:
            raise HTTPException(
                status_code=500, detail=f"Could not create project. Error: {str(ex)}"
            )
