from fastapi import APIRouter, Request, HTTPException, Depends
from ...dependencies.auth import login_required
from fastapi.responses import JSONResponse
from db.models import User, Project, UserProject
from db.enums import ProjectPermission
from api_service.database import db
from .types import SignupRequest, LoginRequest
from datetime import datetime
from sqlalchemy import select
from datetime import timedelta
from ...constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ...utils.auth import create_access_token, get_user_from_database_using_id
from ...utils.misc import sanitize_string
router = APIRouter(tags=["auth", "login"])


@router.post("/auth/signup")
async def signup(request: Request, data: SignupRequest):
    async with db.session() as session:

        user_query = select(User).where(User.email == data.email)
        user = (await session.execute(user_query)).scalar_one_or_none()

        if user is not None:
            raise HTTPException(status_code=409, detail="User with this email already exists")

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
        return JSONResponse(
            content={
                "access_token": access_token,
                "token_type": "Bearer",
                "expiry": ACCESS_TOKEN_EXPIRE_MINUTES,
            },
            status_code=200,
        )


@router.post("/auth/login")
async def login(request: Request, data: LoginRequest):
    async with db.session() as session:
        user_query = select(User).where(User.email == data.email)
        user = (await session.execute(user_query)).scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User with this email does not exist")

        if user.password != data.password:
            raise HTTPException(status_code=401, detail="Password is incorrect")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": str(user.id)}, expires_delta=access_token_expires
        )
        return JSONResponse(
            content={
                "access_token": access_token,
                "token_type": "Bearer",
                "expiry": ACCESS_TOKEN_EXPIRE_MINUTES,
            },
            status_code=200,
        )


@router.get("/auth/get", dependencies=[Depends(login_required)])
async def get_user(request: Request):
    return await get_user_from_database_using_id(request.state.user_id)
