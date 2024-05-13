from typing import List

from fastapi import Request
from ragit_db.models import Playground
from sqlalchemy import select

from ....database import db
from .types import PlayGroundResponse


async def get_playgrounds(
    request: Request, project_id: str
) -> List[PlayGroundResponse]:
    async with db.session() as session:
        get_playground_query = select(Playground).where(
            Playground.project_id == project_id
        )
        playground = (await session.execute(get_playground_query)).scalars().all()
        return [
            PlayGroundResponse(
                id=playground.id,
                name=playground.name,
                description=playground.description,
                readable_id=playground.readable_id,
                project_id=playground.project_id,
                context_id=playground.context_id,
                owner_id=playground.owner_id,
            )
            for playground in playground
        ]
