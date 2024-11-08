# models/users_model.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from backend.database.database import Base

class UsersModel(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_full_name = Column(String(50), unique=True, nullable=False)
    user_email = Column(String(100), unique=True, nullable=False)
    user_password = Column(String(100), nullable=False)
    user_password_salt = Column(String(100), nullable=False)
    user_created_at = Column(TIMESTAMP, server_default=func.now())
