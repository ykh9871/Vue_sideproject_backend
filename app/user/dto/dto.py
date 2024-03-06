from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    name: str
    email: str
    password: str
    address: str
    phone:str

class UserInfo(BaseModel):
    name: str
    email: str
    address: str
    phone:str
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

class UserInfoUpdate(BaseModel):
    name: str
    email: str
    address: str
    phone:str
    
class ChangePassword(BaseModel):
    current_password : str
    new_password: str

class UserID(BaseModel):
    id: int