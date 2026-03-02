import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # Força o schema public
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"options": "-csearch_path=public"}
    }

class DevelopmentConfig(Config):
    pass

config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig
}