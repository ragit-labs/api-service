from pydantic import BaseModel, Field



class SignupRequest(BaseModel):
    email: str = Field(..., title="Email", description="User's Email")
    password: str = Field(..., title="Password", description="User's Password")
    first_name: str = Field(..., title="First Name", description="User's First Name")
    last_name: str = Field(..., title="Last Name", description="User's Last Name")


class LoginRequest(BaseModel):
    email: str = Field(..., title="Email", description="User's Email")
    password: str = Field(..., title="Password", description="User's Password")
