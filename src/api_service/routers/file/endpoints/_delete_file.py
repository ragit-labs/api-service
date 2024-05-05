from fastapi import HTTPException, Request
from ragit_db.models import File
from sqlalchemy import select

from api_service.clients import s3_client
from api_service.database import db

from .types import DeleteFileRequest


async def delete_file(request: Request, data: DeleteFileRequest):
    async with db.session() as session:
        file_query = select(File).where(File.id == data.file_id)
        file = (await session.execute(file_query)).scalar_one_or_none()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        session.delete(file)
        session.flush()
        s3_client.delete_file(file.s3_key)
        await session.commit()
        return {"status": True}
