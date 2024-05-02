import asyncio
import io
from typing import List
from uuid import uuid4

import numpy as np
from celery.app import Celery
from ragit_db.enums import EmbeddingStatus
from ragit_db.models import ContextFile
from fastapi import HTTPException
from qdrant_client.models import PointStruct
from sqlalchemy import select
from api_service.settings import settings
from unstructured.partition.pdf import partition_pdf

from api_service.clients import qdrant, s3_client
from api_service.database import db
from api_service.types.embedding_model import EmbeddingModel
from fastembed.embedding import TextEmbedding
from time import time

broker_uri = settings.REDIS_BROKER

celery_app = Celery(__name__, broker=broker_uri, backend=broker_uri)


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


def create_text_embeddings(
    documents: List[str],
    max_length: int,
    model_name: str = EmbeddingModel.BAAI_BGE_BASE_EN,
):
    embedding_model = TextEmbedding(
        model_name=model_name, max_length=max_length, cache_dir="cachee"
    )
    embeddings: List[np.ndarray] = embedding_model.embed(documents)
    return embeddings


async def update_status(context_id: str, file_id: str, status: EmbeddingStatus):
    async with db.session() as session:
        context_file_query = select(ContextFile).where(
            ContextFile.context_id == context_id, ContextFile.file_id == file_id
        )
        context_file = (await session.execute(context_file_query)).scalar_one_or_none()
        if not context_file:
            raise HTTPException(status_code=404, detail="ContextFile not found")
        context_file.status = status
        await session.commit()


@celery_app.task
def partition_and_insert(context_id: str, file_id: str, file_key: str, meta: dict, batch_size: int):
    try:
        file_data = s3_client.download_file_as_obj(file_key)
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Could not download file from S3. {str(ex)}"
        )
    s1 = time()
    file_bytes = file_data["Body"].read()
    file_stream = io.BytesIO(file_bytes)
    e1 = time()
    print(f"Downloaded file in {e1-s1} seconds")

    s2 = time()
    partitions = partition_pdf(file=file_stream)
    e2 = time()
    print(f"Partitioned file in {e2-s2} seconds")


    for partition_batch in batch(partitions, batch_size):
        documents = []
        metadata = []
        for partition in partition_batch:
            partition_data = partition.to_dict()
            documents.append(partition_data["text"])
            metadata.append(
                {
                    **meta,
                    "extra_metadata": partition_data["metadata"],
                }
            )
        s3 = time()
        embeddings = create_text_embeddings(documents, max_length=768)
        e3 = time()
        print(f"Embeddings created in {e3-s3} seconds")

        s4 = time()
        qdrant.upsert(
            collection_name=context_id,
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
            wait=True,
        )
        e4 = time()
        print(f"Embeddings inserted in {e4-s4} seconds")

    asyncio.run(update_status(context_id, file_id, EmbeddingStatus.FINISHED))
