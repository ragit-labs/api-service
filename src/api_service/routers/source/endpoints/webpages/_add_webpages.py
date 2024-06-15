from fastapi import Request

from .....database import db
from ..types import AddWebPagesRequest, MarkSuccess
from ragit_db.models import Source
from ragit_db.enums import SourceStatus, SourceType
from datetime import datetime
from arq.connections import create_pool
from arq.connections import RedisSettings


REDIS_SETTINGS = RedisSettings()


async def add_webpages(
    request: Request, data: AddWebPagesRequest
) -> MarkSuccess:
    async with db.session() as session:
        sources = [
            Source(
                project_id=data.project_id,
                name=url,
                status=SourceStatus.PARSING,
                source_type=SourceType.WEBPAGE,
                url=url,
                created_at=datetime.utcnow(),
                user_id=request.state.user_id,
            ) for url in data.urls
        ]
        session.add_all(sources)
        await session.commit()
    redis = await create_pool(REDIS_SETTINGS)
    await redis.enqueue_job("process_webpage_async", data.project_id, data.urls)
    return MarkSuccess(success=True)
