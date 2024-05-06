from typing import List

from fastapi import HTTPException, Request

from .types import ChatResponse
from .utils import get_chat_history_by_id, get_playground_by_id


async def get_chat_history(request: Request, playground_id: str) -> List[ChatResponse]:
    chat_history = await get_chat_history_by_id(playground_id)
    return [
        ChatResponse(
            id=chat.id,
            playground_id=chat.playground_id,
            user_id=chat.user_id,
            system_prompt=chat.system_prompt,
            user_prompt=chat.user_prompt,
            model=chat.model,
            model_response=chat.model_response,
            model_params=chat.model_params,
            documents=chat.documents,
            created_at=chat.created_at,
        )
        for chat in chat_history
    ]
