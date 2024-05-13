from datetime import timedelta

from fastapi import HTTPException, Request
from ragit_db.models import User
from sqlalchemy import select

from ....constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ....database import db
from ....utils.auth import create_access_token
from .types import LoginRequest, TAuthResponse, TUser


async def login(request: Request, data: LoginRequest) -> TAuthResponse:
    async with db.session() as session:
        user_query = select(User).where(User.email == data.email)
        user = (await session.execute(user_query)).scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=404, detail="User with this email does not exist"
            )

        if user.password != data.password:
            raise HTTPException(status_code=401, detail="Password is incorrect")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": str(user.id)}, expires_delta=access_token_expires
        )
        return TAuthResponse(
            access_token=access_token,
            token_type="Bearer",
            expiry=ACCESS_TOKEN_EXPIRE_MINUTES,
            user=TUser(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                signin_provider=user.signin_provider or "",
                created_at=str(user.created_at),
            ),
        )
