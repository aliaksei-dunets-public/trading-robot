from graphene_pydantic import PydanticObjectType, PydanticInputObjectType
from graphene import Enum, List
from app.models.main import ChannelTypeEnum, UserChangeModel, UserCreateModel, UserModel, ChannelModel, ChannelChangeModel, ChannelCreateModel


ChannelTypeGrapheneEnum = Enum.from_enum(ChannelTypeEnum)


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
