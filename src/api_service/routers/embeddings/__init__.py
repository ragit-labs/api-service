from fastapi import APIRouter, Request, HTTPException
from api_service.clients import s3_client
from api_service.database import db
from sqlalchemy import select
from .types import CreateEmbeddingsRequest
from api_service.database import db
from db.models import File, Context
from db.enums import FileStatus
import io
from unstructured.partition.pdf import partition_pdf
from api_service.clients import qdrant
from uuid import uuid4
from .utils import create_text_embeddings

router = APIRouter(tags=["embeddings", "vector-store"])

@router.post("/embeddings/create")
async def create_embeddings(request: Request, data: CreateEmbeddingsRequest):
    async with db.session() as session:
        context_query = select(Context).where(Context.id == data.context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")
        
        file_query = select(File).where(File.id == data.file_id)
        file = (await session.execute(file_query)).scalar_one_or_none()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        if file.status != FileStatus.FINISHED:
            raise HTTPException(status_code=400, detail="File is not uploaded yet.")
        
        file_data = s3_client.download_file_as_obj(file.s3_key)
        file_bytes = file_data['Body'].read()
        file_stream = io.BytesIO(file_bytes)
        partitions = partition_pdf(file=file_stream)
        
        documents = []
        metadata = []
        
        for partition in partitions:
            data = partition.to_dict()
            documents.append(data['text'])
            metadata.append(data['metadata'])
        embeddings = await create_text_embeddings(documents, max_length=384)
        for embedding in embeddings:
            print(embedding)
        # qdrant.add(
        #     collection_name=str(context.id),
        #     documents=documents,
        #     metadata=metadata,
        # )
