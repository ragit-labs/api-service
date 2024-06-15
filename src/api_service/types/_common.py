from pydantic import BaseModel, Field


class TSuccess(BaseModel):
    success: bool = Field(..., title="Success")