import asyncio
import io
from time import time
from uuid import uuid4

from celery.app import Celery
from fastapi import HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pdfminer.high_level import extract_text
from qdrant_client.models import PointStruct
from ragit_db.enums import EmbeddingStatus
from ragit_db.models import ContextFile
from sqlalchemy import select

from api_service.clients import qdrant, s3_client
from api_service.database import db
from api_service.settings import settings
from api_service.utils import create_text_embeddings

broker_uri = settings.REDIS_BROKER

celery_app = Celery(__name__, broker=broker_uri, backend=broker_uri)


def batch(iterable, n=1):
    l = len(iterable)  # noqa
    for ndx in range(0, l, n):
        yield iterable[ndx: min(ndx + n, l)]  # noqa


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
def partition_and_insert(
    context_id: str,
    file_id: str,
    file_key: str,
    meta: dict,
    embedding_dimension: int,
    chunksize: int,
    overlap: int,
    batch_size: int,
):
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
    # partitions = partition_pdf(file=file_stream)
    pdf_text = extract_text(file_stream)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunksize, chunk_overlap=overlap
    )
    partitions = splitter.split_text(pdf_text)
    e2 = time()
    print(f"Partitioned file in {e2-s2} seconds")

    for partition_batch in batch(partitions, batch_size):
        documents = partition_batch
        s3 = time()
        embeddings = create_text_embeddings(documents, max_length=embedding_dimension)
        e3 = time()
        print(f"Embeddings created in {e3-s3} seconds")

        s4 = time()
        qdrant.upsert(
            collection_name=context_id,
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=e.tolist(),
                    payload={
                        "document": d,
                        **meta,
                    },
                )
                for e, d in zip(embeddings, documents)
            ],
            wait=True,
        )
        e4 = time()
        print(f"Embeddings inserted in {e4-s4} seconds")

    asyncio.run(update_status(context_id, file_id, EmbeddingStatus.FINISHED))
