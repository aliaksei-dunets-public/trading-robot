from datetime import datetime, timedelta
from pydantic import BaseModel, Field, validator

from app.core.config import consts
import app.models.enum as enum
from app.utils.helpers import EncryptionTool

################## ID models #######################


class IdentifierModel(BaseModel):
    id: str = Field(alias="_id", default=None)

    @validator("id", pre=True, always=True)
    def convert_id_to_str(cls, value):
        return str(value)


class SymbolIdModel(BaseModel):
    symbol: str

    @validator("symbol")
    def check_symbol(cls, value):
        if not value or value == "null":
            raise ValueError("The symbol is missed")
        return value


class IntervalIdModel(BaseModel):
    interval: enum.IntervalEnum
################## ID models #######################


class AdminModel(BaseModel):
    created_at: datetime = None
    changed_at: datetime = None


class ChannelIdentifierModel(BaseModel):
    type: enum.ChannelTypeEnum
    channel: str

    def to_mongodb(self):
        return {
            consts.MODEL_FIELD_TYPE: self.type.value,
            consts.MODEL_FIELD_CHANNEL: self.channel,
        }


class ChannelChangeModel(ChannelIdentifierModel):
    name: str = 'Default Channel'
    type: enum.ChannelTypeEnum
    channel: str

    def to_mongodb(self):
        data = super().to_mongodb()
        data[consts.MODEL_FIELD_NAME] = self.name
        return data


class ChannelCreateModel(ChannelChangeModel):
    user_id: str

    def to_mongodb(self):
        data = super().to_mongodb()
        data[consts.MODEL_FIELD_USER_ID] = self.user_id
        return data


class ChannelModel(IdentifierModel, ChannelCreateModel, AdminModel):
    pass


class TraderModel(IdentifierModel, AdminModel):
    user_id: str
    exchange_id: enum.ExchangeIdEnum
    name: str
    status: enum.TraderStatusEnum = enum.TraderStatusEnum.New
    expired_dt: datetime = datetime.now() + timedelta(days=365)
    default: bool = True
    api_key: str = ""
    api_secret: str = ""

    @validator("expired_dt")
    def check_expired_dt(cls, value_dt):
        if value_dt <= datetime.now():
            raise ValueError("The expired datetime is invalid")
        return value_dt

    def encrypt_key(self, key, user_token=None):
        return EncryptionTool.encrypt_key(self.user_id, key, user_token)

    def decrypt_key(self, encrypted_key, user_token=None):
        return EncryptionTool.decrypt_key(self.user_id, encrypted_key, user_token)

    def to_mongodb_doc(self):
        return {
            consts.MODEL_FIELD_USER_ID: self.user_id,
            consts.MODEL_FIELD_EXCHANGE_ID: self.exchange_id,
            consts.MODEL_FIELD_NAME: self.name,
            consts.MODEL_FIELD_STATUS: self.status,
            consts.MODEL_FIELD_EXPIRED_DT: self.expired_dt,
            consts.MODEL_FIELD_DEFAULT: self.default,
            consts.MODEL_FIELD_API_KEY: self.api_key,
            consts.MODEL_FIELD_API_SECRET: self.api_secret,
        }


class UserChangeModel(BaseModel):
    first_name: str
    second_name: str
    technical_user: bool = False

    def to_mongodb(self):
        return {
            "first_name": self.first_name,
            "second_name": self.second_name,
            "technical_user": self.technical_user,
        }


class UserCreateModel(UserChangeModel, ChannelIdentifierModel):
    pass


class UserModel(IdentifierModel, UserChangeModel, AdminModel):
    pass
