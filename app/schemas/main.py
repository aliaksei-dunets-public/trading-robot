from graphene_pydantic import PydanticObjectType, PydanticInputObjectType
from graphene import Enum
from app.models.main import ChannelTypeEnum, ExchangeIdEnum, TraderStatusEnum, UserChangeModel, UserCreateModel, UserModel, ChannelModel, ChannelChangeModel, ChannelCreateModel, TraderModel


ChannelTypeGrapheneEnum = Enum.from_enum(ChannelTypeEnum)
ExchangeIdGrapheneEnum = Enum.from_enum(ExchangeIdEnum)
TraderStatusGrapheneEnum = Enum.from_enum(TraderStatusEnum)


class UserCreateInput(PydanticInputObjectType):
    class Meta:
        model = UserCreateModel
    type = ChannelTypeGrapheneEnum()


class UserChangeInput(PydanticInputObjectType):
    class Meta:
        model = UserChangeModel


class UserType(PydanticObjectType):
    class Meta:
        model = UserModel


class ChannelCreateInput(PydanticInputObjectType):
    class Meta:
        model = ChannelCreateModel
    type = ChannelTypeGrapheneEnum()


class ChannelChangeInput(PydanticInputObjectType):
    class Meta:
        model = ChannelChangeModel
    type = ChannelTypeGrapheneEnum()


class ChannelType(PydanticObjectType):
    class Meta:
        model = ChannelModel
    type = ChannelTypeGrapheneEnum()


class TraderCreateInput(PydanticInputObjectType):
    class Meta:
        model = TraderModel
    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()


class TraderChangeInput(PydanticInputObjectType):
    class Meta:
        model = TraderModel
    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()


class TraderType(PydanticObjectType):
    class Meta:
        model = TraderModel
    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()
