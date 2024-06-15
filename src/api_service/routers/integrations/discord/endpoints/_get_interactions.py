from fastapi import Request
from typing import List
from .types import TDiscordInteraction
from ragit_db.models import DiscordInteraction
from .....database import db
from sqlalchemy import select

async def get_interactions(request: Request, project_id: str) -> List[TDiscordInteraction]:
    async with db.session() as session:
        interaction_query = select(DiscordInteraction).where(DiscordInteraction.project_id == project_id)
        interactions = (await session.execute(interaction_query)).scalars().all()
        return [
            TDiscordInteraction(
                id=str(interaction.id),
                project_id=str(interaction.project_id),
                guild_id=str(interaction.guild_id),
                channel_id=str(interaction.channel_id),
                message_id=str(interaction.message_id),
                message_information=interaction.message_information,
                updated_at=str(interaction.updated_at),
            )
            for interaction in interactions
       ]
