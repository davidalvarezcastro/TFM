""" Gestión información de cultivos """

import typing
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.dao.crop_value import DAOCropValue
from src.database.mysql import SessionLocal
from src.models.database import CropValueSchema, UpdateCropValueSchema
from src.database.models import CropValueORM
from src.models.responses import ErrorMessage, SuccessMessage
from src.api.dependencies.db import get_db


router = APIRouter()


@router.get(
    "/crops", tags=["crops"],
    name="GETs Crops",
    description="Gets list of crops",
    responses={
        500: {"model": ErrorMessage}
    },
    response_model=typing.List[CropValueSchema]
)
async def get_crops(db: SessionLocal = Depends(get_db)):
    status_code = 200
    content = {}

    try:
        content = jsonable_encoder([CropValueSchema.from_orm(c) for c in DAOCropValue.get_crop_values(db)])
    except Exception as e:
        status_code = 500
        content = {
            "msg": "Error getting crops information" 
        }

    return JSONResponse(
        status_code = status_code,
        content = content
    )

@router.get(
    "/crop/{crop}", tags=["crops"],
    name="GETs Crop",
    description="Gets information about a specific crop",
    responses={
        404: {"model": ErrorMessage},
        500: {"model": ErrorMessage},
    },
    response_model=CropValueSchema
)
async def get_crop(crop: str, db: SessionLocal = Depends(get_db)):
    status_code = 200
    content = {}

    try:
        info = DAOCropValue.get_crop_values_by_crop(db, crop)
        
        if info is None:
            status_code = 404
            content = {
            "msg": f"{crop} not found!" 
        }
        else:
            content = jsonable_encoder(info)
    except Exception as e:
        status_code = 500
        content = {
            "msg": "Error getting crops information" 
        }

    return JSONResponse(
        status_code = status_code,
        content = content
    )

@router.post(
    "/crop", tags=["crops"],
    name="CREATEs Crop",
    description="Adds a new crop",
    responses={
        500: {"model": ErrorMessage},
    },
    response_model=CropValueSchema
)
async def post_crop(crop: CropValueSchema, db: SessionLocal = Depends(get_db)):
    status_code = 201
    content = {}
    error_msg = "Error adding crop information"

    try:
        # check if crop exists
        if DAOCropValue.get_crop_values_by_crop(db, crop.crop) is None:
            if not DAOCropValue.add_crop_info(db, CropValueORM(**crop.dict())):
                raise Exception(error_msg)
            else:
                content = crop.dict()
        else:
            status_code = 500
            content = {
                "msg": f"Crop {crop.crop} already in the database"
            }
    except Exception as e:
        status_code = 500
        content = {
            "msg": error_msg
        }

    return JSONResponse(
        status_code = status_code,
        content = content
    )

@router.put(
    "/crop/{crop_name}", tags=["crops"],
    name="UPDATEs Crop",
    description="Updates info from a specific crop",
    responses={
        404: {"model": ErrorMessage},
        500: {"model": ErrorMessage},
    },
    response_model=CropValueSchema
)
async def put_crop(crop_name: str, crop: UpdateCropValueSchema, db: SessionLocal = Depends(get_db)):
    status_code = 200
    content = {}
    error_msg = "Error updating crop information"
        
    try:
        # check if crop exists
        crop_db =  DAOCropValue.get_crop_values_by_crop(db, crop_name)
        if crop_db:
            if not DAOCropValue.update_crop_info(db, crop_name, crop):
                raise Exception(error_msg)
            else:
                content = crop.dict()
        else:
            status_code = 404
            content = {
                "msg": f"Crop {crop_name} does not exists"
            }
    except Exception as e:
        status_code = 500
        content = {
            "msg": error_msg
        }

    return JSONResponse(
        status_code = status_code,
        content = content
    )

@router.delete(
    "/crop/{crop_name}", tags=["crops"],
    name="DELETEs Crop",
    description="Removes a specific crop",
    responses={
        404: {"model": ErrorMessage},
        500: {"model": ErrorMessage},
    },
    response_model=SuccessMessage
)
async def delete_crop(crop_name: str, db: SessionLocal = Depends(get_db)):
    status_code = 200
    content = {}
    error_msg = "Error removing crop information"
        
    try:
        # check if crop exists
        crop_db =  DAOCropValue.get_crop_values_by_crop(db, crop_name)
        if crop_db:
            if not DAOCropValue.delete_crop_info(db, crop_db):
                raise Exception(error_msg)
            else:
                content = {
                    "msg": f"Crop {crop_name} removed successfully"
                }
        else:
            status_code = 404
            content = {
                "msg": f"Crop {crop_name} does not exists"
            }
    except Exception as e:
        status_code = 500
        content = {
            "msg": error_msg
        }

    return JSONResponse(
        status_code = status_code,
        content = content
    )
