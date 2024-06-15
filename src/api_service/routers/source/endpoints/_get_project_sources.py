from typing import List

from fastapi import Request
from ragit_db.models import Source
from sqlalchemy import select

from ....database import db
from .types import TSource


async def get_project_sources(request: Request, project_id: str) -> List[TSource]:
    async with db.session() as session:
        file_query = select(Source).where(Source.project_id == project_id)
        files = (await session.execute(file_query)).scalars().all()
        return [
            TSource(
                id=str(file.id),
                project_id=str(file.project_id),
                name=file.name,
                status=file.status,
                source_type=str(file.source_type),
                created_at=str(file.created_at),
                url=file.url,
                extra_metadata=file.extra_metadata or {},
                user_id=str(file.user_id),
            )
            for file in files
        ]
