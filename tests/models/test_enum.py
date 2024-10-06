from app.models.enums import ExchangeIdEnum, TraderStatusEnum, TradingTypeEnum, IntervalEnum, ChannelTypeEnum


def test_exchange_id_enum_values():
    assert ExchangeIdEnum.demo_dzengi_com == "DEMO_DZENGI_COM"
    assert ExchangeIdEnum.dzengi_com == "DZENGI_COM"
    assert ExchangeIdEnum.demo_bybit_com == "DEMO_BYBIT_COM"
    assert ExchangeIdEnum.bybit_com == "BYBIT_COM"


def test_exchange_id_enum_docstrings():
    assert ExchangeIdEnum.demo_dzengi_com.__doc__ == "Demo: Dzengi.com"
    assert ExchangeIdEnum.dzengi_com.__doc__ == "Dzengi.com"
    assert ExchangeIdEnum.demo_bybit_com.__doc__ == "Demo: ByBit.com"
    assert ExchangeIdEnum.bybit_com.__doc__ == "ByBit.com"


def test_trader_status_enum_values():
    assert TraderStatusEnum.New == 0
    assert TraderStatusEnum.Public == 1
    assert TraderStatusEnum.Private == 2
    assert TraderStatusEnum.Expired == -1
    assert TraderStatusEnum.Failed == -2


def test_trading_type_enum_values():
    assert TradingTypeEnum.LEVERAGE == "Leverage"
    assert TradingTypeEnum.SPOT == "Spot"


def test_interval_enum_values():
    assert IntervalEnum.MIN_1 == "1m"
    assert IntervalEnum.MIN_3 == "3m"
    assert IntervalEnum.MIN_5 == "5m"
    assert IntervalEnum.MIN_15 == "15m"
    assert IntervalEnum.MIN_30 == "30m"
    assert IntervalEnum.HOUR_1 == "1h"
    assert IntervalEnum.HOUR_2 == "2h"
    assert IntervalEnum.HOUR_4 == "4h"
    assert IntervalEnum.HOUR_6 == "6h"
    assert IntervalEnum.HOUR_12 == "12h"
    assert IntervalEnum.DAY_1 == "1d"
    assert IntervalEnum.WEEK_1 == "1w"
    assert IntervalEnum.MONTH_1 == "1month"


def test_interval_enum_docstrings():
    assert IntervalEnum.MIN_1.__doc__ == "1 Minute"
    assert IntervalEnum.MIN_3.__doc__ == "3 Minutes"
    assert IntervalEnum.MIN_5.__doc__ == "5 Minutes"
    assert IntervalEnum.MIN_15.__doc__ == "15 Minutes"
    assert IntervalEnum.MIN_30.__doc__ == "30 Minutes"
    assert IntervalEnum.HOUR_1.__doc__ == "1 Hour (60 min)"
    assert IntervalEnum.HOUR_2.__doc__ == "2 Hours (120 min)"
    assert IntervalEnum.HOUR_4.__doc__ == "4 Hours (240 min)"
    assert IntervalEnum.HOUR_6.__doc__ == "6 Hours (360 min)"
    assert IntervalEnum.HOUR_12.__doc__ == "12 Hours (720 min)"
    assert IntervalEnum.DAY_1.__doc__ == "1 Day"
    assert IntervalEnum.WEEK_1.__doc__ == "1 Week"
    assert IntervalEnum.MONTH_1.__doc__ == "1 Month"


def test_channel_type_enum_values():
    assert ChannelTypeEnum.EMAIL == "Email"
    assert ChannelTypeEnum.TELEGRAM_BOT == "Telegram"
