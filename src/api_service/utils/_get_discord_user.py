import aiohttp
from fastapi import HTTPException


DISCORD_API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = "1247251128249225348"
CLIENT_SECRET = "R5A7wD3qjZZCjNZDka4WgVrRkj0q_LWB"


async def get_discord_user(access_token: str) -> dict:
    async with aiohttp.ClientSession(headers={
        "Authorization": f"Bearer {access_token}",
    }) as session:
        async with session.get(f"{DISCORD_API_ENDPOINT}/users/@me") as response:
            body = await response.json()
            if "error" in body:
                raise HTTPException(status_code=400, detail=body["error"])
            try:
                _id = body["id"]
                username = body["username"]
                discriminator = body["discriminator"]
                avatar = body["avatar"]
                return {
                    "id": _id,
                    "username": username,
                    "discriminator": discriminator,
                    "avatar": avatar,
                }
            except KeyError as e:
                raise HTTPException(status_code=400, detail=f"{e}")
