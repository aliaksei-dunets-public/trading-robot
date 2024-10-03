import requests
import json

from app.api.common import ApiBase, ExceptionApi, logger
from app.core.config import consts
import app.models.main as model
import app.models.enum as enum


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

    def get_endpoint(self) -> str:
        return "https://api-adapter.backend.currency.com/api/v2/"

    def ping_server(self, **kwargs) -> bool:
        response = requests.get(self._get_url(self.SERVER_TIME_ENDPOINT))

        if response.status_code == 200:
            return True
        else:
            logger.error(
                f"[{self.__class__.__name__}]: ping_server - {self._trader_model.exchange_id.value} -> {response.text}")
            return False

    def get_symbols(self, **kwargs) -> dict[model.SymbolModel]:
        symbols = {}

        TRADING_FEE_FIELD = "tradingFee"
        EXCHANGE_FEE_FIELD = "exchangeFee"
        QUOTE_ASSET_FIELD = "quoteAsset"

        # TODO
        # if config.get_config_value(Const.CONF_PROPERTY_API_LOG):
        #     logger.info(
        #         f"ExchangeApiBase: {
        #             self._trader_model.exchange_id.value} - getSymbols()"
        #     )

        # Get data about Symbols from API
        response = requests.get(self._get_url(
            self.EXCHANGE_INFORMATION_ENDPOINT))

        if response.status_code == 200:
            json_api_response = json.loads(response.text)

            # Create an instance of Symbol and add to the list
            for row in json_api_response["symbols"]:
                if (
                    row[QUOTE_ASSET_FIELD] == "USD"
                    and row["assetType"]
                    in ["CRYPTOCURRENCY", "EQUITY", "COMMODITY", "CURRENCY"]
                    and "REGULAR" in row["marketModes"]
                ):
                    status_converted = (
                        enum.SymbolStatusEnum.OPEN
                        if row[consts.MODEL_FIELD_STATUS] == "TRADING"
                        else enum.SymbolStatusEnum.CLOSE
                    )

                    if TRADING_FEE_FIELD in row and row[TRADING_FEE_FIELD]:
                        trading_fee = row[TRADING_FEE_FIELD]
                    elif EXCHANGE_FEE_FIELD in row and row[EXCHANGE_FEE_FIELD]:
                        trading_fee = row[EXCHANGE_FEE_FIELD]
                    else:
                        trading_fee = 0

                    symbol_data = {
                        consts.MODEL_FIELD_SYMBOL: row[consts.MODEL_FIELD_SYMBOL],
                        consts.MODEL_FIELD_NAME: row[consts.MODEL_FIELD_NAME],
                        consts.MODEL_FIELD_STATUS: status_converted,
                        consts.MODEL_FIELD_TYPE: row["marketType"],
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

        else:
            message = f"[{self.__class__.__name__}]: get_symbols - {
                self._trader_model.exchange_id.value} -> {response.text}"
            logger.error(message)
            raise ExceptionApi(message)


class ApiDemoDzengiCom(ApiDzengiCom):
    def get_endpoint(self) -> str:
        return "https://demo-api-adapter.backend.currency.com/api/v2/"
