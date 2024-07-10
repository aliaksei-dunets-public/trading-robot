from graphene_pydantic import PydanticObjectType
from graphene import List
from app.models.complex import UserComplexModel, ChannelComplexModel
from app.schemas.main import ChannelTypeGrapheneEnum, UserType, ChannelType
from app.handlers.handlers import UserHandler, ChannelHandler


class ChannelComplexType(PydanticObjectType):
    class Meta:
        model = ChannelComplexModel

    type = ChannelTypeGrapheneEnum()
    user = UserType

    async def resolve_user(parent, info):
        return await UserHandler().get_user(user_id=parent.user_id)


class UserComplexType(PydanticObjectType):
    class Meta:
        model = UserComplexModel

    channels = List(ChannelType)

    async def resolve_channels(parent, info):
        return await ChannelHandler().get_channels(user_id=parent.id)
