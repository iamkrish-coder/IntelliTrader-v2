# backend/models/users_model.py

from backend.models.BaseModel import BaseModel


class UsersModel(BaseModel):
    def __init__(
        self,
        user_id=None,
        user_name=None,
        user_email=None,
        user_password=None,
        user_password_salt=None,
        user_password_reset_token=None,
        created_date=None,
        modified_date=None,
    ):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.user_password_salt = user_password_salt
        self.user_password_reset_token = user_password_reset_token
        self.created_date = created_date
        self.modified_date = modified_date
