from pydantic import BaseModel,EmailStr
from typing import Optional

class RegisterUserSchema(BaseModel):
    username:str
    email:EmailStr
    password:str
    country:str

class GetAllUserSchema(BaseModel):
    id:str
    username:str
    email:str
    password:str
    country:str

class PatchUserSchema(BaseModel):
    username : Optional[str] = None
    email : Optional[EmailStr] = None
    password : Optional[str] = None
    country : Optional[str] = None

class PutForgetPassword(BaseModel):
    new_password : str 
    confirm_password : str 

class resetUserPassword(BaseModel):
    password:str
    new_password : str 
    confirm_password : str 