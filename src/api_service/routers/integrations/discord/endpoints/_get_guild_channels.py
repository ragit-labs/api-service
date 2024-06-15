from fastapi import Request
from typing import List
from .types import TDiscordChannel
from .....clients import discord_client

async def get_guild_channels(request: Request, guild_id: str) -> List[TDiscordChannel]:
    _channels = await discord_client.get_channels_for_guild(guild_id)
    print(_channels)
    channels = filter(lambda channel: channel["type"] == 0, _channels)
    return [TDiscordChannel(
        id=channel["id"],
        guild_id=channel["guild_id"],
        name=channel["name"],
    ) for channel in channels]
