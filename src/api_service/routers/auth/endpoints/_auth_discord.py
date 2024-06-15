from datetime import datetime, timedelta

from fastapi import Request
from ragit_db.models import User
from sqlalchemy import select

from ....constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ....database import db
from ....utils.auth import create_access_token
from .types import SignupDiscordRequest, TAuthResponse
from ....utils._create_project import create_project
from ....utils._get_discord_info import get_discord_info
from ....utils._get_discord_user import get_discord_user
from ....utils._add_guilid import add_guild_to_project


async def auth_discord(request: Request, data: SignupDiscordRequest) -> TAuthResponse:
    code = data.code
    redirect_uri = data.redirect_uri
    guild_id = data.guild_id
    permissions = data.permissions

    discord_info = await get_discord_info(code, redirect_uri)
    print(discord_info)
    discord_user = await get_discord_user(discord_info["access_token"])
    print(discord_user)
    guild = discord_info["guild"]
    
    async with db.session() as session:

        user_query = select(User).where(User.discord_id == discord_user["id"])
        user = (await session.execute(user_query)).scalar_one_or_none()

        if user is not None:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"user_id": str(user.id)}, expires_delta=access_token_expires
            )
            return TAuthResponse(
                access_token=access_token,
                token_type="Bearer",
                expiry=ACCESS_TOKEN_EXPIRE_MINUTES,
            )
        

        user = User(
            discord_id=discord_user["id"],
            discord_username=discord_user["username"],
            discord_access_token=discord_info["access_token"],
            discord_refresh_token=discord_info["refresh_token"],
            discord_expiry_date=datetime.utcnow() + timedelta(seconds=discord_info["expires_in"]),
            created_at=datetime.utcnow(),
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)
        user_id = user.id
        project_id = await create_project(f"{guild['name']}", str(user_id))
        _project_id, _guild_id = await add_guild_to_project(project_id, guild_id)
        await session.commit()
        print("Added user to database")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": str(user_id)}, expires_delta=access_token_expires
        )
        return TAuthResponse(
            access_token=access_token,
            token_type="Bearer",
            expiry=ACCESS_TOKEN_EXPIRE_MINUTES,
        )
