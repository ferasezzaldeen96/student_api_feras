from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

today = date.today()


class Gender(str, Enum):
    male = 'male'
    female = 'female'


class BaseStudent(BaseModel):
    id: Optional[UUID]
    name: str = Field(example="first middle last", max_length=50)
    gender: Gender = Field(example="male or female", max_length=10)
    state: str = Field(example="New York, LA, Texas", max_length=20)
    department: str = Field(
        example="civil engineer, sotware engineer", max_length=40)
    birth_date: date
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PostStudent(BaseModel):
    name: str = Field(example="first middle last", max_length=50)
    gender: Gender = Field(example="male or female", )
    state: str = Field(example="New York, LA, Texas", max_length=20)
    department: str = Field(
        example="civil engineer, sotware engineer", max_length=40)
    birth_date: date

    @validator("birth_date", pre=True)
    def check_birth_date(cls, value: str):
        if value > str(datetime.utcnow()):
            raise ValueError('wrong entry')
        else:
            return value


class PatchStudent(BaseModel):
    name: Optional[str] = Field(example="first middle last", max_length=50)
    gender: Optional[Gender] = Field(example="male or female", max_length=10)
    state: Optional[str] = Field(example="New York, LA, Texas", max_length=20)
    department: Optional[str] = Field(
        example="civil engineer, sotware engineer", max_length=40)
    birth_date: Optional[date]

    @validator("birth_date", pre=True)
    def check_birth_date(cls, value: str):
        if value > str(datetime.utcnow()):
            raise ValueError('wrong entry')
        else:
            return value


class PutStudent(BaseModel):
    name: str = Field(example="first middle last", max_length=50)
    gender: Gender = Field(example="male or female", max_length=10)
    state: str = Field(example="New York, LA, Texas", max_length=20)
    department: str = Field(
        example="civil engineer, sotware engineer", max_length=40)
    birth_date: date
    created_at: datetime
    updated_at: datetime

    @validator("birth_date", pre=True)
    def check_birth_date(cls, value: str):
        if value > str(datetime.utcnow()):
            raise ValueError('wrong entry')
        else:
            return value
