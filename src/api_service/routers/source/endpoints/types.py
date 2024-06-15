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


class DeleteSourceRequest(BaseModel):
    source_id: str = Field(..., title="Source ID")


class TSource(BaseModel):
    id: str = Field(..., title="Source ID")
    project_id: str = Field(..., title="Project ID")
    name: str = Field(..., title="Source Name")
    status: str = Field(..., title="Status")
    source_type: str = Field(..., title="Source Type")
    url: Optional[str] = Field(None, title="URL")
    created_at: str = Field(..., title="Created At")
    extra_metadata: Optional[dict] = Field(None, title="Extra Metadata")
    user_id: str = Field(..., title="User ID")


class PresignedUrl(BaseModel):
    url: str = Field(..., title="Presigned URL")
    file_id: str = Field(..., title="File ID")


class MarkSuccess(BaseModel):
    success: bool = Field(..., title="Success")


class AddWebPagesRequest(BaseModel):
    project_id: str = Field(..., title="Project ID")
    urls: list[str] = Field(..., title="List of URLs")
