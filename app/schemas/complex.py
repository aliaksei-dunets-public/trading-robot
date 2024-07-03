from graphene_pydantic import PydanticObjectType
from graphene import List, Field
from app.models.complex import UserComplexModel, ChannelComplexModel
from app.schemas.main import ChannelTypeGrapheneEnum, UserType, ChannelType


class ChannelComplexType(PydanticObjectType):
    class Meta:
        model = ChannelComplexModel
    type = ChannelTypeGrapheneEnum()
    user = UserType

class UserComplexType(PydanticObjectType):
    class Meta:
        model = UserComplexModel

    channels = List(ChannelType)
