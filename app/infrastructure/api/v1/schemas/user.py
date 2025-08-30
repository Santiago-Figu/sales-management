from datetime import datetime
from pydantic import BaseModel, EmailStr, field_serializer
from typing import Optional
from app.utils.datatime_utils import format_datetime_with_timezone

class UserBaseSchema(BaseModel):

    first_name: str = "John"
    last_name: str = "Doe"
    username: str = "TestUser1"
    password: str = "tu_password_seguro"
    email: EmailStr = "example@outlook.com"

class UserCreateSchema(UserBaseSchema):
    pass

class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponseSchema(BaseModel):
    id: int = 1
    first_name: str = "John"
    last_name: str = "Doe"
    username: str = "TestUser1"
    email: EmailStr = "example@outlook.com"
    created: datetime = "12/01/2025"
    last_update: datetime

    @field_serializer('created', 'last_update')
    def serialize_datetime(self, dt: datetime, _info) -> str:
        
        return format_datetime_with_timezone(
            dt,
            timezone_str="America/Mexico_City",
            format_str="%d/%m/%Y %H:%M"
        )
    
    class Config:
        from_attributes = True

class UserFind(BaseModel):
    username_email: str = "Jhondoe | johndoe@example.com"
    password: str = "securepassword"

class UserUpdateMail(BaseModel):
    username: str = "Jhondoe"
    current_email: EmailStr = "johndoe@example.com"
    new_email: EmailStr = "newjohndoe@example.com"

class UserUpdateResponse(UserResponseSchema):
    message: str = "Datos del usuario actualizados correctamente"

class UserDeleteResponse(BaseModel):
    message: str = "User deleted successfully"