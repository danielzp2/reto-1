from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Schema para crear usuario (POST)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=100)  # minimo 4 caracteres para las contraseñas

# Schema para actualizar usuario (PUT)
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=4, max_length=100)  

# Schema para devolver usuario (Response)
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
