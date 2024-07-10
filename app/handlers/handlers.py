from app.models.main import ChannelTypeEnum, UserModel, UserChangeModel, UserCreateModel, ChannelModel, ChannelChangeModel, ChannelCreateModel
from app.models.complex import UserComplexModel, ChannelComplexModel
from app.db.database import MongoDB
from app.core.config import consts


class ChannelHandler:
    def __init__(self) -> None:
        self._db = MongoDB(consts.DB_COLLECTION_CHANNELS)

    async def get_channel(self, channel_id: str) -> ChannelModel:
        data = await self._db.find_one(channel_id)
        return ChannelModel(**data) if data else None
    
    async def get_channels(self, user_id: str = None, type: ChannelTypeEnum = None) -> list[ChannelModel]:
        query = {}
        if user_id:
            query[consts.MODEL_FIELD_USER_ID] = user_id
        if type:
            query[consts.MODEL_FIELD_TYPE] = type
        data = await self._db.find_many(query)
        channels = [ChannelModel(**channel) for channel in data]
        return channels if channels else []

    async def create_channel(self, channel: ChannelCreateModel) -> ChannelModel:
        channel_dict = channel.to_mongodb()
        created_id = await self._db.insert_one(channel_dict)
        return await self.get_channel(created_id)

    async def update_channel(self, channel_id: str, channel: ChannelChangeModel) -> ChannelModel:
        exist_channel = await self.get_channel(channel_id)
        if not exist_channel:
            raise Exception(
                f"[{self.__class__.__name__}]: update_channel - Channel {channel_id} is not found")
        channel_dict = channel.to_mongodb()
        await self._db.update_one(id=channel_id, query=channel_dict)
        return await self.get_channel(channel_id)

    async def delete_channel(self, channel_id: str) -> bool:
        return await self._db.delete_one(channel_id)


class UserHandler:
    def __init__(self) -> None:
        self._db = MongoDB(consts.DB_COLLECTION_USERS)

    async def get_user(self, user_id: str) -> UserModel:
        data = await self._db.find_one(user_id)
        return UserModel(**data) if data else None

    async def get_users(self) -> list[UserModel]:
        data = await self._db.find_many()
        users = [UserModel(**user) for user in data]
        return users if users else []

    async def create_user(self, user: UserCreateModel) -> UserModel:
        user_dict = user.to_mongodb()
        created_id = await self._db.insert_one(user_dict)
        channel_mdl = ChannelCreateModel(
            user_id=created_id, type=user.type, channel=user.channel)
        await ChannelHandler().create_channel(channel_mdl)
        return await self.get_user(created_id)

    async def update_user(self, user_id: str, user: UserChangeModel) -> UserModel:
        exist_user = await self.get_user(user_id)
        if not exist_user:
            raise Exception(
                f"[{self.__class__.__name__}]: update_user - User {user_id} is not found")
        user_dict = user.to_mongodb()
        await self._db.update_one(id=user_id, query=user_dict)
        return await self.get_user(user_id)

    async def delete_user(self, user_id: str) -> bool:
        return await self._db.delete_one(user_id)
