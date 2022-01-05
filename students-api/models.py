from enum import Enum
from typing import Optional
from pydantic import Field, validator , BaseModel  
from datetime import datetime
from uuid import UUID


class TestDB(BaseModel):
    id: Optional[UUID] = Field(example="b1067c8e-6d3c-11ec-90d6-0242ac120003",)
    name: str = Field(example="first middle last", max_length=40)
    gender: str = Field(example="male or female", max_length=10)
    state: str = Field(example="New York, LA, Texas" , max_length=20)
    department: str = Field(example="civil engineer, sotware engineer" , max_length=40)
    birth_date: Optional[datetime] 
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PostDB(BaseModel):
    name: str = Field(example="first middle last", max_length=40)
    gender: str = Field(example="male or female", max_length=10)
    state: str = Field(example="New York, LA, Texas" , max_length=20)
    department: str = Field(example="civil engineer, sotware engineer" , max_length=40)

class PatchDB(BaseModel):
    name: Optional[str] = Field(example="first middle last", max_length=40)
    gender: Optional[str] = Field(example="male or female", max_length=10)
    state: Optional[str] = Field(example="New York, LA, Texas" , max_length=20)
    department: Optional[str] = Field(example="civil engineer, sotware engineer" , max_length=40)
    
class PutDB(BaseModel):
    name: str = Field(example="first middle last", max_length=40)
    gender: str = Field(example="male or female", max_length=10)
    state: str = Field(example="New York, LA, Texas" , max_length=20)
    department: str = Field(example="civil engineer, sotware engineer" , max_length=40) 
    