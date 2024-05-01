import random
import string
from datetime import datetime

from ragit_db.enums import FileStatus
from ragit_db.models import File, Project
from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select

from api_service.clients import s3_client
from api_service.database import db

from ...utils.misc import sanitize_string
from .types import DeleteFileRequest, GetPresignedUrlRequest, MarkUploadStatusRequest
from .utils import get_context_files, get_project_files

router = APIRouter(tags=["s3", "data-store"])


@router.post("/files/get_presigned_url")
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
        
        if(data.file_size > 5 * 1024 * 1024):
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


@router.post("/files/complete_upload")
async def mark_upload_success(request: Request, data: MarkUploadStatusRequest):
    async with db.session() as session:
        file_query = select(File).where(File.id == data.file_id)
        file = (await session.execute(file_query)).scalar_one_or_none()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        file.status = FileStatus.FINISHED
        await session.commit()
        return {"status": True}


@router.get("/files/get/{project_id}")
async def get_project_files_(request: Request, project_id: str):
    return await get_project_files(project_id)


@router.get("/files/get/{project_id}/{context_id}")
async def get_context_files_(request: Request, project_id: str, context_id: str):
    return await get_context_files(project_id, context_id)


@router.post("/files/delete")
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
