from typing import Optional

from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    email: str = Field(..., title="Email", description="User's Email")
    password: str = Field(..., title="Password", description="User's Password")
    first_name: str = Field(..., title="First Name", description="User's First Name")
    last_name: str = Field(..., title="Last Name", description="User's Last Name")


class SignupDiscordRequest(BaseModel):
    code: str = Field(..., title="Code", description="Discord Auth Code")
    guild_id: str = Field(..., title="Guild ID", description="Guild ID")
    permissions: str = Field(..., title="Permissions", description="Permissions")
    redirect_uri: str = Field(..., title="Redirect URI", description="Redirect URI")


class LoginRequest(BaseModel):
    email: str = Field(..., title="Email", description="User's Email")
    password: str = Field(..., title="Password", description="User's Password")


class TUser(BaseModel):
    id: str = Field(..., title="User ID", description="User's ID")
    email: Optional[str] = Field(None, title="Email", description="User's Email")
    first_name: Optional[str] = Field(None, title="First Name", description="User's First Name")
    last_name: Optional[str] = Field(None, title="Last Name", description="User's Last Name")
    discord_id: Optional[str] = Field(None, title="Discord ID", description="User's Discord ID")
    discord_username: Optional[str] = Field(
        None, title="Discord Username", description="User's Discord Username"
    )
    signin_provider: Optional[str] = Field(
        None, title="Signin Provider", description="User's Signin Provider"
    )
    created_at: str = Field(..., title="Created At", description="User's Created At")


class TAuthResponse(BaseModel):
    access_token: str = Field(..., title="Access Token", description="Access Token")
    token_type: str = Field(..., title="Token Type", description="Token Type")
    expiry: int = Field(..., title="Expiry", description="Expiry")
