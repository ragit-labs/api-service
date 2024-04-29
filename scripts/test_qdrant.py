import asyncio
import io
from uuid import uuid4

from celery.app import Celery
from qdrant_client.models import PointStruct
from unstructured.partition.pdf import partition_pdf

from api_service.clients import qdrant, s3_client
from api_service.routers.embeddings.utils import create_text_embeddings

broker_uri = "redis://localhost:6379"
celery_app = Celery(__name__, broker=broker_uri, backend=broker_uri)


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


@celery_app.task
def process_file():
    asyncio.run(partition_and_insert())


async def partition_and_insert():
    fk = "PxzVao_Jessica-Livingston---Founders-at-Work_-Stories-of-Startups-Early-Days-Apress-2009.pdf"
    file_data = s3_client.download_file_as_obj(fk)
    file_bytes = file_data["Body"].read()
    file_stream = io.BytesIO(file_bytes)
    partitions = partition_pdf(file=file_stream)
    total = len(partitions)
    cnt = 0
    for partition_batch in batch(partitions, 100):
        documents = []
        metadata = []
        for partition in partition_batch:
            data = partition.to_dict()
            documents.append(data["text"])
            metadata.append(data["metadata"])
        embeddings = await create_text_embeddings(documents, max_length=768)
        qdrant.upsert(
            collection_name="0775cf17-314c-40c9-afdd-5811100ee2c6",
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
        cnt += len(documents)
        print(f"Processed: {cnt}/{total}")
        break
