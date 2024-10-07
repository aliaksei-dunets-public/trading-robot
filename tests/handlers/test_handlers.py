import pytest
from unittest.mock import AsyncMock, patch
from bson import ObjectId
from app.core.config import consts
import app.model.models as model
import app.model.enums as enum
from app.db.database import MongoDB
from app.api.dzengi_com import ApiDzengiCom, ApiDemoDzengiCom
from app.handler.handlers import BufferBaseHandler, ChannelHandler, TraderHandler, UserHandler, ExchangeHandler, SymbolHandler, HistoryDataHandler, ExceptionHandler


# Sample buffer data for mocking
MOCK_BUFFER_DATA = {"key1": {"data": "sample_data"}}


### BufferBaseHandler Unit Tests ###

def test_buffer_base_handler():
    buffer_handler = BufferBaseHandler()

    # Test initial empty buffer
    assert buffer_handler.get_buffer() == {}

    # Test setting buffer data
    buffer_handler.set_buffer({"key": "value"})
    assert buffer_handler.get_buffer() == {"key": "value"}

    # Test checking if data is in buffer
    assert buffer_handler.is_data_in_buffer("key") == True
    assert buffer_handler.is_data_in_buffer("missing_key") == False

    # Test setting data to buffer
    buffer_handler.set_data_to_buffer("new_key", {"some": "data"})
    assert buffer_handler.get_from_buffer("new_key") == {"some": "data"}

    # Test removing from buffer
    buffer_handler.remove_from_buffer("new_key")
    assert buffer_handler.get_from_buffer("new_key") == None

    # Test clearing buffer
    buffer_handler.clear_buffer()
    assert buffer_handler.get_buffer() == {}


### ChannelHandler Unit Tests ###

@pytest.mark.asyncio
async def test_channel_handler(monkeypatch):
    channel_id = ObjectId()
    channel_name = "test_channel"
    channel_type = enum.ChannelTypeEnum.EMAIL
    channel = "test@example.com"
    user_id = "123456789"

    mock_channel_data = {
        consts.DB_FIELD_ID: channel_id,
        consts.MODEL_FIELD_NAME: channel_name,
        consts.MODEL_FIELD_TYPE: channel_type,
        consts.MODEL_FIELD_CHANNEL: channel,
        consts.MODEL_FIELD_USER_ID: user_id,
    }

    channel_handler = ChannelHandler()

    monkeypatch.setattr(channel_handler._db, "find_one",
                        AsyncMock(return_value=mock_channel_data))
    monkeypatch.setattr(channel_handler._db, "find_many",
                        AsyncMock(return_value=[mock_channel_data]))
    monkeypatch.setattr(channel_handler._db, "insert_one",
                        AsyncMock(return_value=channel_id))

    # Test get_channel
    channel = await channel_handler.get_channel(channel_id)
    assert channel.name == channel_name

    # Test get_channels
    channels = await channel_handler.get_channels(user_id=user_id)
    assert len(channels) == 1

    # Test create_channel - exception case if user not found
    with patch('app.handler.handlers.UserHandler.get_user', return_value=None):
        with pytest.raises(ExceptionHandler):
            await channel_handler.create_channel(model.ChannelCreateModel(**mock_channel_data))

    # Test create_channel - valid case
    with patch('app.handler.handlers.UserHandler.get_user', return_value=mock_channel_data):
        created_channel = await channel_handler.create_channel(model.ChannelCreateModel(**mock_channel_data))
        assert created_channel.id == str(channel_id)

    # Test update_channel - invalid channel case
    with patch('app.handler.handlers.ChannelHandler.get_channel', return_value=None):
        with pytest.raises(ExceptionHandler):
            await channel_handler.update_channel("non_existing_id", model.ChannelChangeModel(**mock_channel_data))

    # Test delete_channel - invalid channel case
    with patch('app.handler.handlers.ChannelHandler.get_channel', return_value=None):
        with pytest.raises(ExceptionHandler):
            await channel_handler.delete_channel("non_existing_id")


# ### TraderHandler Unit Tests ###

# @pytest.mark.asyncio
# @patch('app.db.database.MongoDB')
# async def test_trader_handler(mock_db):
#     mock_db.return_value.find_one = AsyncMock(
#         return_value={"_id": "trader123", "name": "test_trader"})
#     mock_db.return_value.find_many = AsyncMock(
#         return_value=[{"_id": "trader123", "name": "test_trader"}])
#     mock_db.return_value.insert_one = AsyncMock(return_value="trader123")

#     trader_handler = TraderHandler()

#     # Test get_trader
#     trader = await trader_handler.get_trader("trader123")
#     assert trader.name == "test_trader"

#     # Test get_traders
#     traders = await trader_handler.get_traders(user_id="user123")
#     assert len(traders) == 1

#     # Test create_trader - invalid case
#     with patch('app.handler.handlers.TraderHandler.get_trader', return_value=None):
#         created_trader = await trader_handler.create_trader(models.TraderCreateModel(user_id="user123", name="new_trader"))
#         assert created_trader._id == "trader123"


# ### UserHandler Unit Tests ###

# @pytest.mark.asyncio
# @patch('app.db.database.MongoDB')
# async def test_user_handler(mock_db):
#     mock_db.return_value.find_one = AsyncMock(
#         return_value={"_id": "user123", "name": "test_user"})
#     mock_db.return_value.insert_one = AsyncMock(return_value="user123")

#     user_handler = UserHandler()

#     # Test get_user
#     user = await user_handler.get_user("user123")
#     assert user.name == "test_user"

#     # Test create_user
#     with patch('app.handler.handlers.ChannelHandler.create_channel', AsyncMock(return_value="channel123")):
#         created_user = await user_handler.create_user(models.UserCreateModel(name="new_user"))
#         assert created_user._id == "user123"


# ### ExchangeHandler Unit Tests ###

# @pytest.mark.asyncio
# @patch('app.db.database.MongoDB')
# async def test_exchange_handler(mock_db):
#     mock_db.return_value.find_one = AsyncMock(
#         return_value={"_id": "trader123", "exchange_id": enums.ExchangeIdEnum.dzengi_com})

#     exchange_handler = ExchangeHandler("trader123")

#     # Test get_trader_id
#     assert exchange_handler.get_trader_id() == "trader123"

#     # Test get_exchange_id
#     exchange_id = await exchange_handler.get_exchange_id()
#     assert exchange_id == enums.ExchangeIdEnum.dzengi_com


# ### SymbolHandler Unit Tests ###

# @pytest.mark.asyncio
# @patch('app.db.database.MongoDB')
# async def test_symbol_handler(mock_db):
#     mock_db.return_value.find_one = AsyncMock(
#         return_value={"_id": "symbol123", "name": "BTC/USD"})
#     symbol_handler = SymbolHandler("trader123")

#     # Test get_symbol_fee
#     with patch('app.handler.handlers.SymbolHandler.get_symbol', AsyncMock(return_value=models.SymbolModel(symbol="BTC/USD", trading_fee=None))):
#         fee = await symbol_handler.get_symbol_fee("BTC/USD")
#         assert fee is not None


# ### HistoryDataHandler Unit Tests ###

# @pytest.mark.asyncio
# @patch('app.db.database.MongoDB')
# async def test_history_data_handler(mock_db):
#     history_handler = HistoryDataHandler("trader123")

#     # Test get_history_data
#     with patch('app.api.dzengi_com.ApiDzengiCom.get_history_data', AsyncMock(return_value=models.HistoryDataModel(symbol="BTC/USD", interval=enums.IntervalEnum.ONE_MINUTE))):
#         data = await history_handler.get_history_data(models.HistoryDataParamModel(symbol="BTC/USD", interval=enums.IntervalEnum.ONE_MINUTE, limit=100, buffer=True))
#         assert data.symbol == "BTC/USD"
