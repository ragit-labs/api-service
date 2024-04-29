from fastapi import APIRouter, Request, HTTPException, Depends
from api_service.clients import s3_client, qdrant
from db.models import Project
from api_service.database import db
from .types import CreateProjectRequest, GetProjectsRequest
from sqlalchemy import select

router = APIRouter(tags=["project"])

@router.post("/project/create")
async def create_project(request: Request, data: CreateProjectRequest):

    if not data.name:
        raise HTTPException(status_code=400, detail="name is not in the request.")
    if not data.owner_id:
        raise HTTPException(status_code=400, detail="owner_id is not in the request.")

    async with db.session() as session:
        get_project_query = select(Project).where(Project.owner_id == data.owner_id, Project.name == data.name)
        get_project_result = (await session.execute(get_project_query)).scalar_one_or_none()
        if get_project_result is not None:
            raise HTTPException(status_code=409, detail=f"Project by the name {data.name} already exists in this project.")
        
        try:
            new_project = Project(
                name=data.name,
                description=data.description or "",
                owner_id=data.owner_id,
            )
            session.add(new_project)
            await session.flush()
            await session.refresh(new_project)
            project_id = new_project.id
            if qdrant.create_collection(project_id, vectors_config={
                "distance": "Cosine",
                "size": "768",
                "on_disk": True
            }):
                await session.commit()
                return {"id": str(project_id)}
            else:
                await session.rollback()
                raise HTTPException(status_code=500, detail="Could not create project.")
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Could not create project. Error: {str(ex)}")


@router.get("/project/get")
async def get_all_projects(request: Request, limit: int = 10, offset: int = 0):
    owner_id = request.state.user_id
    async with db.session() as session:
        get_project_query = select(Project).where(Project.owner_id == owner_id).limit(limit).offset(offset)
        get_project_result = (await session.execute(get_project_query)).scalars().all()
        return get_project_result


@router.get("/project/get/{project_id}")
async def get_project(request: Request, project_id: str):
    async with db.session() as session:
        get_project_query = select(Project).where(Project.readable_id == project_id.lower())
        get_project_result = (await session.execute(get_project_query)).scalar_one_or_none()
        if get_project_result is None:
            raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found.")
        return get_project_result


@router.get("/project/getbyuuid/{project_id}")
async def get_project(request: Request, project_id: str):
    async with db.session() as session:
        get_project_query = select(Project).where(Project.id == project_id)
        get_project_result = (await session.execute(get_project_query)).scalar_one_or_none()
        if get_project_result is None:
            raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found.")
        return get_project_result
