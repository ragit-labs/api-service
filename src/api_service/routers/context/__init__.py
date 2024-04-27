from fastapi import APIRouter, Request, HTTPException
from api_service.clients import s3_client, qdrant
from db.models import Context, File, FileContext
from datetime import datetime
from api_service.database import db
from db.enums import EmbeddingStatus
from .types import CreateContextRequest, GetContextsRequest, GetContextsRequest, AddFileRequest, ProjectsContextRequest, ContextRequest
from sqlalchemy import select
from api_service.types.embedding_model import EmbeddingModel

from .utils import get_context, get_project_contexts

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
        get_context_query = select(Context).where(Context.project_id == data.project_id, Context.name == data.name)
        get_context_result = (await session.execute(get_context_query)).scalar_one_or_none()
        if get_context_result is not None:
            raise HTTPException(status_code=409, detail=f"Context by the name {data.name} already exists in this project.")
        
        try:
            new_context = Context(
                name=data.name,
                description=data.description or "",
                project_id=data.project_id,
                owner_id=data.owner_id,
                metadata=data.extra_metadata or {},
                created_at=datetime.utcnow(),
            )
            session.add(new_context)
            await session.flush()
            await session.refresh(new_context)
            context_id = new_context.id
            if qdrant.create_collection(context_id, vectors_config={
                "distance": "Cosine",
                "size": "768",
                "on_disk": True
            }):
                await session.commit()
                return {"id": str(context_id)}
            else:
                await session.rollback()
                raise HTTPException(status_code=500, detail="Could not create context.")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Could not create context. Error: {str(ex)}")


@router.post("/context/get")
async def get_all_contexts(request: Request, data: GetContextsRequest):
    if type(data.where) is ProjectsContextRequest:
        return await get_project_contexts(data.where)
    
    if type(data.where) is ContextRequest:
        return await get_context(data.where)


@router.post("/context/add_file")
async def add_file(request: Request, data: AddFileRequest):
    if not data.context_id:
        raise HTTPException(status_code=400, detail="context_id is not in the request.")
    if not data.file_id:
        raise HTTPException(status_code=400, detail="file_id is not in the request.")

    async with db.session() as session:
        get_context_query = select(Context).where(Context.id == data.context_id)
        get_context_result = (await session.execute(get_context_query)).scalar_one_or_none()
        if get_context_result is None:
            raise HTTPException(status_code=404, detail="Context not found.")
        
        get_file_query = select(File).where(File.id == data.file_id)
        get_file_result = (await session.execute(get_file_query)).scalar_one_or_none()
        if get_file_result is None:
            raise HTTPException(status_code=404, detail="File not found.")
        
        get_file_context_query = select(FileContext).where(FileContext.context_id == data.context_id, FileContext.file_id == data.file_id)
        get_file_context_result = (await session.execute(get_file_context_query)).scalar_one_or_none()
        if get_file_context_result is not None:
            raise HTTPException(status_code=409, detail="File is already associated with the context.")
        
        try:
            fc = FileContext(context_id=data.context_id, file_id=data.file_id, status=EmbeddingStatus.PENDING)
            session.add(fc)
            await session.commit()
            return {"status": True}
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Could not add file to context. Error: {str(ex)}")
