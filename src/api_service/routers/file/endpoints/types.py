from typing import Optional, Union

from pydantic import BaseModel, Field


class GetPresignedUrlRequest(BaseModel):
    key: str = Field(..., title="Key of the object in S3")
    expiration: int = Field(300, title="Expiration time in seconds")
    project_id: str = Field(
        ...,
        title="Project ID",
        description="ID of the project to which the context belongs",
    )
    file_size: int = Field(
        ...,
        title="File Size",
        description="Size of the file in bytes",
    )
    file_type: str = Field(
        ...,
        title="File Type",
        description="Type of the file",
    )


class MarkUploadStatusRequest(BaseModel):
    file_id: str = Field(..., title="File ID")


class ProjectFilesRequest(BaseModel):
    project_id: str = Field(..., title="Project ID")


class ContextFilesRequest(BaseModel):
    context_id: str = Field(..., title="Context ID")


class GetFilesRequest(BaseModel):
    where: Union[ProjectFilesRequest, ContextFilesRequest] = Field(
        ..., title="Where to get files from"
    )


class DeleteFileRequest(BaseModel):
    file_id: str = Field(..., title="File ID")


class TFile(BaseModel):
    id: str = Field(..., title="File ID")
    name: str = Field(..., title="File Name")
    status: str = Field(..., title="Status")
    description: Optional[str] = Field(None, title="Description")
    project_id: str = Field(..., title="Project ID")
    owner_id: str = Field(..., title="Owner ID")
    created_at: str = Field(..., title="Created At")
    file_size: int = Field(..., title="File Size")
    file_type: str = Field(..., title="File Type")
    extra_metadata: Optional[dict] = Field(None, title="Extra Metadata")


class TContextFile(BaseModel):
    file_id: str = Field(..., title="File ID")
    context_id: str = Field(..., title="Context ID")
    name: str = Field(..., title="File Name")
    status: str = Field(..., title="Status")


class PresignedUrl(BaseModel):
    url: str = Field(..., title="Presigned URL")
    file_id: str = Field(..., title="File ID")


class MarkSuccess(BaseModel):
    success: bool = Field(..., title="Success")
