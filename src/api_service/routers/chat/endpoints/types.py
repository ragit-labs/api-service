from typing import Optional

from pydantic import BaseModel, Field


class DiscordChatRequest(BaseModel):
    message: str = Field(
        ...,
        title="Message",
        min_length=2,
    )
    message_id: int = Field(
        ...,
        title="Discord Message ID",
    )
    user_id: int = Field(
        ...,
        title="Discord User ID",
    )
    channel_id: int = Field(
        ...,
        title="Discord Channel ID",
    )
    guild_id: int = Field(
        title="Discord Guild ID",
    )



class DiscordChatResponse(BaseModel):
    response: str = Field(
        ...,
        title="Response",
    )
