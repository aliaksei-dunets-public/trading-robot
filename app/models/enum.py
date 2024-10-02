from enum import Enum


class ExchangeIdEnum(str, Enum):
    demo_dzengi_com = "DEMO_DZENGI_COM"
    dzengi_com = "DZENGI_COM"
    demo_bybit_com = "DEMO_BYBIT_COM"
    bybit_com = "BYBIT_COM"


ExchangeIdEnum.demo_dzengi_com.__doc__ = "Demo: Dzengi.com"
ExchangeIdEnum.dzengi_com.__doc__ = "Dzengi.com"
ExchangeIdEnum.demo_bybit_com.__doc__ = "Demo: ByBit.com"
ExchangeIdEnum.bybit_com.__doc__ = "ByBit.com"


class TraderStatusEnum(int, Enum):
    New = 0
    Public = 1
    Private = 2
    Expired = -1
    Failed = -2


class TradingTypeEnum(str, Enum):
    LEVERAGE = "Leverage"
    SPOT = "Spot"


class IntervalEnum(str, Enum):
    MIN_1 = "1m"            # 1 minute
    MIN_3 = "3m"            # 3 minutes
    MIN_5 = "5m"            # 5 minutes
    MIN_15 = "15m"          # 15 minutes
    MIN_30 = "30m"          # 30 minutes
    HOUR_1 = "1h"           # 1 hour
    HOUR_2 = "2h"           # 2 hours
    HOUR_4 = "4h"           # 4 hours
    HOUR_6 = "6h"           # 6 hours
    HOUR_12 = "12h"         # 12 hours
    DAY_1 = "1d"            # 1 day
    WEEK_1 = "1w"           # 1 week
    MONTH_1 = "1month"      # 1 month


IntervalEnum.MIN_1.__doc__ = "1 Minute"
IntervalEnum.MIN_3.__doc__ = "3 Minutes"
IntervalEnum.MIN_5.__doc__ = "5 Minutes"
IntervalEnum.MIN_15.__doc__ = "15 Minutes"
IntervalEnum.MIN_30.__doc__ = "30 Minutes"
IntervalEnum.HOUR_1.__doc__ = "1 Hour (60 min)"
IntervalEnum.HOUR_2.__doc__ = "2 Hours (120 min)"
IntervalEnum.HOUR_4.__doc__ = "4 Hours (240 min)"
IntervalEnum.HOUR_6.__doc__ = "6 Hours (360 min)"
IntervalEnum.HOUR_12.__doc__ = "12 Hours (720 min)"
IntervalEnum.DAY_1.__doc__ = "1 Day"
IntervalEnum.WEEK_1.__doc__ = "1 Week"
IntervalEnum.MONTH_1.__doc__ = "1 Month"


class ChannelTypeEnum(str, Enum):
    EMAIL = "Email"
    TELEGRAM_BOT = "Telegram"
