from datetime import datetime, timedelta, timezone
from typing import Optional

from ragit_db.models import User
from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select

from api_service.database import db

from ..constants import JWT_ALGORITHM, JWT_DEFAULT_EXPIRY, JWT_SECRET_KEY


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_DEFAULT_EXPIRY)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def parse_user_id_from_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id


async def get_user_from_database_using_id(id: str):
    async with db.session() as session:
        query = select(
            User.id, User.email, User.first_name, User.last_name, User.created_at
        ).where(User.id == id)
        user = (await session.execute(query)).scalars().one_or_none()
        return user
