from typing import List

from fastapi import Request
from ragit_db.models import Context
from sqlalchemy import select

from ....database import db
from .types import TContext


async def get_project_contexts(request: Request, project_id: str) -> List[TContext]:
    async with db.session() as session:
        context_query = select(Context).where(Context.project_id == project_id)
        contexts = (await session.execute(context_query)).scalars().all()
        return [
            TContext(
                id=context.id,
                name=context.name,
                description=context.description,
                readable_id=context.readable_id,
                project_id=context.project_id,
                owner_id=context.owner_id,
                search_mode=context.search_mode,
                retrieval_length=context.retrieval_length,
                docs_to_retrieve=context.docs_to_retrieve,
                max_doc_length=context.max_doc_length,
                doc_overlap_length=context.doc_overlap_length,
                embedding_model=context.embedding_model,
                embedding_dimension=context.embedding_dimension,
                distance_metric=context.distance_metric,
                semantic_search=context.semantic_search,
                extra_metadata=context.extra_metadata,
                last_refreshed_at=str(context.last_refreshed_at),
                created_at=str(context.created_at),
            )
            for context in contexts
        ]


async def get_context_by_readable_id(
    request: Request, project_id: str, readable_id: int
) -> TContext:
    async with db.session() as session:
        context_query = select(Context).where(
            Context.project_id == project_id, Context.readable_id == readable_id
        )
        context = (await session.execute(context_query)).scalar_one_or_none()
        return TContext(
            id=context.id,
            name=context.name,
            description=context.description,
            readable_id=context.readable_id,
            project_id=context.project_id,
            owner_id=context.owner_id,
            search_mode=context.search_mode,
            retrieval_length=context.retrieval_length,
            docs_to_retrieve=context.docs_to_retrieve,
            max_doc_length=context.max_doc_length,
            doc_overlap_length=context.doc_overlap_length,
            embedding_model=context.embedding_model,
            embedding_dimension=context.embedding_dimension,
            distance_metric=context.distance_metric,
            semantic_search=context.semantic_search,
            extra_metadata=context.extra_metadata,
            last_refreshed_at=str(context.last_refreshed_at),
            created_at=str(context.created_at),
        )
