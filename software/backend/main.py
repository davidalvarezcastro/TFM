"""
Backend entry file (using bt docker-compose file)
    - init database
    - deploy fastapi services

https://github.com/davidalvarezcastro/
"""
from src.app import create_api
from src.database.mysql import Base, engine

# init database
Base.metadata.create_all(bind=engine)

# init api
app = create_api()
