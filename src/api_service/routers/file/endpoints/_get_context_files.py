from fastapi import Request
from ragit_db.models import ContextFile, File
from sqlalchemy import select

from api_service.database import db


async def get_context_files(request: Request, project_id: str, context_id: str):
    async with db.session() as session:
        file_query = (
            select(File).join(ContextFile).where(ContextFile.context_id == context_id)
        )
        files = (await session.execute(file_query)).scalars().all()
        return files
