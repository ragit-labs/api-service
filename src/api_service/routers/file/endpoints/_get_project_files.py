from typing import List

from fastapi import Request
from ragit_db.models import File
from sqlalchemy import select

from ....database import db
from .types import TFile


async def get_project_files(request: Request, project_id: str) -> List[TFile]:
    async with db.session() as session:
        file_query = select(File).where(File.project_id == project_id)
        files = (await session.execute(file_query)).scalars().all()
        return [
            TFile(
                id=file.id,
                name=file.name,
                status=file.status,
                description=file.description,
                project_id=file.project_id,
                owner_id=file.owner_id,
                created_at=str(file.created_at),
                file_size=file.file_size,
                file_type=file.file_type,
                extra_metadata=file.extra_metadata or {},
            )
            for file in files
        ]
