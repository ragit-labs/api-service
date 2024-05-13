from uuid import uuid4

from fastapi import Request

from .types import CreatePlaygroundRequest, PlayGroundResponse
from .utils import create_playground


async def create_playground_(
    request: Request, data: CreatePlaygroundRequest
) -> PlayGroundResponse:
    playground = await create_playground(
        playground_id=uuid4(),
        project_id=data.project_id,
        context_id=data.context_id,
        name=data.name,
        description=data.description,
        owner_id=request.state.user_id,
    )
    return PlayGroundResponse(
        id=playground.id,
        name=playground.name,
        description=playground.description,
        readable_id=playground.readable_id,
        project_id=playground.project_id,
        context_id=playground.context_id,
        owner_id=playground.owner_id,
    )
