from typing import Optional

from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str = Field(..., title="Project name", description="Name of the project")
    description: Optional[str] = Field(
        None, title="Project description", description="Description of the project"
    )


class GetProjectsRequest(BaseModel):
    limit: int = Field(
        10, title="Limit", description="Limit of the number of contexts to return"
    )
    offset: int = Field(
        0, title="Offset", description="Offset of the contexts to return"
    )


class GetProjectRequest(BaseModel):
    project_id: str = Field(
        ..., title="Project ID", description="ID of the project to get"
    )


class TProject(BaseModel):
    id: str = Field(..., title="Project ID", description="Project's ID")
    name: str = Field(..., title="Name", description="Project's Name")
    owner_id: str = Field(..., title="Owner ID", description="Project's Owner ID")
    description: Optional[str] = Field(
        ..., title="Description", description="Project's Description"
    )
