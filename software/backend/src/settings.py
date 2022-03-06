""" Archivo con variables de configuración """
import os


class SettingsModels:
    FILES_FOLDER: str = './data/raw/'

class SettingsDatabase:
    HOST: str = os.getenv('DB_HOST', 'localhost')
    PORT: int = int(os.getenv('DB_PORT', 3306))
    USER: str = os.getenv('DB_USER', 'user')
    PASSWORD: str = os.getenv('DB_PASS', 'sercret')
    ROOT_USER: str = os.getenv('DB_ROOT_USER', 'admin')
    ROOT_PASSWORD: str = os.getenv('DB_ROOT_PASS', 'sercret')
    DATABASE: str = os.getenv('DB_DATABASE', 'cool_database')


models_settings = SettingsModels()
db_settings = SettingsDatabase()
