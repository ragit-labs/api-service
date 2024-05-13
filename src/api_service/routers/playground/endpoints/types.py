from typing import Optional

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
    model: str = Field(
        ...,
        title="Model Provider",
        description="The model provider to use",
    )
    model_params: dict = Field(
        ...,
        title="Model Parameters",
        description="The model parameters to use",
    )


class CreatePlaygroundRequest(BaseModel):
    project_id: str = Field(
        ...,
        title="Project ID",
        description="The project ID to create the playground with",
    )
    context_id: str = Field(
        ...,
        title="Context ID",
        description="The context ID to create the playground with",
    )
    name: str = Field(
        ...,
        title="Name",
        description="The name of the playground",
        min_length=2,
    )
    description: Optional[str] = Field(
        None,
        title="Description",
        description="The description of the playground",
    )


class ChatResponse(BaseModel):
    id: str = Field(..., title="Chat ID", description="The chat ID")
    playground_id: str = Field(
        ..., title="Playground ID", description="The playground ID"
    )
    user_id: str = Field(..., title="User ID", description="The user ID")
    system_prompt: str = Field(
        ..., title="System Prompt", description="The system prompt"
    )
    user_prompt: str = Field(..., title="User Prompt", description="The user prompt")
    model_response: str = Field(
        ..., title="Model Response", description="The model response"
    )
    model: str = Field(..., title="Model", description="The model")
    model_params: dict = Field(
        ..., title="Model Parameters", description="The model parameters"
    )
    documents: list[str] = Field(..., title="Documents", description="The documents")
    created_at: str = Field(
        ..., title="Created At", description="The creation date and time"
    )


class PlayGroundResponse(BaseModel):
    id: str = Field(..., title="Playground ID", description="The playground ID")
    name: str = Field(..., title="Name", description="The name of the playground")
    description: Optional[str] = Field(
        ..., title="Description", description="The description of the playground"
    )
    readable_id: int = Field(
        ..., title="Readable ID", description="The readable ID of the playground"
    )
    project_id: str = Field(
        ..., title="Project ID", description="The project ID of the playground"
    )
    context_id: str = Field(
        ..., title="Context ID", description="The context ID of the playground"
    )
    owner_id: str = Field(
        ..., title="Owner ID", description="The owner ID of the playground"
    )
