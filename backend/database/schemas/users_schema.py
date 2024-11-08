from pydantic import BaseModel, Field

class UsersSchema(BaseModel):
    user_full_name: str = Field(..., alias='userFullName')
    user_email: str = Field(..., alias='userEmail')
    user_password: str = Field(..., alias='userPassword')