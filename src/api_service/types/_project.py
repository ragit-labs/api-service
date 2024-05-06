from pydantic import BaseModel, Field


class TProject(BaseModel):
    id: str = Field(..., title="Project ID", description="Project's ID")
    readable_id: str = Field(
        ..., title="Readable ID", description="Project's Readable ID"
    )
    name: str = Field(..., title="Name", description="Project's Name")
    owner_id: str = Field(..., title="Owner ID", description="Project's Owner ID")
    description: Optional[str] = Field(
        ..., title="Description", description="Project's Description"
    )
