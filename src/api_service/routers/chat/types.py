from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        title="Query string",
        description="The query string to search for",
        min_length=2,
    )
    context_id: str = Field(
        ...,
        title="Context ID",
        description="The context ID to search in",
    )
