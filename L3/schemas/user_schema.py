from pydantic import BaseModel,EmailStr,Field
from uuid import UUID


class CreateUser(BaseModel):
    email:EmailStr
    name:str
    password:str=Field(...,min_length=6,max_length=20)

class UserResponse(BaseModel):
    id:UUID
    name:str
    email:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

