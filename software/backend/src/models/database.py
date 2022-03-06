import typing
from numpy import number
from pydantic import BaseModel


class CropValueSchema(BaseModel):
    crop: str
    kc: float

    class Config:
        orm_mode = True

class UpdateCropValueSchema(BaseModel):
    kc: float

class ModelTypeSchema(BaseModel):
    id: int
    description: str
    
    class Config:
        orm_mode = True


class ModelSchema(BaseModel):
    id: int
    description: str
    type: int
    location: str
    
    class Config:
        orm_mode = True
