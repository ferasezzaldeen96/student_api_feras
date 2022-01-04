from enum import Enum
from typing import Optional
from pydantic import Field, validator , BaseModel  
from datetime import datetime
from uuid import UUID

class Gender(Enum):
    male = 'male'
    female = 'female'


class PostStudent(BaseModel):
    id: Optional[int] = Field(example=1234 )
    name: str = Field(example='name', max_length=30)
    major: str = Field(example='the major', max_length=50)
    gender: Gender
    @validator('gender')
    def validate_gender(cls, value: str):
        try:
            value = Gender(value)
        except ValueError:
            ValueError('This gender is not available')
        return value
    @validator("name")
    def validate_name(cls, value:str):
        try:
            print(len(value))
            len(value)<20
        except ValueError:
            ValueError('name length can not exceed 20')
        return value


class PatchStudent(BaseModel):
    name: Optional[str] = Field(example='name')
    major: Optional[str] = Field(example='the major')
    gender: Optional[Gender]

    @validator('gender')
    def validate_gender(cls, value: str):
        try:
            value = Gender(value)
        except ValueError:
            ValueError('This gender is not available')
        return value


class PutStudent(BaseModel):
    id: Optional[int] = Field(example=1234)
    name: str = Field(example='name', max_length=30)
    major: str = Field(example='the major', max_length=50)
    gender: Gender

    @validator('gender')
    def validate_gender(cls, value: str):
        try:
            value = Gender(value)
        except ValueError:
            ValueError('This gender is not available')
        return value


def enum_to_string(cls) -> str:
    return ', '.join([f'{e.name}' for e in cls])


class StudentResponse (BaseModel):
    id: int = Field(example=1234)
    name: Optional[str] = Field(example='name')
    major: Optional[str] = Field(example='the major')
    gender: Optional[str] = Field(example=enum_to_string(Gender))


class TestDB(BaseModel):
    id: Optional[UUID] = Field(example="b1067c8e-6d3c-11ec-90d6-0242ac120003")
    name: str
    gender: str
    state: str
    department: str
    birth_date: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PostDB(BaseModel):
    name: str
    gender: str
    state: str
    department: str

class PatchDB(BaseModel):
    name: Optional[str]
    gender: Optional[str]
    state: Optional[str]
    department: Optional[str]
    
class PutDB(BaseModel):
    name: str
    gender: str
    state: str
    department: str
    