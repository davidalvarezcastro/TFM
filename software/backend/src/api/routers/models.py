""" Gestión de modelos deep learning """

from fastapi import APIRouter

router = APIRouter()

@router.get("/models/", tags=["users"])
async def get_models():
    return [{"username": "Rick"}, {"username": "Morty"}]