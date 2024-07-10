from typing import List
from app.models.main import UserModel, ChannelModel


class UserComplexModel(UserModel):
    channels: List[ChannelModel]


class ChannelComplexModel(ChannelModel):
    user: UserModel = None
