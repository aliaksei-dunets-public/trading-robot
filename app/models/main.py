from app.core.config import consts
from app.models.common import BaseModel, IdentifierModel, AdminModel, ChannelTypeEnum


class ChannelIdentifierModel(BaseModel):
    type: ChannelTypeEnum
    channel: str

    def to_mongodb(self):
        return {
            consts.MODEL_FIELD_TYPE: self.type.value,
            consts.MODEL_FIELD_CHANNEL: self.channel,
        }


class ChannelChangeModel(ChannelIdentifierModel):
    name: str = 'Default Channel'
    type: ChannelTypeEnum
    channel: str

    def to_mongodb(self):
        data = super().to_mongodb()
        data[consts.MODEL_FIELD_NAME] = self.name
        return data


class ChannelCreateModel(ChannelChangeModel):
    user_id: str

    def to_mongodb(self):
        data = super().to_mongodb()
        data[consts.MODEL_FIELD_USER_ID] = self.user_id
        return data


class ChannelModel(IdentifierModel, ChannelCreateModel, AdminModel):
    pass

class UserChangeModel(BaseModel):
    first_name: str
    second_name: str
    technical_user: bool = False

    def to_mongodb(self):
        return {
            "first_name": self.first_name,
            "second_name": self.second_name,
            "technical_user": self.technical_user,
        }


class UserCreateModel(UserChangeModel, ChannelIdentifierModel):
    pass


class UserModel(IdentifierModel, UserChangeModel, AdminModel):
    pass

