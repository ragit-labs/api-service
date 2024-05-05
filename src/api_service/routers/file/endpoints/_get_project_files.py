from fastapi import Request
from ragit_db.models import File
from sqlalchemy import select

from api_service.database import db


async def get_project_files(request: Request, project_id: str):
    async with db.session() as session:
        file_query = select(File).where(File.project_id == project_id)
        files = (await session.execute(file_query)).scalars().all()
        return files
