from fastapi import Request
from typing import List
from .types import TDiscordCreateInteractionRequest, TDiscordCreateInteractionResponse
from .....clients import discord_client
from ragit_db.models import DiscordInteraction
from .....database import db
from datetime import datetime

async def create_interaction(request: Request, data: TDiscordCreateInteractionRequest) -> TDiscordCreateInteractionResponse:
    _message = await discord_client.create_discord_interaction(data.channel_id, data.title, data.content, data.button, data.color)
    async with db.session() as session:
        interaction = DiscordInteraction(
            project_id=data.project_id,
            guild_id=data.guild_id,
            channel_id=data.channel_id,
            message_id=_message["id"],
            message_information=_message,
            updated_at=datetime.utcnow(),
        )
        session.add(interaction)
        await session.commit()
    return TDiscordCreateInteractionResponse(message_id=_message["id"])
