from pydantic import BaseModel, Field

class CreateEmbeddingsRequest(BaseModel):
    context_id: str = Field(..., description="Context ID")
    file_id: str = Field(..., description="File ID")
    options: dict = Field({}, description="Options for embeddings generation")
