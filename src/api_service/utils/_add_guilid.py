from fastapi import HTTPException
from ragit_db.models import Discord

from ..database import db


async def add_guild_to_project(project_id: str, guild_id: str) -> str:
    async with db.session() as session:
        try:
            new_guild_project = Discord(
                project_id=project_id,
                guild_id=guild_id
            )
            session.add(new_guild_project)
            await session.flush()
            await session.refresh(new_guild_project)
            project_id = new_guild_project.project_id
            guild_id = new_guild_project.guild_id
            await session.commit()
            return (str(project_id), str(guild_id))
        except Exception as ex:
            raise HTTPException(
                status_code=500, detail=f"Could not add guild to project. Error: {str(ex)}"
            )
