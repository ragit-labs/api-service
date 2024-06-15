import aiohttp
from fastapi import HTTPException


DISCORD_API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = "1247251128249225348"
CLIENT_SECRET = "R5A7wD3qjZZCjNZDka4WgVrRkj0q_LWB"


async def get_discord_info(code: str, redirect_uri: str) -> dict:
    async with aiohttp.ClientSession(headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }, auth=aiohttp.BasicAuth(CLIENT_ID, CLIENT_SECRET)) as session:
        async with session.post(f"{DISCORD_API_ENDPOINT}/oauth2/token", data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }) as response:
            body = await response.json()
            if "error" in body:
                raise HTTPException(status_code=400, detail=body["error"])
            try:
                access_token = body["access_token"]
                refresh_token = body["refresh_token"]
                print(access_token, refresh_token)
                return body
            except KeyError as e:
                raise HTTPException(status_code=400, detail=f"{e}")
