from pydantic import BaseModel,EmailStr,Field
from uuid import UUID
from models.user_role import UserRole


class CreateUser(BaseModel):
    email:EmailStr
    name:str
    password:str=Field(...,min_length=6,max_length=20)
    role_name:UserRole = UserRole.NEW_HIRE

class UserResponse(BaseModel):
    id:UUID
    name:str
    email:str
    role_name:UserRole
    assigned_to:UUID | None = None

class UserLogin(BaseModel):
    email:EmailStr
    password:str

