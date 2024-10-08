from typing import Optional

from fastapi import Request

from ....utils.auth import get_user_from_database_using_id
from .types import TUser


async def get_user(request: Request) -> Optional[TUser]:
    user = await get_user_from_database_using_id(request.state.user_id)
    if user:
        return TUser(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            discord_id=user.discord_id,
            discord_username=user.discord_username,
            signin_provider=user.signin_provider,
            created_at=str(user.created_at),
        )
    return None
