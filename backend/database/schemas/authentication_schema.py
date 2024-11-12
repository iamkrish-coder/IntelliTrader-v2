from pydantic import BaseModel, Field, EmailStr


class UsersSchema(BaseModel):
    user_full_name: str = Field(..., alias="userFullName")
    user_email: EmailStr = Field(..., alias="userEmail")
    user_password: str = Field(..., alias="userPassword")


class LoginSchema(BaseModel):
    user_email: EmailStr = Field(..., alias="userEmail")
    user_password: str = Field(..., alias="userPassword")


class ForgotPasswordSchema(BaseModel):
    user_email: EmailStr = Field(..., alias="userEmail")


class ResetPasswordSchema(BaseModel):
    token: str = Field(..., alias="token")
    user_password: str = Field(..., alias="userPassword")
