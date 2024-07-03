from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import datetime

class ChannelTypeEnum(str, Enum):
    EMAIL = "Email"
    TELEGRAM_BOT = "Telegram"

class IdentifierModel(BaseModel):
    id: str = Field(alias="_id", default=None)

    @validator("id", pre=True, always=True)
    def convert_id_to_str(cls, value):
        return str(value)


class AdminModel(BaseModel):
    created_at: datetime = None
    changed_at: datetime = None
