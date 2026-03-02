import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        database_url = database_url.replace("postgres://", "postgresql://")
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = (
            "postgresql+psycopg2://postgres:senha@localhost:5432/pipeline_imobiliario"
            "?options=-csearch_path=imobiliario"
        )


config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig
}