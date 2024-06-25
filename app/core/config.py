from pydantic import BaseModel, BaseSettings


class Constants(BaseModel):
    DB_COLLECTION_USERS = "users"

    DB_FIELD_ID: str = "_id"
    DB_FIELD_CREATED_AT = "created_at"
    DB_FIELD_CHANGED_AT = "changed_at"


class Settings(BaseSettings):
    APP_NAME: str = "Trading Robot API"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "trading_db"

    class Config:
        env_file = ".env"


consts = Constants()
settings = Settings()
