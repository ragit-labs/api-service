from fastapi import HTTPException, Request
from ragit_db.models import Context
from sqlalchemy import select

from ....clients import qdrant
from ....database import db
from ....utils import create_text_embeddings
from .types import SearchRequest


async def search_documents(request: Request, data: SearchRequest):
    async with db.session() as session:
        context_query = select(Context).where(Context.id == data.context_id)
        context = (await session.execute(context_query)).scalar_one_or_none()
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")
        max_len = context.max_doc_length
        query_embedding = list(
            create_text_embeddings([data.query], max_len, context.embedding_model)
        )[0]
        docs_to_retrieve = context.docs_to_retrieve

    return qdrant.search(
        collection_name=data.context_id,
        query_vector=query_embedding.tolist(),
        limit=docs_to_retrieve,
    )
