import asyncio
import io
import json
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
from unstructured.documents.elements import TYPE_TO_TEXT_ELEMENT_MAP
from collections import defaultdict
from uuid import uuid4

broker_uri = settings.REDIS_BROKER

celery_app = Celery(__name__, broker=broker_uri, backend=broker_uri)


def defval():
    return 5


prio = defaultdict(defval)
prio[TYPE_TO_TEXT_ELEMENT_MAP['Title']] = 1
prio[TYPE_TO_TEXT_ELEMENT_MAP['Section-header']] = 2
prio[TYPE_TO_TEXT_ELEMENT_MAP['Headline']] = 3
prio[TYPE_TO_TEXT_ELEMENT_MAP['Subheadline']] = 4
prio[type(None)] = 0


def batch(iterable, n=1):
    l = len(iterable)  # noqa
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]  # noqa


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


async def update_partition_key(context_id: str, file_id: str, s3_key: str):
    async with db.session() as session:
        context_file_query = select(ContextFile).where(
            ContextFile.context_id == context_id, ContextFile.file_id == file_id
        )
        context_file = (await session.execute(context_file_query)).scalar_one_or_none()
        if not context_file:
            raise HTTPException(status_code=404, detail="ContextFile not found")
        context_file.s3_key = s3_key
        await session.commit()


async def get_partitions_key(context_id: str, file_id: str):
    async with db.session() as session:
        context_file_query = select(ContextFile).where(
            ContextFile.context_id == context_id, ContextFile.file_id == file_id
        )
        context_file = (await session.execute(context_file_query)).scalar_one_or_none()
        if not context_file:
            return None
        return context_file.s3_key


def recursive_chunk(text: str, chunksize: int, overlap: int):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunksize, chunk_overlap=overlap
    )
    partitions = splitter.split_text(text)
    return partitions

def pdf_chunk(text: str, chunksize):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunksize, chunk_overlap=0
    )
    partitions = splitter.split_text(text)
    return partitions


async def process(
    context_id: str,
    file_id: str,
    file_key: str,
    meta: dict,
    embedding_dimension: int,
    chunksize: int,
    overlap: int,
    batch_size: int,
):
    partition_key = await get_partitions_key(context_id, file_id)
    partitions = []
    if partition_key is None:
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
        # partitions = agentic_chunk(pdf_text)
        partitions = recursive_chunk(pdf_text)
        # partitions = recursive_chunk(pdf_text, chunksize, overlap)
        new_key = str(uuid4()) + ".json"
        s3_client.save_obj_as_file(json.dumps(partitions), new_key)
        await update_partition_key(context_id, file_id, new_key)
    else:
        try:
            partition_file_data = s3_client.download_file_as_obj(partition_key)
        except:
            raise HTTPException(
                status_code=500, detail=f"Could not download file from S3. {str(ex)}"
            )
        partition_bytes = partition_file_data["Body"].read()
        partition_stream = io.BytesIO(partition_bytes)
        partitions = json.load(partition_stream)

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

    await update_status(context_id, file_id, EmbeddingStatus.FINISHED)


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
    asyncio.run(
        process(
            context_id,
            file_id,
            file_key,
            meta,
            embedding_dimension,
            chunksize,
            overlap,
            batch_size,
        )
    )
