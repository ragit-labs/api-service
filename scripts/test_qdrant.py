import asyncio
from unstructured.partition.pdf import partition_pdf
from api_service.clients import s3_client, qdrant
import io
from api_service.routers.embeddings.utils import create_text_embeddings
from qdrant_client.models import PointStruct
from uuid import uuid4

async def main():
    fk = "PxzVao_Jessica-Livingston---Founders-at-Work_-Stories-of-Startups-Early-Days-Apress-2009.pdf"
    file_data = s3_client.download_file_as_obj(fk)
    file_bytes = file_data['Body'].read()
    file_stream = io.BytesIO(file_bytes)
    partitions = partition_pdf(file=file_stream)
    documents = []
    metadata = []
    
    for partition in partitions:
        data = partition.to_dict()
        documents.append(data['text'])
        metadata.append(data['metadata'])
    embeddings = await create_text_embeddings(documents, max_length=768)
    qdrant.upsert(
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

asyncio.run(main())
