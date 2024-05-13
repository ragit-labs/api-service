from typing import List

from fastapi import Request
from ragit_db.models import ContextFile, File
from sqlalchemy import select

from ....database import db
from .types import TFile


async def get_context_files(request: Request, context_id: str) -> List[TFile]:
    async with db.session() as session:
        file_query = (
            select(File).join(ContextFile).where(ContextFile.context_id == context_id)
        )
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
                extra_metadata=file.extra_metadata,
            )
            for file in files
        ]
