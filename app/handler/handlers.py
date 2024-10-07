from datetime import datetime

from app.core.config import consts
import app.model.models as model
import app.model.enums as enum
from app.db.database import MongoDB
from app.api.common import ApiBase
from app.api.dzengi_com import ApiDzengiCom, ApiDemoDzengiCom


class ExceptionHandler(Exception):
    pass


class BufferBaseHandler:
    def __init__(self):
        self._buffer = {}

    def get_buffer(self) -> dict:
        return self._buffer

    def get_from_buffer(self, key) -> dict:
        if self.is_data_in_buffer(key):
            return self._buffer[key]
        else:
            None

    def is_buffer(self) -> bool:
        return True if self._buffer else False

    def is_data_in_buffer(self, key) -> bool:
        return True if key and key in self._buffer else False

    def set_buffer(self, buffer: dict):
        if buffer:
            self._buffer = buffer

    def set_data_to_buffer(self, key, data: dict):
        self._buffer[key] = data

    def remove_from_buffer(self, key):
        self._buffer.pop(key)

    def clear_buffer(self):
        self._buffer.clear()


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
        self.__trader_id = trader_id
        self.__api: ApiBase = None
        self.__trader_mdl: model.TraderModel = None

    def get_trader_id(self) -> str:
        return self.__trader_id

    async def get_exchange_id(self) -> enum.ExchangeIdEnum:
        trader_mdl = await self.get_trader_model()
        return trader_mdl.exchange_id

    async def get_trader_model(self) -> model.TraderModel:
        if not self.__trader_mdl:
            self.__trader_mdl = await TraderHandler().get_trader(self.__trader_id)

            if not self.__trader_mdl or not self.__trader_mdl.exchange_id:
                raise ExceptionHandler(
                    f"[{self.__class__.__name__}]: __init__ - Exchange Id is missed for Trader: {self.__trader_id}")

        return self.__trader_mdl

    async def get_api(self) -> ApiBase:

        if not self.__api:

            trader_mdl: model.TraderModel = await self.get_trader_model()
            exchange_id = trader_mdl.exchange_id

            if exchange_id == enum.ExchangeIdEnum.dzengi_com:
                self.__api = ApiDzengiCom(trader_mdl)
            elif exchange_id == enum.ExchangeIdEnum.demo_dzengi_com:
                self.__api = ApiDemoDzengiCom(trader_mdl)
            else:
                raise ExceptionHandler(
                    f"[{self.__class__.__name__}]: __init__ - API implementation is missed for Exchange Id: {exchange_id}")

        return self.__api


class SymbolHandler():
    def __init__(self, trader_id: str):
        self.__exchange_handler = ExchangeHandler(trader_id)
        self._buffer_symbols: BufferBaseHandler = singleton_runtime.get_symbol_buffer_handler()
        self._buffer_timeframes: BufferBaseHandler = BufferBaseHandler()

    async def get_symbol(self, symbol: str) -> model.SymbolModel:
        try:
            symbol_model = await self.get_symbols()[symbol]
        except KeyError:
            raise ExceptionHandler(
                f"[{self.__class__.__name__}]: get_symbol - Symbol: {symbol} is not found for Trader: {self.__exchange_handler.get_trader_id()}")
        return symbol_model

    async def get_symbol_fee(self, symbol: str) -> float:
        symbol_mdl = await self.get_symbol(symbol)
        # Try to fetch fee from API and update the buffer
        if not symbol_mdl.trading_fee:
            api = await self.__exchange_handler.get_api()
            trading_fee = await api.get_symbol_fee(symbol)
            symbol_mdl.trading_fee = trading_fee if trading_fee else api.DEFAULT_FEE

        return symbol_mdl.trading_fee

    async def get_symbols(self) -> dict[model.SymbolModel]:
        symbols = {}
        exchange_id = await self.__exchange_handler.get_exchange_id()

        # If buffer data is existing -> get symbols from the buffer
        if self._buffer_symbols.is_data_in_buffer(key=exchange_id):
            #  Get symbols from the buffer
            symbols = self._buffer_symbols.get_from_buffer(key=exchange_id)
        else:
            # Send a request to an API to get symbols
            api = await self.__exchange_handler.get_api()
            symbols = await api.get_symbols()
            # Set fetched symbols to the buffer
            self._buffer_symbols.set_data_to_buffer(
                key=exchange_id, data=symbols)

        return symbols

    async def get_symbol_list(self, **kwargs) -> list[model.SymbolModel]:
        symbol_list = []
        symbol_models = await self.get_symbols()

        symbol = kwargs.get(consts.MODEL_FIELD_SYMBOL, None)
        name = kwargs.get(consts.MODEL_FIELD_NAME, None)
        status = kwargs.get(consts.MODEL_FIELD_STATUS, None)
        type = kwargs.get(consts.MODEL_FIELD_TYPE, None)

        for symbol_model in symbol_models.values():
            if symbol and symbol != symbol_model.symbol:
                continue
            if name and name.lower() not in symbol_model.name.lower():
                continue
            if status and status != symbol_model.status:
                continue
            if type and type != symbol_model.type:
                continue
            else:
                symbol_list.append(symbol_model)

        return sorted(symbol_list, key=lambda x: x.symbol)

    async def is_available(self, interval: enum.IntervalEnum, symbol: str) -> bool:
        pass
        # TODO


class HistoryDataHandler():
    def __init__(self, trader_id: str):
        self._exchange_handler: ExchangeHandler = ExchangeHandler(trader_id)
        self._hd_buffer: BufferBaseHandler = BufferBaseHandler()

    async def get_history_data(self, hd_param: model.HistoryDataParamModel, **kwargs) -> model.HistoryDataModel:
        hd_mdl = None

        api = await self._exchange_handler.get_api()

        buffer_key = self.__get_buffer_key(
            symbol=hd_param.symbol, interval=hd_param.interval)

        # If history data is required from buffer and the buffer data exists -> Check the buffer data
        if hd_param.buffer and self._hd_buffer.is_data_in_buffer(key=buffer_key):
            # Get history data from buffer
            hd_mdl_buffer: model.HistoryDataModel = self._hd_buffer.get_from_buffer(
                buffer_key)

            # Get Current end_datetime for History Data
            current_end_datetime = api.get_end_datetime(
                interval=hd_param.interval, closed=hd_param.closed)

            # If required limit and end_datetime is fitted with buffer history data
            if (hd_param.limit <= hd_mdl_buffer.limit and current_end_datetime and current_end_datetime <= hd_mdl_buffer.end_datetime):
                # Buffered history data Dataframe
                df_buffer = hd_mdl_buffer.data
                # Required DataFrame based on end_datetime
                df_required = df_buffer[df_buffer.index <=
                                        current_end_datetime]
                # Required DataFrame based on limit
                df_required = df_required.tail(hd_param.limit)

                hd_mdl = model.HistoryDataModel(
                    symbol=hd_param.symbol, interval=hd_param.interval, limit=hd_param.limit, data=df_required)

        # If history data from the buffer doesn't exist
        if not hd_mdl:
            # Send a request to an API to get history data
            hd_mdl = await api.get_history_data(hd_param=hd_param)

            # Set fetched history data to the buffer if it's required
            if hd_param.buffer:
                self._hd_buffer.set_buffer(hd_mdl)

        return hd_mdl

    def __get_buffer_key(self, symbol: str, interval: enum.IntervalEnum) -> tuple:
        if not symbol or not interval:
            ExceptionHandler(
                f"[{self.__class__.__name__}]: get_buffer_key - History Data buffer key is invalid: symbol: {
                    symbol}, interval: {interval.value}"
            )

        return (symbol, interval.value)


class SingletonRuntimeHandler:
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)

            class_.__symbol_buffer_handler = BufferBaseHandler()
            # class_.__hd_handler_buffer = BufferBaseHandler()
            # class_.__signal_handler = BufferSingleDictionary()
            # class_.__interval_handler = {}
            # class_.__user_handler = UserHandler()
            # class_.__trader_handler = TraderHandler()
            # class_.__job_handler = BufferSingleDictionary()

        return class_._instance

    def get_symbol_buffer_handler(self) -> BufferBaseHandler:
        return self.__symbol_buffer_handler

    # def get_hd_handler(self, trader_id: str) -> HistoryDataHandler:
    #     hd_handler = self.__hd_handler_buffer.get_from_buffer(key=trader_id)
    #     if not hd_handler:
    #         hd_handler = HistoryDataHandler(trader_id)
    #         self.__hd_handler_buffer.set_data_to_buffer(
    #             key=trader_id, data=hd_handler)

    #     return hd_handler

    def refresh(self):
        self.__symbol_buffer_handler.clear_buffer()
        # self.__hd_handler_buffer.clear_buffer()


singleton_runtime = SingletonRuntimeHandler()
