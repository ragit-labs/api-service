from pydantic import BaseModel, Field


class TUser(BaseModel):
    id: str = Field(..., title="User ID", description="User's ID")
    email: str = Field(..., title="Email", description="User's Email")
    first_name: str = Field(..., title="First Name", description="User's First Name")
    last_name: str = Field(..., title="Last Name", description="User's Last Name")
    signin_provider: str = Field(
        ..., title="Signin Provider", description="User's Signin Provider"
    )
    created_at: str = Field(..., title="Created At", description="User's Created At")
