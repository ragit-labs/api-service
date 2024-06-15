from pydantic import BaseModel, Field

class TDiscordChannel(BaseModel):
    id: str = Field(..., title="Channel ID")
    guild_id: str = Field(..., title="Guild ID")
    name: str = Field(..., title="Channel Name")


class TDiscordCreateInteractionRequest(BaseModel):
    project_id: str = Field(..., title="Project ID")
    guild_id: str = Field(..., title="Guild ID")
    channel_id: str = Field(..., title="Channel ID")
    title: str = Field(..., title="Title")
    content: str = Field(..., title="Content")
    button: str = Field(..., title="Button")
    color: str = Field(..., title="Color")


class TDiscordCreateInteractionResponse(BaseModel):
    message_id: str = Field(..., title="Message ID")


class TDiscordInteraction(BaseModel):
    id: str = Field(..., title="Interaction ID")
    project_id: str = Field(..., title="Project ID")
    guild_id: str = Field(..., title="Guild ID")
    channel_id: str = Field(..., title="Channel ID")
    message_id: str = Field(..., title="Message ID")
    message_information: dict = Field(..., title="Message Information")
    updated_at: str = Field(..., title="Updated At")
