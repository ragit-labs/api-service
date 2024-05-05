from fastapi import Request

from ....utils.auth import get_user_from_database_using_id


async def get_user(request: Request):
    return await get_user_from_database_using_id(request.state.user_id)
