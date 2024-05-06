import random
import string
from datetime import datetime

from fastapi import HTTPException, Request
from ragit_db.enums import FileStatus
from ragit_db.models import File, Project
from sqlalchemy import select

from ....clients import s3_client
from ....database import db
from ....utils.misc import sanitize_string
from .types import GetPresignedUrlRequest


async def get_presigned_url(request: Request, data: GetPresignedUrlRequest):
    key = data.key
    key_sanitized = sanitize_string(key)
    prefix = "".join(random.choice(string.ascii_letters) for i in range(6))
    key_sanitized = prefix + "_" + key_sanitized
    expiration = data.expiration

    async with db.session() as session:
        project_query = select(Project).where(Project.id == data.project_id)
        project = (await session.execute(project_query)).scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if data.file_size > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size is too large")

        file = File(
            name=key,
            s3_key=key_sanitized,
            status=FileStatus.PENDING,
            description="",
            project_id=data.project_id,
            owner_id=request.state.user_id,
            created_at=datetime.utcnow(),
            file_size=data.file_size,
            file_type=data.file_type,
        )
        session.add(file)
        await session.flush()
        await session.commit()
        await session.refresh(file)
        return {
            "url": s3_client.create_presigned_url(key_sanitized, expiration),
            "file_id": str(file.id),
        }
