from graphene_pydantic import PydanticObjectType, PydanticInputObjectType
from graphene import Enum, List

import app.models.main as model
import app.models.enum as enum
import app.handlers.handlers as handler

ChannelTypeGrapheneEnum = Enum.from_enum(enum.ChannelTypeEnum)
ExchangeIdGrapheneEnum = Enum.from_enum(enum.ExchangeIdEnum)
TraderStatusGrapheneEnum = Enum.from_enum(enum.TraderStatusEnum)
SymbolStatusGrapheneEnum = Enum.from_enum(enum.SymbolStatusEnum)
TradingTypeGrapheneEnum = Enum.from_enum(enum.TradingTypeEnum)


class SymbolType(PydanticObjectType):
    class Meta:
        model = model.SymbolModel
    status = SymbolStatusGrapheneEnum()
    type = TradingTypeGrapheneEnum()


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


class ChannelComplexType(PydanticObjectType):
    class Meta:
        model = model.ChannelComplexModel

    type = ChannelTypeGrapheneEnum()

    user = UserType

    async def resolve_user(parent, info):
        return await handler.UserHandler().get_user(user_id=parent.user_id)


class TraderComplexType(PydanticObjectType):
    class Meta:
        model = model.TraderComplexModel

    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()

    user = UserType

    async def resolve_user(parent, info):
        return await handler.UserHandler().get_user(user_id=parent.user_id)


class UserComplexType(PydanticObjectType):
    class Meta:
        model = model.UserComplexModel

    channels = List(ChannelType)
    traders = List(TraderType)

    async def resolve_channels(parent, info):
        return await handler.ChannelHandler().get_channels(user_id=parent.id)

    async def resolve_traders(parent, info):
        return await handler.TraderHandler().get_traders(user_id=parent.id)
