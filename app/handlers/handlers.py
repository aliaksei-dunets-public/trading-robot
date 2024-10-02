from app.core.config import consts
import app.models.main as model
import app.models.enum as enum
from app.db.database import MongoDB
from api.common import ApiBase
from api.dzengi_com import ApiDzengiCom, ApiDemoDzengiCom


class ExceptionHandler(Exception):
    pass


class ChannelHandler:
    def __init__(self) -> None:
        self._db = MongoDB(consts.DB_COLLECTION_CHANNELS)

    async def get_channel(self, channel_id: str) -> model.ChannelModel:
        data = await self._db.find_one(channel_id)
        return model.ChannelModel(**data) if data else None

    async def get_channels(self, user_id: str = None, type: enum.ChannelTypeEnum = None) -> list[model.ChannelModel]:
        query = {}
        if user_id:
            query[consts.MODEL_FIELD_USER_ID] = user_id
        if type:
            query[consts.MODEL_FIELD_TYPE] = type
        data = await self._db.find_many(query)
        channels = [model.ChannelModel(**channel) for channel in data]
        return channels if channels else []

    async def create_channel(self, channel: model.ChannelCreateModel) -> model.ChannelModel:
        exist_user = await UserHandler().get_user(channel.user_id)
        if not exist_user:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: create_channel - User: {channel.user_id} is not found")

        channel_dict = channel.to_mongodb()
        created_id = await self._db.insert_one(channel_dict)
        return await self.get_channel(created_id)

    async def update_channel(self, channel_id: str, channel: model.ChannelChangeModel) -> model.ChannelModel:
        exist_channel = await self.get_channel(channel_id)
        if not exist_channel:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: update_channel - Channel: {channel_id} is not found")
        channel_dict = channel.to_mongodb()
        await self._db.update_one(id=channel_id, query=channel_dict)
        return await self.get_channel(channel_id)

    async def delete_channel(self, channel_id: str) -> bool:
        exist_channel = await self.get_channel(channel_id)
        if not exist_channel:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: update_channel - Channel: {channel_id} is not found")
        return await self._db.delete_one(channel_id)

    async def delete_channels_by_user(self, user_id: str) -> bool:
        query = {consts.MODEL_FIELD_USER_ID: user_id}
        result = await self._db.delete_many(query)
        return result


class TraderHandler:
    def __init__(self):
        self._db = MongoDB(consts.DB_COLLECTION_TRADERS)

    async def get_trader(self, trader_id: str) -> model.TraderModel:
        data = await self._db.find_one(trader_id)
        return model.TraderModel(**data) if data else None

    async def get_traders(self, user_id: str = None) -> list[model.TraderModel]:
        query = {}
        if user_id:
            query[consts.MODEL_FIELD_USER_ID] = user_id
        data = await self._db.find_many(query)
        traders = [model.TraderModel(**trader) for trader in data]
        return traders if traders else []

    async def create_trader(self, trader: model.TraderCreateModel) -> model.TraderModel:
        # TODO - add trader checks
        # await self.check_trader_status(trader)

        # TODO - think about encrypting on the model side
        # Encrypt API key and secret before saving to the DB
        if trader.api_key:
            trader.api_key = trader.encrypt_key(key=trader.api_key)
        if trader.api_secret:
            trader.api_secret = trader.encrypt_key(key=trader.api_secret)

        trader_dict = trader.to_mongodb_doc()
        created_id = await self._db.insert_one(trader_dict)
        return await self.get_trader(created_id)

    async def update_trader(self, trader_id: str, trader: model.TraderChangeModel) -> model.TraderModel:
        exist_trader = await self.get_trader(trader_id)
        if not exist_trader:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: update_trader - Trader: {trader_id} is not found")

        # TODO - add trader checks
        # await self.check_trader_status(trader)

        # TODO - think about encrypting on the model side
        # Encrypt API key and secret before saving to the DB
        if trader.api_key:
            trader.api_key = trader.encrypt_key(key=trader.api_key)
        if trader.api_secret:
            trader.api_secret = trader.encrypt_key(key=trader.api_secret)

        trader_dict = trader.to_mongodb_doc()
        await self._db.update_one(trader_id, trader_dict)
        return await self.get_trader(trader_id)

    async def check_trader_status(self, trader: model.TraderModel):
        pass
        # TODO - add trader checks

    async def get_default_trader(self, user_id: str) -> model.TraderModel:
        query = {consts.MODEL_FIELD_USER_ID: user_id,
                 consts.MODEL_FIELD_DEFAULT: True}
        data = await self._db.find_one(query)
        return model.TraderModel(**data) if data else None

    async def delete_trader(self, trader_id: str) -> bool:
        exist_trader = await self.get_trader(trader_id)
        if not exist_trader:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: delete_trader - Trader: {trader_id} is not found")
        return await self._db.delete_one(trader_id)

    async def delete_traders_by_user(self, user_id: str) -> bool:
        return await self._db.delete_many({consts.MODEL_FIELD_USER_ID: user_id})


class UserHandler:
    def __init__(self) -> None:
        self._db = MongoDB(consts.DB_COLLECTION_USERS)

    async def get_user(self, user_id: str) -> model.UserModel:
        data = await self._db.find_one(user_id)
        return model.UserModel(**data) if data else None

    async def get_users(self) -> list[model.UserModel]:
        data = await self._db.find_many()
        users = [model.UserModel(**user) for user in data]
        return users if users else []

    async def create_user(self, user: model.UserCreateModel) -> model.UserModel:
        user_dict = user.to_mongodb()
        created_id = await self._db.insert_one(user_dict)
        channel_mdl = model.ChannelCreateModel(
            user_id=created_id, type=user.type, channel=user.channel)
        await ChannelHandler().create_channel(channel_mdl)
        return await self.get_user(created_id)

    async def update_user(self, user_id: str, user: model.UserChangeModel) -> model.UserModel:
        exist_user = await self.get_user(user_id)
        if not exist_user:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: update_user - User : {user_id} is not found")
        user_dict = user.to_mongodb()
        await self._db.update_one(id=user_id, query=user_dict)
        return await self.get_user(user_id)

    async def delete_user(self, user_id: str) -> bool:
        exist_user = await self.get_user(user_id)
        if not exist_user:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: delete_user - User: {user_id} is not found")

        # First, delete all channels associated with the user
        channels_deleted = await ChannelHandler().delete_channels_by_user(user_id)
        if not channels_deleted:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: delete_user - Failed to delete channels for user: {user_id}")

        # Second, delete all channels associated with the user
        traders_deleted = await TraderHandler().delete_traders_by_user(user_id)
        if not traders_deleted:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: delete_user - Failed to delete traders for user: {user_id}")

        # Then, delete the user
        user_deleted = await self._db.delete_one(user_id)
        return user_deleted


class ExchangeHandler:
    def __init__(self, trader_id: str):
        self.__api: ApiBase = None
        self.__trader_mdl: model.TraderModel = TraderHandler().get_trader(trader_id)

        if not self.__trader_mdl or not self.__trader_mdl.exchange_id:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: __init__ - Exchange Id is missed for Trader: {trader_id}")

    def get_trader_id(self) -> str:
        return self.__trader_mdl.id

    def get_trader_model(self) -> model.TraderModel:
        return self.__trader_mdl

    def get_api(self) -> ApiBase:
        if not self.__api:
            if self.__trader_mdl.exchange_id == enum.ExchangeIdEnum.dzengi_com:
                self.__api = ApiDzengiCom(trader_model=self.__trader_mdl)
            elif self.__trader_mdl.exchange_id == enum.ExchangeIdEnum.demo_dzengi_com:
                self.__api = ApiDemoDzengiCom(trader_model=self.__trader_mdl)
            else:
                raise ExceptionHandler(
                    f"[{self.__class__.__name__}]: __init__ - API implementation is missed for Exchange Id: {self.__trader_mdl.exchange_id}")

        return self.__api


class SymbolHandler():
    def __init__(self, trader_id: str):
        self.__api: ApiBase = ExchangeHandler(trader_id).get_api()

    def get_symbol(self, symbol: str) -> model.SymbolModel:
        # symbol_model = self.get_symbols()[symbol]
        # return symbol_model
        # TODO
        pass

    def get_symbols(self) -> dict[model.SymbolModel]:
        symbols = {}

        # # If buffer data is existing -> get symbols from the buffer
        # if self._buffer_symbols.is_data_in_buffer():
        #     #  Get symbols from the buffer
        #     symbols = self._buffer_symbols.get_buffer()
        # else:
        #     # Send a request to an API to get symbols
        #     symbols = self._exchange_handler.get_symbols()
        #     # Set fetched symbols to the buffer
        #     self._buffer_symbols.set_buffer(symbols)

        symbols = self.__api.get_symbols()

        return symbols
