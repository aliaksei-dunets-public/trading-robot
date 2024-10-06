from pydantic import BaseModel
from pydantic_settings import BaseSettings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class Constants(BaseModel):
    DB_COLLECTION_USERS: str = "users"
    DB_COLLECTION_CHANNELS: str = "channels"
    DB_COLLECTION_TRADERS: str = "traders"

    DB_FIELD_ID: str = "_id"
    DB_FIELD_CREATED_AT: str = "created_at"
    DB_FIELD_CHANGED_AT: str = "changed_at"

    MODEL_FIELD_USER_ID: str = "user_id"
    MODEL_FIELD_USER: str = "user"
    MODEL_FIELD_TYPE: str = "type"
    MODEL_FIELD_CHANNEL: str = "channel"
    MODEL_FIELD_CHANNELS: str = "channels"
    MODEL_FIELD_NAME: str = "name"
    MODEL_FIELD_EXCHANGE_ID: str = "exchange_id"
    MODEL_FIELD_STATUS: str = "status"
    MODEL_FIELD_EXPIRED_DT: str = "expired_dt"
    MODEL_FIELD_DEFAULT: str = "default"
    MODEL_FIELD_API_KEY: str = "api_key"
    MODEL_FIELD_API_SECRET: str = "api_secret"
    MODEL_FIELD_SYMBOL: str = "symbol"
    MODEL_FIELD_END_DATETIME: str = "end_datetime"
    MODEL_FIELD_DATA: str = "data"
    MODEL_FIELD_CLOSED: str = "closed"
    MODEL_FIELD_BUFFER: str = "buffer"


class Settings(BaseSettings):
    APP_NAME: str = "Trading Robot API"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "SharedCluster"
    ENCRYPT_OPEN_KEY: str = None

    class Config:
        env_file = ".env"


consts = Constants()
settings = Settings()
