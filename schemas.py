from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    surname: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str] = None
    surname: Optional[str] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# School
class SchoolBase(BaseModel):
    name: str
    user_id: int


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(SchoolBase):
    name: Optional[str] = None
    user_id: Optional[int] = None


class School(SchoolBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
