from graphene_pydantic import PydanticObjectType, PydanticInputObjectType
from graphene import Enum, List

import app.models.models as models
import app.models.enums as enums
import app.handler.handlers as handler

ChannelTypeGrapheneEnum = Enum.from_enum(enums.ChannelTypeEnum)
ExchangeIdGrapheneEnum = Enum.from_enum(enums.ExchangeIdEnum)
TraderStatusGrapheneEnum = Enum.from_enum(enums.TraderStatusEnum)
SymbolStatusGrapheneEnum = Enum.from_enum(enums.SymbolStatusEnum)
TradingTypeGrapheneEnum = Enum.from_enum(enums.TradingTypeEnum)


class SymbolType(PydanticObjectType):
    class Meta:
        model = models.SymbolModel
    status = SymbolStatusGrapheneEnum()
    type = TradingTypeGrapheneEnum()


class UserCreateInput(PydanticInputObjectType):
    class Meta:
        model = models.UserCreateModel
    type = ChannelTypeGrapheneEnum()


class UserChangeInput(PydanticInputObjectType):
    class Meta:
        model = models.UserChangeModel


class UserType(PydanticObjectType):
    class Meta:
        model = models.UserModel


class ChannelCreateInput(PydanticInputObjectType):
    class Meta:
        model = models.ChannelCreateModel
    type = ChannelTypeGrapheneEnum()


class ChannelChangeInput(PydanticInputObjectType):
    class Meta:
        model = models.ChannelChangeModel
    type = ChannelTypeGrapheneEnum()


class ChannelType(PydanticObjectType):
    class Meta:
        model = models.ChannelModel
    type = ChannelTypeGrapheneEnum()


class TraderCreateInput(PydanticInputObjectType):
    class Meta:
        model = models.TraderCreateModel
    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()


class TraderChangeInput(PydanticInputObjectType):
    class Meta:
        model = models.TraderChangeModel
    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()


class TraderType(PydanticObjectType):
    class Meta:
        model = models.TraderModel
    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()


class ChannelComplexType(PydanticObjectType):
    class Meta:
        model = models.ChannelComplexModel

    type = ChannelTypeGrapheneEnum()

    user = UserType

    async def resolve_user(parent, info):
        return await handler.UserHandler().get_user(user_id=parent.user_id)


class TraderComplexType(PydanticObjectType):
    class Meta:
        model = models.TraderComplexModel

    exchange_id = ExchangeIdGrapheneEnum()
    status = TraderStatusGrapheneEnum()

    user = UserType

    async def resolve_user(parent, info):
        return await handler.UserHandler().get_user(user_id=parent.user_id)


class UserComplexType(PydanticObjectType):
    class Meta:
        model = models.UserComplexModel

    channels = List(ChannelType)
    traders = List(TraderType)

    async def resolve_channels(parent, info):
        return await handler.ChannelHandler().get_channels(user_id=parent.id)

    async def resolve_traders(parent, info):
        return await handler.TraderHandler().get_traders(user_id=parent.id)
