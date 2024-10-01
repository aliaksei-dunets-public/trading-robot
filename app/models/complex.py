from typing import List
import app.models.main as model


class UserComplexModel(model.UserModel):
    channels: List[model.ChannelModel]
    traders: List[model.TraderModel]


class ChannelComplexModel(model.ChannelModel):
    user: model.UserModel = None


class TraderComplexModel(model.TraderModel):
    user: model.UserModel = None
