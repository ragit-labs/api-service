from datetime import datetime, timedelta

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from ragit_db.enums import ProjectPermission
from ragit_db.models import Project, User, UserProject
from sqlalchemy import select

from ....constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ....database import db
from ....utils.auth import create_access_token
from ....utils.misc import sanitize_string
from .types import SignupRequest, TAuthResponse


async def signup(request: Request, data: SignupRequest) -> TAuthResponse:
    async with db.session() as session:

        user_query = select(User).where(User.email == data.email)
        user = (await session.execute(user_query)).scalar_one_or_none()

        if user is not None:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

        user = User(
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            created_at=datetime.utcnow(),
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)
        user_id = user.id
        default_project_name = f"{data.first_name}'s Workspace"
        project = Project(
            name=default_project_name,
            description="Default workspace for the user.",
            owner_id=user_id,
            readable_id=sanitize_string(default_project_name).lower(),
        )
        session.add(project)
        await session.flush()
        await session.refresh(project)
        project_id = project.id
        user_project = UserProject(
            user_id=user_id,
            project_id=project_id,
            permission=ProjectPermission.OWNER,
        )

        session.add(user_project)
        await session.commit()

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": str(user_id)}, expires_delta=access_token_expires
        )
        return TAuthResponse(
            access_token=access_token,
            token_type="Bearer",
            expiry=ACCESS_TOKEN_EXPIRE_MINUTES,
        )
