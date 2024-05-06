from fastapi import HTTPException, Request

from .types import PlayGroundResponse
from .utils import get_chat_history_by_id, get_playground_by_id


async def get_playground(request: Request, playground_id: str) -> PlayGroundResponse:
    playground = await get_playground_by_id(playground_id)
    if not playground:
        raise HTTPException(status_code=404, detail="Playground not found")
    chat_history = await get_chat_history_by_id(playground_id)
    return PlayGroundResponse(
        id=playground.id,
        name=playground.name,
        description=playground.description,
        readable_id=playground.readable_id,
        project_id=playground.project_id,
        context_id=playground.context_id,
        owner_id=playground.owner_id,
        chat_history=chat_history,
    )
