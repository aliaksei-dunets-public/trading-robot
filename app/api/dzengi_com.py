import pandas as pd

from app.api.common import ApiBase, ExceptionApi, logger
from app.core.config import consts
import app.model.models as model
import app.model.enums as enum


class ApiDzengiCom(ApiBase):
    """
    A class representing the Dzengi.com API for retrieving historical data from the stock exchange.
    It inherits from the ExchangeApiBase class.
    """

    HEADER_API_KEY_NAME = "X-MBX-APIKEY"

    AGG_TRADES_MAX_LIMIT = 1000
    KLINES_MAX_LIMIT = 1000
    RECV_WINDOW_MAX_LIMIT = 60000

    # Public API Endpoints
    SERVER_TIME_ENDPOINT = "time"
    EXCHANGE_INFORMATION_ENDPOINT = "exchangeInfo"

    # Market data Endpoints
    ORDER_BOOK_ENDPOINT = "depth"
    AGGREGATE_TRADE_LIST_ENDPOINT = "aggTrades"
    KLINES_DATA_ENDPOINT = "klines"
    PRICE_CHANGE_24H_ENDPOINT = "ticker/24hr"

    # Account Endpoints
    ACCOUNT_INFORMATION_ENDPOINT = "account"
    ACCOUNT_TRADE_LIST_ENDPOINT = "myTrades"

    # Order Endpoints
    ORDER_ENDPOINT = "order"
    CURRENT_OPEN_ORDERS_ENDPOINT = "openOrders"
    GET_ORDER_ENDPOINT = "fetchOrder"
    CANCEL_ORDER = "cancelOrder"

    # Leverage Endpoints
    CLOSE_TRADING_POSITION_ENDPOINT = "closeTradingPosition"
    TRADING_POSITIONS_ENDPOINT = "tradingPositions"
    TRADING_POSITIONS_HISTORY_ENDPOINT = "tradingPositionsHistory"
    LEVERAGE_SETTINGS_ENDPOINT = "leverageSettings"
    UPDATE_TRADING_ORDERS_ENDPOINT = "updateTradingOrder"
    UPDATE_TRADING_POSITION_ENDPOINT = "updateTradingPosition"

    PRICE_TYPE_BID = "bid"
    PRICE_TYPE_ASK = "ask"

    TA_API_INTERVAL_1M = "1m"
    TA_API_INTERVAL_5M = "5m"
    TA_API_INTERVAL_15M = "15m"
    TA_API_INTERVAL_30M = "30m"
    TA_API_INTERVAL_1H = "1h"
    TA_API_INTERVAL_4H = "4h"
    TA_API_INTERVAL_1D = "1d"
    TA_API_INTERVAL_1WK = "1w"

    API_FLD_END_TIME = "endTime"

    def get_endpoint(self) -> str:
        return "https://api-adapter.backend.currency.com/api/v2/"

    async def ping_server(self, **kwargs) -> bool:
        try:
            await self._request_async.get(self._get_url(self.SERVER_TIME_ENDPOINT))
            return True
        except ExceptionApi:
            return False

    async def get_symbols(self, **kwargs) -> dict[model.SymbolModel]:
        symbols = {}

        TRADING_FEE_FIELD = "tradingFee"
        EXCHANGE_FEE_FIELD = "exchangeFee"
        QUOTE_ASSET_FIELD = "quoteAsset"

        # Get data about Symbols from API
        response_data = await self._request_async.get(self._get_url(self.EXCHANGE_INFORMATION_ENDPOINT))

        # Create an instance of Symbol and add to the list
        for row in response_data["symbols"]:
            if (
                row[QUOTE_ASSET_FIELD] == "USD"
                and row["assetType"]
                in ["CRYPTOCURRENCY", "EQUITY", "COMMODITY", "CURRENCY"]
                and "REGULAR" in row["marketModes"]
            ):
                # Symbol Status
                status_converted = (
                    enum.SymbolStatusEnum.OPEN
                    if row[consts.MODEL_FIELD_STATUS] == "TRADING"
                    else enum.SymbolStatusEnum.CLOSE
                )

                # Trading Fee
                if TRADING_FEE_FIELD in row and row[TRADING_FEE_FIELD]:
                    trading_fee = row[TRADING_FEE_FIELD]
                elif EXCHANGE_FEE_FIELD in row and row[EXCHANGE_FEE_FIELD]:
                    trading_fee = row[EXCHANGE_FEE_FIELD]
                else:
                    trading_fee = 0

                # Symbol Type
                symbol_type = enum.TradingTypeEnum.LEVERAGE.value if row[
                    "marketType"] == enum.TradingTypeEnum.LEVERAGE.name else enum.TradingTypeEnum.SPOT.value

                symbol_data = {
                    consts.MODEL_FIELD_SYMBOL: row[consts.MODEL_FIELD_SYMBOL],
                    consts.MODEL_FIELD_NAME: row[consts.MODEL_FIELD_NAME],
                    consts.MODEL_FIELD_STATUS: status_converted,
                    consts.MODEL_FIELD_TYPE: symbol_type,
                    "trading_time": row["tradingHours"],
                    "currency": row[QUOTE_ASSET_FIELD],
                    "quote_precision": row["quotePrecision"],
                    "trading_fee": trading_fee,
                }

                symbol_mdl = model.SymbolModel(**symbol_data)

                symbols[symbol_mdl.symbol] = symbol_mdl
            else:
                continue

        return symbols

    async def _get_history_dataframe(self, hd_param: model.HistoryDataParamModel, start=None, end=None, **kwargs) -> model.HistoryDataModel:
        COLUMN_DATETIME_FLOAT = "DatetimeFloat"

        # Prepare URL parameters
        url_params = {
            consts.MODEL_FIELD_SYMBOL: hd_param.symbol,
            consts.MODEL_FIELD_INTERVAL: self._map_interval(interval=hd_param.interval),
            consts.MODEL_FIELD_LIMIT: hd_param.limit,
            self.API_FLD_END_TIME: end,
        }

        # Importing parameters price_type: bid, ask
        # price_type = kwargs.get(Const.FLD_PRICE_TYPE, self.PRICE_TYPE_BID)
        # url_params[Const.API_FLD_PRICE_TYPE] = price_type

        # Get History Data from API
        response_json = await self._request_async.get(self._get_url(self.KLINES_DATA_ENDPOINT), params=url_params)

        # Convert API response to the DataFrame with columns: 'Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'
        df = pd.DataFrame(
            response_json,
            columns=[
                COLUMN_DATETIME_FLOAT,
                consts.API_FIELD_OPEN,
                consts.API_FIELD_HIGH,
                consts.API_FIELD_LOW,
                consts.API_FIELD_CLOSE,
                consts.API_FIELD_VOLUME,
            ],
        )
        df[consts.API_FIELD_DATETIME] = df.apply(
            lambda x: pd.to_datetime(
                self.getDatetimeByUnixTimeMs(x[COLUMN_DATETIME_FLOAT])
            ),
            axis=1,
        )
        df.set_index(consts.API_FIELD_DATETIME, inplace=True)
        df.drop([COLUMN_DATETIME_FLOAT], axis=1, inplace=True)
        df = df.astype(float)

        return df


class ApiDemoDzengiCom(ApiDzengiCom):
    def get_endpoint(self) -> str:
        return "https://demo-api-adapter.backend.currency.com/api/v2/"
