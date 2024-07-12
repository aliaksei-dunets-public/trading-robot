from pydantic import BaseModel, BaseSettings


class Constants(BaseModel):
    DB_COLLECTION_USERS = "users"
    DB_COLLECTION_CHANNELS = "channels"

    DB_FIELD_ID: str = "_id"
    DB_FIELD_CREATED_AT = "created_at"
    DB_FIELD_CHANGED_AT = "changed_at"

    MODEL_FIELD_USER_ID = "user_id"
    MODEL_FIELD_USER = "user"
    MODEL_FIELD_TYPE = "type"
    MODEL_FIELD_CHANNEL = "channel"
    MODEL_FIELD_CHANNELS = "channels"
    MODEL_FIELD_NAME = "name"


class Settings(BaseSettings):
    APP_NAME: str = "Trading Robot API"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "SharedCluster"

    class Config:
        env_file = ".env"


consts = Constants()
settings = Settings()
