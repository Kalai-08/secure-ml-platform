from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import Role

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: Role
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" 
    #bearer token is a type of access token that is used in authentication 
    # and authorization protocols, such as OAuth 2.0.
    #  It is called a "bearer" token because the client must present the token to the server in order to access protected resources.
    #  The server then verifies the token and grants access if it is valid.