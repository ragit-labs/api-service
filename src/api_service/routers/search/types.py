from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    context_id: str = Field(
        ..., title="Context ID", description="The ID of the context to search in"
    )
    query: str = Field(
        ...,
        title="Query string",
        description="The query string to search for",
        min_length=3,
        max_length=100,
    )
    semantic: bool = Field(
        False,
        title="Semantic search",
        description="Whether to perform a semantic search or not",
    )
