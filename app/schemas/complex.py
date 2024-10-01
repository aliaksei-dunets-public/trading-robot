from graphene_pydantic import PydanticObjectType
from graphene import List
import app.models.complex as model
import app.schemas.main as schema
import app.handlers.handlers as handler


class ChannelComplexType(PydanticObjectType):
    class Meta:
        model = model.ChannelComplexModel

    type = schema.ChannelTypeGrapheneEnum()

    user = schema.UserType

    async def resolve_user(parent, info):
        return await handler.UserHandler().get_user(user_id=parent.user_id)


class TraderComplexType(PydanticObjectType):
    class Meta:
        model = model.TraderComplexModel

    exchange_id = schema.ExchangeIdGrapheneEnum()
    status = schema.TraderStatusGrapheneEnum()

    user = schema.UserType

    async def resolve_user(parent, info):
        return await handler.UserHandler().get_user(user_id=parent.user_id)


class UserComplexType(PydanticObjectType):
    class Meta:
        model = model.UserComplexModel

    channels = List(schema.ChannelType)
    traders = List(schema.TraderType)

    async def resolve_channels(parent, info):
        return await handler.ChannelHandler().get_channels(user_id=parent.id)

    async def resolve_traders(parent, info):
        return await handler.TraderHandler().get_traders(user_id=parent.id)
