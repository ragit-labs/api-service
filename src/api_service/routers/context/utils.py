from .types import ProjectsContextRequest, ContextRequest
from fastapi import HTTPException
from api_service.database import db
from sqlalchemy import select
from db.models import Context
from typing import List
from fastembed.embedding import TextEmbedding
import numpy as np
from api_service.types.embedding_model import EmbeddingModel
from api_service.clients import celery_app
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from uuid import uuid4
from ...utils import batch
from unstructured.partition.pdf import partition_pdf
import io

async def get_project_contexts(project_id: str):
    async with db.session() as session:
        context_query = select(Context).where(Context.project_id == project_id)
        contexts = (await session.execute(context_query)).scalars().all()
        return contexts


async def get_context_by_readable_id(project_id: str, readable_id: int):
    async with db.session() as session:
        context_query = select(Context).where(Context.project_id == project_id, Context.readable_id == readable_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        return context


async def create_text_embeddings(documents: List[str], model_name: str = EmbeddingModel.BAAI_BGE_BASE_EN, max_length: int = 512):
    embedding_model = TextEmbedding(model_name=EmbeddingModel.BAAI_BGE_BASE_EN, max_length=512)
    embeddings: List[np.ndarray] = embedding_model.embed(documents)
    return embeddings


@celery_app.task
def partition_and_insert(file_stream: io.BytesIO, qc: QdrantClient, batch_size: int = 100):
    partitions = partition_pdf(file=file_stream)
    for partition_batch in batch(partitions, batch_size):
        documents = []
        metadata = []
        for partition in partition_batch:
            data = partition.to_dict()
            documents.append(data['text'])
            metadata.append(data['metadata'])
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
                    }
                ) for data in zip(embeddings, documents, metadata)
            ]
        )
        break