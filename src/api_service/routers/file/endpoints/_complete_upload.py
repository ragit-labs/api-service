from fastapi import HTTPException, Request
from ragit_db.enums import FileStatus
from ragit_db.models import File
from sqlalchemy import select

from ....database import db
from .types import MarkSuccess, MarkUploadStatusRequest


async def complete_upload(
    request: Request, data: MarkUploadStatusRequest
) -> MarkSuccess:
    async with db.session() as session:
        file_query = select(File).where(File.id == data.file_id)
        file = (await session.execute(file_query)).scalar_one_or_none()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        file.status = FileStatus.FINISHED
        await session.commit()
        return MarkSuccess(success=True)
