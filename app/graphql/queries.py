import graphene
from app.schemas.complex import UserComplexType, ChannelComplexType
from app.handlers.handlers import UserHandler, ChannelHandler


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserComplexType, user_id=graphene.String(required=True))
    users = graphene.List(UserComplexType)
    channel = graphene.Field(
        ChannelComplexType, channel_id=graphene.String(required=True))
    channels = graphene.List(ChannelComplexType)

    async def resolve_user(parent, info, user_id):
        return await UserHandler().get_user(user_id=user_id)

    async def resolve_users(parent, info):
        return await UserHandler().get_users()

    async def resolve_channel(parent, info, channel_id):
        return await ChannelHandler().get_channel(channel_id=channel_id)

    async def resolve_channels(parent, info):
        return await ChannelHandler().get_channels()
