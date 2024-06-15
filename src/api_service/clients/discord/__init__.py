from __future__ import annotations
import aiohttp
from ragit_db.models import DiscordInteraction
from ...database import db
from datetime import datetime

DISCORD_API_ENDPOINT = 'https://discord.com/api/v10'

class DiscordClient:
    
    def __init__(self: DiscordClient, token: str, endpoint_url: str = DISCORD_API_ENDPOINT):
        self.token = token
        self.endpoint_url = endpoint_url
    

    async def get_channels_for_guild(self: DiscordClient, guild_id: str) -> dict:
        async with aiohttp.ClientSession(headers={
            "Authorization": f"Bot {self.token}",
        }) as session:
            async with session.get(f"{self.endpoint_url}/guilds/{guild_id}/channels") as response:
                try:
                    body = await response.json()
                    if "error" in body:
                        raise Exception(status_code=400, detail=body["error"])
                    return body
                except Exception as e:
                    raise Exception(status_code=400, detail=f"{e}")


    async def create_discord_interaction(self: DiscordClient, channel_id: str, title: str, content: str, button: str, color: str) -> dict:
        async with aiohttp.ClientSession(headers={
            "Authorization": f"Bot {self.token}",
        }) as session:
            message_information = {
                "embeds": [
                    {
                        "title": title,
                        "description": content,
                        "color": int(color.replace("#", "0x"), 0),
                    }
                ],
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "style": 1,
                                "label": button,
                                "custom_id": "create_ticket",
                            },
                        ]
                    }
                ]
            }
            async with session.post(f"{self.endpoint_url}/channels/{channel_id}/messages", json=message_information) as response:
                try:
                    body = await response.json()
                    if "error" in body:
                        raise Exception(status_code=400, detail=body["error"])
                    return body
                except Exception as e:
                    raise Exception(status_code=400, detail=f"{e}")
