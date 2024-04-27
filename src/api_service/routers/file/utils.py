from sqlalchemy import select
from .types import ProjectFilesRequest, ContextFilesRequest
from db.models import File, FileContext
from api_service.database import db


async def get_project_files(data: ProjectFilesRequest):
    async with db.session() as session:
        file_query = select(File).where(File.project_id == data.project_id)
        files = (await session.execute(file_query)).scalars().all()
        return files


async def get_context_files(data: ContextFilesRequest):
    async with db.session() as session:
        # file_contexts = select(file_context_association).where(file_context_association.c.context_id == data.context_id)
        file_query = select(File).join(FileContext).where(FileContext.context_id == data.context_id)
        files = (await session.execute(file_query)).scalars().all()
        return files