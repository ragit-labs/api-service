from datetime import datetime

from ragit_db.enums import DocumentEmbeddingDistanceMetric, EmbeddingStatus
from ragit_db.models import Context, ContextFile, File
from fastapi import APIRouter, HTTPException, Request
from qdrant_client.models import VectorParams
from sqlalchemy import select

from api_service.clients import qdrant, s3_client
from api_service.database import db
from api_service.utils import partition_and_insert

from .types import AddFileRequest, CreateContextRequest
from .utils import get_context_by_readable_id, get_project_contexts

router = APIRouter(tags=["context"])


@router.post("/context/create")
async def create_context(request: Request, data: CreateContextRequest):

    if not data.name:
        raise HTTPException(status_code=400, detail="name is not in the request.")
    if not data.project_id:
        raise HTTPException(status_code=400, detail="project_id is not in the request.")
    if not data.owner_id:
        raise HTTPException(status_code=400, detail="owner_id is not in the request.")

    async with db.session() as session:
        get_context_query = select(Context).where(
            Context.project_id == data.project_id, Context.name == data.name
        )
        get_context_result = (
            await session.execute(get_context_query)
        ).scalar_one_or_none()
        if get_context_result is not None:
            raise HTTPException(
                status_code=409,
                detail=f"Context by the name {data.name} already exists in this project.",
            )

        last_context_query = (
            select(Context)
            .where(Context.project_id == data.project_id)
            .order_by(Context.id.desc())
            .limit(1)
        )
        last_context_result = (
            await session.execute(last_context_query)
        ).scalar_one_or_none()
        readable_id = 1
        if last_context_result is not None:
            readable_id = last_context_result.readable_id + 1

        try:
            new_context = Context(
                name=data.name,
                description=data.description or "",
                readable_id=readable_id,
                project_id=data.project_id,
                owner_id=data.owner_id,
                search_mode=data.search_mode,
                retrieval_length=data.retrieval_length,
                docs_to_retrieve=data.docs_to_retrieve,
                max_doc_length=data.max_doc_length,
                doc_overlap_length=data.doc_overlap_length,
                embedding_model=data.embedding_model,
                embedding_dimension=data.embedding_dimension,
                distance_metric=data.distance_metric,
                extra_metadata=data.extra_metadata or {},
                created_at=datetime.utcnow(),
                last_refreshed_at=datetime.utcnow(),
            )
            session.add(new_context)
            await session.flush()
            await session.refresh(new_context)
            context_id = new_context.id

            distance_metric = "Cosine"
            if data.distance_metric == DocumentEmbeddingDistanceMetric.COSINE:
                distance_metric = "Cosine"
            elif data.distance_metric == DocumentEmbeddingDistanceMetric.DOT:
                distance_metric = "Dot"
            elif data.distance_metric == DocumentEmbeddingDistanceMetric.EUCLIDEAN:
                distance_metric = "Euclidean"

            vc = VectorParams(
                size=data.embedding_dimension, distance=distance_metric, on_disk=True
            )

            if qdrant.create_collection(context_id, vectors_config=vc):
                await session.commit()
                return {"id": str(context_id)}
            else:
                await session.rollback()
                raise HTTPException(status_code=500, detail="Could not create context.")
        except Exception as ex:
            raise HTTPException(
                status_code=500, detail=f"Could not create context. Error: {str(ex)}"
            )


@router.get("/context/get/{project_id}/{readable_id}")
async def get_context(request: Request, project_id: str, readable_id: int):
    return await get_context_by_readable_id(project_id, readable_id)


@router.get("/context/get/{project_id}")
async def get_all_contexts(request: Request, project_id: str):
    return await get_project_contexts(project_id)


@router.post("/context/add_file")
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

        try:
            new_context_file = ContextFile(
                context_id=data.context_id,
                file_id=data.file_id,
                linked_at=datetime.utcnow(),
                status=EmbeddingStatus.PENDING,
            )
            session.add(new_context_file)
            await session.flush()
            await session.refresh(new_context_file)
            partition_and_insert.delay(
                data.context_id, get_file_result.id, get_file_result.s3_key, 40
            )
            await session.commit()
            return {"status": True}
        except Exception as ex:
            raise HTTPException(
                status_code=500,
                detail=f"Could not add file to context. Error: {str(ex)}",
            )
