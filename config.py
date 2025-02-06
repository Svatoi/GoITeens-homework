import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig:
    """Базова конфігурація"""

    APP_NAME = os.getenv("APP_NAME", "Topchik")
    SECRET_KEY = os.getenv("SECRET_KEY", "Вап, секретного ключа тут немає, ХА-ХА!")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
    DEBUG_TB_ENABLED = False
    WTF_CSRF_ENABLED = False

    @staticmethod
    def configure(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(BASE_DIR, "development.sqlite3"),
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(BASE_DIR, "production.sqlite3"),
    )


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}