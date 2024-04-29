from fastapi import APIRouter, Request, HTTPException
from api_service.clients import s3_client
import random
import string
from db.models import Project, File
from db.enums import FileStatus
from api_service.database import db
from sqlalchemy import select
from .types import GetPresignedUrlRequest, MarkUploadStatusRequest, GetFilesRequest, ProjectFilesRequest, ContextFilesRequest, DeleteFileRequest
from datetime import datetime
from .utils import get_project_files, get_context_files
from ...utils.misc import sanitize_string

router = APIRouter(tags=["s3", "data-store"])

@router.post("/files/get_presigned_url")
async def get_presigned_url(request: Request, data: GetPresignedUrlRequest):
    key = data.key
    key_sanitized = sanitize_string(key)
    prefix = ''.join(random.choice(string.ascii_letters) for i in range(6))
    key_sanitized = prefix + "_" + key_sanitized
    expiration = data.expiration

    async with db.session() as session:
        project_query = select(Project).where(Project.id == data.project_id)
        project = (await session.execute(project_query)).scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        url = s3_client.create_presigned_url(key_sanitized, expiration)

        file = File(
            project_id=data.project_id,
            name=key,
            s3_key=key_sanitized,
            status=FileStatus.PENDING,
            description="",
            created_at=datetime.utcnow(),
        )
        session.add(file)
        await session.flush()
        await session.commit()
        await session.refresh(file)
        return {"url": s3_client.create_presigned_url(key_sanitized, expiration), "file_id": str(file.id)}



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


@router.post("/files/get")
async def mark_upload_success(request: Request, data: GetFilesRequest):
    if type(data.where) is ProjectFilesRequest:
        return await get_project_files(data.where)
    if type(data.where) is ContextFilesRequest:
        return await get_context_files(data.where)


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
