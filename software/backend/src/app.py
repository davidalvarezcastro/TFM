""" FastApi """
from fastapi import FastAPI

from src.api.routers import crops, models, predict


def create_api():
    # app = FastAPI(dependencies=[Depends(get_query_token)]) # in case of jwt token auth
    app = FastAPI()

    # adding endpoints
    app.include_router(crops.router)
    app.include_router(models.router)
    
    return app

if __name__ == "__main__":
    create_api()