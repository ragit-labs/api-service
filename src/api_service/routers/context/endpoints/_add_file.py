from datetime import datetime

from fastapi import HTTPException, Request
from ragit_db.enums import EmbeddingStatus
from ragit_db.models import Context, ContextFile, File
from sqlalchemy import select

from api_service.database import db
from embeddings_service import partition_and_insert

from .types import AddFileRequest


async def add_file(request: Request, data: AddFileRequest):
    if not data.context_id:
        raise HTTPException(status_code=400, detail="context_id is not in the request.")
    if not data.file_id:
        raise HTTPException(status_code=400, detail="file_id is not in the request.")

    async with db.session() as session:
        get_context_query = select(Context).where(Context.id == data.context_id)
        get_context_result = (
            await session.execute(get_context_query)
        ).scalar_one_or_none()
        if get_context_result is None:
            raise HTTPException(status_code=404, detail="Context not found.")

        get_file_query = select(File).where(File.id == data.file_id)
        get_file_result = (await session.execute(get_file_query)).scalar_one_or_none()
        if get_file_result is None:
            raise HTTPException(status_code=404, detail="File not found.")

        get_file_context_query = select(ContextFile).where(
            ContextFile.context_id == data.context_id,
            ContextFile.file_id == data.file_id,
        )
        get_file_context_result = (
            await session.execute(get_file_context_query)
        ).scalar_one_or_none()
        if get_file_context_result is not None:
            raise HTTPException(
                status_code=409, detail="File is already associated with the context."
            )

        new_context_file = ContextFile(
            context_id=data.context_id,
            file_id=data.file_id,
            linked_at=datetime.utcnow(),
            status=EmbeddingStatus.PENDING,
        )
        session.add(new_context_file)
        await session.flush()
        await session.refresh(new_context_file)
        meta = {
            "file_name": get_file_result.name,
            "file_id": get_file_result.id,
            "file_size": get_file_result.file_size,
            "file_type": get_file_result.file_type,
        }
        partition_and_insert.delay(
            data.context_id,
            data.file_id,
            get_file_result.s3_key,
            meta,
            get_context_result.embedding_dimension,
            get_context_result.max_doc_length,
            get_context_result.doc_overlap_length,
            60,
        )
        await session.commit()
        return {"status": True}
