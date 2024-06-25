from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Trading Robot API"
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "trading_db"

    class Config:
        env_file = ".env"

settings = Settings()