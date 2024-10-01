from graphene_pydantic import PydanticObjectType, PydanticInputObjectType
from graphene import Enum
import app.models.main as model
import app.models.enum as enum


ChannelTypeGrapheneEnum = Enum.from_enum(enum.ChannelTypeEnum)
ExchangeIdGrapheneEnum = Enum.from_enum(enum.ExchangeIdEnum)
TraderStatusGrapheneEnum = Enum.from_enum(enum.TraderStatusEnum)


class UserCreateInput(PydanticInputObjectType):
    class Meta:
        model = model.UserCreateModel
    type = ChannelTypeGrapheneEnum()


class UserChangeInput(PydanticInputObjectType):
    class Meta:
        model = model.UserChangeModel


class UserType(PydanticObjectType):
    class Meta:
        model = model.UserModel


class ChannelCreateInput(PydanticInputObjectType):
    class Meta:
        model = model.ChannelCreateModel
    type = ChannelTypeGrapheneEnum()


class ChannelChangeInput(PydanticInputObjectType):
    class Meta:
        model = model.ChannelChangeModel
    type = ChannelTypeGrapheneEnum()


class ChannelType(PydanticObjectType):
    class Meta:
        model = model.ChannelModel
    type = ChannelTypeGrapheneEnum()


class TraderCreateInput(PydanticInputObjectType):
    class Meta:
        model = model.TraderCreateModel
    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()


class TraderChangeInput(PydanticInputObjectType):
    class Meta:
        model = model.TraderChangeModel
    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()


class TraderType(PydanticObjectType):
    class Meta:
        model = model.TraderModel
    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()
