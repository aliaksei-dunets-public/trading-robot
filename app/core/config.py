from pydantic import BaseModel, BaseSettings


class Constants(BaseModel):
    DB_COLLECTION_USERS = "users"
    DB_COLLECTION_CHANNELS = "channels"
    DB_COLLECTION_TRADERS = "traders"

    DB_FIELD_ID: str = "_id"
    DB_FIELD_CREATED_AT = "created_at"
    DB_FIELD_CHANGED_AT = "changed_at"

    MODEL_FIELD_USER_ID = "user_id"
    MODEL_FIELD_USER = "user"
    MODEL_FIELD_TYPE = "type"
    MODEL_FIELD_CHANNEL = "channel"
    MODEL_FIELD_CHANNELS = "channels"
    MODEL_FIELD_NAME = "name"
    MODEL_FIELD_EXCHANGE_ID = "exchange_id"
    MODEL_FIELD_STATUS = "status"
    MODEL_FIELD_EXPIRED_DT = "expired_dt"
    MODEL_FIELD_DEFAULT = "default"
    MODEL_FIELD_API_KEY = "api_key"
    MODEL_FIELD_API_SECRET = "api_secret"


class Settings(BaseSettings):
    APP_NAME: str = "Trading Robot API"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "SharedCluster"
    ENCRYPT_OPEN_KEY: str = None

    class Config:
        env_file = ".env"


consts = Constants()
settings = Settings()
