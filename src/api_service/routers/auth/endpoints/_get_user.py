from fastapi import Request

from ....utils.auth import get_user_from_database_using_id
from .types import TUser


async def get_user(request: Request) -> TUser:
    user = await get_user_from_database_using_id(request.state.user_id)
    return TUser(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        signin_provider=user.signin_provider or "",
        created_at=str(user.created_at),
    )
