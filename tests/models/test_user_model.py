import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from app.models.models import (
    IdentifierModel,
    SymbolIdModel,
    IntervalIdModel,
    SymbolIntervalLimitParamModel,
    TraderSymbolIntervalLimitParamModel,
    AdminModel,
    SymbolModel,
    ChannelIdentifierModel,
    ChannelChangeModel,
    ChannelCreateModel,
    ChannelModel,
    TraderChangeModel,
    TraderCreateModel,
    TraderModel,
    UserChangeModel,
    UserCreateModel,
    UserModel
)
from app.models.enums import IntervalEnum, ChannelTypeEnum, TraderStatusEnum, ExchangeIdEnum, SymbolStatusEnum, TradingTypeEnum
from app.core.config import consts


################## ID models #######################

# Test IdentifierModel
def test_identifier_model():
    data = {"_id": "12345"}
    model = IdentifierModel(**data)
    assert model.id == "12345"


def test_symbol_id_model():
    model = SymbolIdModel(symbol="BTCUSD")
    assert model.symbol == "BTCUSD"

    with pytest.raises(ValidationError):
        SymbolIdModel(symbol="null")  # Should raise validation error

    with pytest.raises(ValidationError):
        SymbolIdModel(symbol="")  # Should raise validation error


def test_interval_id_model():
    model = IntervalIdModel(interval=IntervalEnum.MIN_1)
    assert model.interval == IntervalEnum.MIN_1

################## Param models #######################


def test_symbol_interval_limit_param_model():
    model = SymbolIntervalLimitParamModel(
        symbol="AAPL", interval=IntervalEnum.HOUR_1, limit=100)
    assert model.symbol == "AAPL"
    assert model.interval == IntervalEnum.HOUR_1
    assert model.limit == 100

    model.set_limit(200)
    assert model.limit == 200


def test_trader_symbol_interval_limit_param_model():
    model = TraderSymbolIntervalLimitParamModel(
        trader_id="123", symbol="AAPL", interval=IntervalEnum.HOUR_1, limit=50
    )
    assert model.trader_id == "123"
    assert model.symbol == "AAPL"
    assert model.interval == IntervalEnum.HOUR_1
    assert model.limit == 50

################## Admin Model #######################


def test_admin_model():
    now = datetime.now()
    model = AdminModel(created_at=now, changed_at=now)
    assert model.created_at == now
    assert model.changed_at == now

################## Symbol Model #######################


def test_symbol_model():
    model = SymbolModel(
        symbol="BTC",
        name="Bitcoin",
        status=SymbolStatusEnum.OPEN,
        type=TradingTypeEnum.SPOT,
        currency="USD",
        quote_precision=2,
        trading_fee=0.1,
        trading_time="24/7"
    )
    # Check if description is calculated correctly
    assert model.symbol == "BTC"
    assert model.name == "Bitcoin"
    assert model.description == "Bitcoin (BTC)"
    assert model.status == SymbolStatusEnum.OPEN
    assert model.type == TradingTypeEnum.SPOT
    assert model.currency == "USD"
    assert model.quote_precision == 2
    assert model.trading_fee == 0.1
    assert model.trading_time == "24/7"

    model2 = SymbolModel(
        symbol="BTC",
        name="BTC",
        status=SymbolStatusEnum.OPEN,
        type=TradingTypeEnum.SPOT,
        currency="USD",
        quote_precision=2,
        trading_fee=0.1,
        trading_time="24/7"
    )
    # Check if description is calculated correctly
    assert model2.description == "BTC"

    with pytest.raises(ValidationError):
        SymbolModel(
            symbol="LTC",
            name="Litecoin",
            type=TradingTypeEnum.SPOT,
            currency="USD",
            quote_precision=2,
            trading_fee=0.2,
            trading_time="24/7"
        )

    with pytest.raises(ValidationError):
        SymbolModel(
            symbol="LTC",
            name="Litecoin",
            status=SymbolStatusEnum.OPEN,
            currency="USD",
            quote_precision=2,
            trading_fee=0.2,
            trading_time="24/7"
        )

################## Channel Models #######################


def test_channel_identifier_model():
    data = {
        "type": ChannelTypeEnum.EMAIL,
        "channel": "test@example.com"
    }
    model = ChannelIdentifierModel(**data)
    assert model.type == ChannelTypeEnum.EMAIL
    assert model.channel == "test@example.com"
    assert model.to_mongodb() == {
        consts.MODEL_FIELD_TYPE: "Email",
        consts.MODEL_FIELD_CHANNEL: "test@example.com"
    }


def test_channel_change_model():
    data = {
        "name": "My Channel"
    }
    model = ChannelChangeModel(**data)
    assert model.name == "My Channel"
    assert model.to_mongodb()[consts.MODEL_FIELD_NAME] == "My Channel"


def test_channel_create_model():
    data = {
        "user_id": "user123",
        "type": ChannelTypeEnum.EMAIL,
        "channel": "test@example.com",
        "name": "User Channel"
    }
    model = ChannelCreateModel(**data)
    assert model.user_id == "user123"
    assert model.type == ChannelTypeEnum.EMAIL
    assert model.channel == "test@example.com"
    assert model.name == "User Channel"
    assert model.to_mongodb()[consts.MODEL_FIELD_USER_ID] == "user123"


def test_channel_model():
    data = {
        "_id": "ch123",
        "user_id": "user123",
        "type": ChannelTypeEnum.EMAIL,
        "channel": "test@example.com",
        "name": "User Channel"
    }
    model = ChannelModel(**data)
    assert model.id == "ch123"
    assert model.user_id == "user123"
    assert model.type == ChannelTypeEnum.EMAIL
    assert model.channel == "test@example.com"
    assert model.to_mongodb()[consts.MODEL_FIELD_USER_ID] == "user123"


################## Trader Models #######################

def test_trader_change_model():
    user_id = "user123"
    name = "Trader One"
    expired_datetime = datetime.now() + timedelta(days=365)
    key = 'abc12345'
    data = {
        "user_id": user_id,
        "name": name,
        "api_key": "some_api_key",
        "api_secret": "some_api_secret",
        "expired_dt": expired_datetime
    }
    model = TraderChangeModel(**data)

    assert model.user_id == user_id
    assert model.name == name
    assert model.status == TraderStatusEnum.New
    assert model.expired_dt == expired_datetime

    # Check if the default expired_dt is valid
    assert model.expired_dt > datetime.now()

    with pytest.raises(ValidationError):
        TraderChangeModel(user_id=user_id, name=name, expired_dt=datetime.now(
        ) - timedelta(days=1))  # Invalid expired_dt

    encrypted_key = model.encrypt_key(key=key)
    assert encrypted_key != key
    assert model.decrypt_key(encrypted_key=encrypted_key) == key


def test_trader_create_model():
    data = {
        "user_id": "user123",
        "name": "Trader One",
        "exchange_id": ExchangeIdEnum.bybit_com,
        "api_key": "some_api_key",
        "api_secret": "some_api_secret"
    }
    model = TraderCreateModel(**data)

    assert model.user_id == "user123"
    assert model.name == "Trader One"
    assert model.exchange_id == ExchangeIdEnum.bybit_com
    assert model.to_mongodb_doc(
    )[consts.MODEL_FIELD_EXCHANGE_ID] == ExchangeIdEnum.bybit_com


def test_trader_model():
    data = {
        "_id": "trader123",
        "user_id": "user123",
        "name": "Trader One",
        "exchange_id": ExchangeIdEnum.bybit_com,
        "api_key": "some_api_key",
        "api_secret": "some_api_secret"
    }
    model = TraderModel(**data)

    assert model.id == "trader123"
    assert model.user_id == "user123"
    assert model.name == "Trader One"
    assert model.exchange_id == ExchangeIdEnum.bybit_com


################## User Models #######################

def test_user_change_model():
    data = {
        "first_name": "John",
        "second_name": "Doe",
        "technical_user": True
    }
    model = UserChangeModel(**data)

    assert model.first_name == "John"
    assert model.second_name == "Doe"
    assert model.technical_user is True
    assert model.to_mongodb() == {
        "first_name": "John",
        "second_name": "Doe",
        "technical_user": True,
    }


def test_user_create_model():
    data = {
        "first_name": "Jane",
        "second_name": "Doe",
        "type": ChannelTypeEnum.EMAIL,
        "channel": "jane@example.com"
    }
    model = UserCreateModel(**data)

    assert model.first_name == "Jane"
    assert model.second_name == "Doe"
    assert model.type == ChannelTypeEnum.EMAIL
    assert model.channel == "jane@example.com"


def test_user_model():
    data = {
        "_id": "user123",
        "first_name": "Jane",
        "second_name": "Doe",
        "technical_user": False
    }
    model = UserModel(**data)

    assert model.id == "user123"
    assert model.first_name == "Jane"
    assert model.second_name == "Doe"
    assert model.technical_user is False
