from pydantic import BaseModel, Field
from typing import Union

class GetPresignedUrlRequest(BaseModel):
    key: str = Field(..., title="Key of the object in S3")
    expiration: int = Field(300, title="Expiration time in seconds")
    project_id: str = Field(..., title="Project ID", description="ID of the project to which the context belongs")


class MarkUploadStatusRequest(BaseModel):
    file_id: str = Field(..., title="File ID")


class ProjectFilesRequest(BaseModel):
    project_id: str = Field(..., title="Project ID")


class ContextFilesRequest(BaseModel):
    context_id: str = Field(..., title="Context ID")


class GetFilesRequest(BaseModel):
    where: Union[ProjectFilesRequest, ContextFilesRequest] = Field(..., title="Where to get files from")

class DeleteFileRequest(BaseModel):
    file_id: str = Field(..., title="File ID")