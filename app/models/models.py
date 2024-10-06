from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator, computed_field
from typing import List
import pandas as pd

from app.core.config import consts
import app.models.enums as enums
from app.utils.helpers import EncryptionTool

################## ID models #######################


class IdentifierModel(BaseModel):
    id: str = Field(alias=consts.DB_FIELD_ID, default=None)

    @field_validator("id", mode="before")
    def convert_id_to_str(cls, value):
        return str(value)


class SymbolIdModel(BaseModel):
    symbol: str

    @field_validator(consts.MODEL_FIELD_SYMBOL)
    def check_symbol(cls, value):
        if not value or value == "null":
            raise ValueError("The symbol is missed")
        return value


class IntervalIdModel(BaseModel):
    interval: enums.IntervalEnum


class TraderIdModel(BaseModel):
    trader_id: str

################## ID models #######################

################## Parameters models #######################


class SymbolIntervalLimitParamModel(SymbolIdModel, IntervalIdModel):
    limit: int = 0

    def set_limit(self, value: int):
        if value:
            self.limit = value


class TraderSymbolIntervalLimitParamModel(TraderIdModel, SymbolIntervalLimitParamModel):
    pass


class HistoryDataParamModel(SymbolIntervalLimitParamModel):
    buffer: bool = True
    closed: bool = False

    @field_validator(consts.MODEL_FIELD_BUFFER, mode="before")
    def convert_buffer(cls, value):
        return cls.convert_to_bool(value)

    @field_validator(consts.MODEL_FIELD_CLOSED, mode="before")
    def convert_closed(cls, value):
        return cls.convert_to_bool(value)

    def convert_to_bool(value):
        if type(value) == bool:
            return value
        elif type(value) == str:
            return bool(value.lower() == "true")

################## Parameters models #######################


################## Main models #############################
class AdminModel(BaseModel):
    created_at: datetime = None
    changed_at: datetime = None


class SymbolModel(SymbolIdModel):
    name: str
    status: enums.SymbolStatusEnum
    type: enums.TradingTypeEnum
    currency: str
    quote_precision: int
    trading_fee: float = None
    trading_time: str

    # Comptuted field for description
    @computed_field
    def description(self) -> str:
        if self.name and self.name != self.symbol:
            return f'{self.name} ({self.symbol})'
        else:
            return self.symbol


class HistoryDataModel(SymbolIntervalLimitParamModel):
    data: pd.DataFrame

    # Comptuted field for END_DATETIME calculated form History DataFrame
    @computed_field
    def end_datetime(self) -> datetime:
        return self.data.index[-1]

    class Config:
        # This is a workaround for DataFrame type
        arbitrary_types_allowed = True


class ChannelIdentifierModel(BaseModel):
    type: enums.ChannelTypeEnum
    channel: str

    def to_mongodb(self):
        return {
            consts.MODEL_FIELD_TYPE: self.type.value,
            consts.MODEL_FIELD_CHANNEL: self.channel,
        }


class ChannelChangeModel(BaseModel):
    name: str

    def to_mongodb(self):
        return {
            consts.MODEL_FIELD_NAME: self.name
        }


class ChannelCreateModel(ChannelIdentifierModel):
    user_id: str
    name: str

    def to_mongodb(self):
        data = super().to_mongodb()
        data[consts.MODEL_FIELD_USER_ID] = self.user_id
        data[consts.MODEL_FIELD_NAME] = self.name
        return data


class ChannelModel(IdentifierModel, ChannelCreateModel, AdminModel):
    pass


class TraderChangeModel(BaseModel):
    user_id: str
    name: str
    status: enums.TraderStatusEnum = enums.TraderStatusEnum.New
    expired_dt: datetime = datetime.now() + timedelta(days=365)
    default: bool = True
    api_key: str = ""
    api_secret: str = ""

    @field_validator(consts.MODEL_FIELD_EXPIRED_DT)
    def check_expired_dt(cls, value_dt):
        if value_dt <= datetime.now():
            raise ValueError("The expired datetime is invalid")
        return value_dt

    def encrypt_key(self, key, user_token=None):
        return EncryptionTool.encrypt_key(self.user_id, key, user_token)

    def decrypt_key(self, encrypted_key, user_token=None):
        return EncryptionTool.decrypt_key(self.user_id, encrypted_key, user_token)

    def to_mongodb(self):
        return {
            consts.MODEL_FIELD_NAME: self.name,
            consts.MODEL_FIELD_STATUS: self.status,
            consts.MODEL_FIELD_EXPIRED_DT: self.expired_dt,
            consts.MODEL_FIELD_DEFAULT: self.default,
            consts.MODEL_FIELD_API_KEY: self.api_key,
            consts.MODEL_FIELD_API_SECRET: self.api_secret,
        }


class TraderCreateModel(TraderChangeModel):
    exchange_id: enums.ExchangeIdEnum

    def to_mongodb_doc(self):
        data = super().to_mongodb()
        data[consts.MODEL_FIELD_USER_ID] = self.user_id
        data[consts.MODEL_FIELD_EXCHANGE_ID] = self.exchange_id
        return data


class TraderModel(IdentifierModel, TraderCreateModel, AdminModel):
    pass


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

################## Main models #############################

################## Complex models ##########################


class UserComplexModel(UserModel):
    channels: List[ChannelModel]
    traders: List[TraderModel]


class ChannelComplexModel(ChannelModel):
    user: UserModel = None


class TraderComplexModel(TraderModel):
    user: UserModel = None
################## Complex models ##########################
