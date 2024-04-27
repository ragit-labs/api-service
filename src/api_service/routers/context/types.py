from pydantic import BaseModel, Field
from typing import Optional, Union

class CreateContextRequest(BaseModel):
    name: str = Field(..., title="Context name", description="Name of the context")
    description: str = Field(None, title="Context description", description="Description of the context")
    project_id: str = Field(..., title="Project ID", description="ID of the project to which the context belongs")
    owner_id: str = Field(..., title="Owner ID", description="ID of the owner of the context")
    extra_metadata: Optional[dict] = Field(None, title="Extra metadata", description="Extra metadata for the context")


class ProjectsContextRequest(BaseModel):
    project_id: str = Field(..., title="Project ID", description="ID of the project to which the context belongs")
    limit: int = Field(10, title="Limit", description="Limit of the number of contexts to return")
    offset: int = Field(0, title="Offset", description="Offset of the contexts to return")


class ContextRequest(BaseModel):
    context_id: str = Field(..., title="Context ID", description="ID of the context to get")


class GetContextsRequest(BaseModel):
    where: Union[ProjectsContextRequest, ContextRequest] = Field(..., title="Context request", description="Request to get contexts")


class AddFileRequest(BaseModel):
    context_id: str = Field(..., title="Context ID", description="ID of the context to which the file belongs")
    file_id: str = Field(..., title="File ID", description="ID of the file to add to the context")