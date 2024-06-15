from fastapi import APIRouter, Depends

from ...dependencies.auth import login_required
from .discord.endpoints import get_guild_channels, create_interaction, get_interactions

router = APIRouter(tags=["integrations"])
router.add_api_route("/discord/guilds/{guild_id}/channels", endpoint=get_guild_channels, methods=["GET"], dependencies=[Depends(login_required)])
router.add_api_route("/discord/interactions", endpoint=create_interaction, methods=["POST"], dependencies=[Depends(login_required)])
router.add_api_route("/discord/interactions/{project_id}", endpoint=get_interactions, methods=["GET"], dependencies=[Depends(login_required)])