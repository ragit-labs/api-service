import io
from uuid import uuid4

from ragit_db.enums import FileStatus
from ragit_db.models import Context, File
from fastapi import APIRouter, HTTPException, Request
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sqlalchemy import select
from unstructured.partition.pdf import partition_pdf

from api_service.clients import qdrant, s3_client
from api_service.clients.s3 import S3Client
from api_service.database import db

from ...utils import batch
from ...utils.decorators import fire_and_forget
from .types import CreateEmbeddingsRequest
from .utils import create_text_embeddings

router = APIRouter(tags=["embeddings", "vector-store"])


@fire_and_forget
def partition_and_insert(
    file_stream: io.BytesIO, qc: QdrantClient, batch_size: int = 100
):
    partitions = partition_pdf(file=file_stream)
    for partition_batch in batch(partitions, batch_size):
        documents = []
        metadata = []
        for partition in partition_batch:
            data = partition.to_dict()
            documents.append(data["text"])
            metadata.append(data["metadata"])
        embeddings = create_text_embeddings(documents, max_length=768)
        qc.upsert(
            collection_name="test",
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=data[0].tolist(),
                    payload={
                        "document": data[1],
                        **data[2],
                    },
                )
                for data in zip(embeddings, documents, metadata)
            ],
        )


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
        file_bytes = file_data["Body"].read()
        file_stream = io.BytesIO(file_bytes)
        partition_and_insert(file_stream, qdrant)
