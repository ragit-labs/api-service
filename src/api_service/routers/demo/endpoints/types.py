from typing import List
from pydantic import BaseModel, Field


class ChatHistory(BaseModel):
    role: str = Field(..., title="Role")
    message: str = Field(..., title="Message")


class ChatRequest(BaseModel):
    query: str = Field(..., title="Query")
    history: List[ChatHistory] = Field([], title="Chat History")


class ChatResponse(BaseModel):
    messages: List[str] = Field(..., title="Assistant Responses")
