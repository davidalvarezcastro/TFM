# coding: utf-8
from sqlalchemy import Column, Float, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from src.database.mysql import Base

metadata = Base.metadata


class CropValueORM(Base):
    __tablename__ = 'CROP_VALUE'

    crop = Column(String(200), primary_key=True)
    kc = Column(Float, nullable=False, comment='coeficiente único del cultivo')


class ModelTypeORM(Base):
    __tablename__ = 'MODEL_TYPES'

    id = Column(INTEGER(11), primary_key=True)
    description = Column(String(300), comment='breve descripción de lo que implica el nuevo tipo de modelo')


class ModelORM(Base):
    __tablename__ = 'MODELS'

    id = Column(INTEGER(11), primary_key=True)
    description = Column(Text, comment='Breve descripción de los objetivos y finalidades del modelo')
    type = Column(ForeignKey('MODEL_TYPES.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    location = Column(String(500), nullable=False, comment='Indica la localización del modelo en el servidor')

    model_type = relationship('ModelTypeORM')
