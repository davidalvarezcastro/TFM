

import typing
from src.database.mysql import SessionLocal
from src.database.models import CropValueORM
from src.models.database import UpdateCropValueSchema


class DAOCropValue():

    @staticmethod
    def get_crop_values(db: SessionLocal) -> typing.List[CropValueORM]:
        return db.query(CropValueORM).all()

    @staticmethod
    def get_crop_values_by_crop(db: SessionLocal, crop: str) -> CropValueORM:
        return db.query(CropValueORM).filter(CropValueORM.crop == crop).first()

    @staticmethod
    def add_crop_info(db: SessionLocal, crop: CropValueORM) -> bool:
        try:
            db.add(crop)
            db.commit()
        except Exception as e:
            return False
        return True

    @staticmethod
    def delete_crop_info(db: SessionLocal, crop: CropValueORM) -> bool:
        try:
            db.delete(crop)
            db.commit()
        except Exception as e:
            return False
        return True

    @staticmethod
    def update_crop_info(db: SessionLocal, crop_name: str, crop: UpdateCropValueSchema) -> bool:
        try:
            db.query(CropValueORM).filter(CropValueORM.crop == crop_name).update(crop.dict())
            db.commit()
        except Exception as e:
            return False
        return True
