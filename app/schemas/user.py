from graphene_pydantic import PydanticObjectType, PydanticInputObjectType
from app.models.user import UserModel, UserModifyModel


class UserInput(PydanticInputObjectType):
    class Meta:
        model = UserModifyModel


class UserType(PydanticObjectType):
    class Meta:
        model = UserModel
