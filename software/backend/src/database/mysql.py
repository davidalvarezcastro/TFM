""" Conector Base de Datos relacional """

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.settings import db_settings


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_settings.USER}:{db_settings.PASSWORD}@{db_settings.HOST}:{db_settings.PORT}/{db_settings.DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
