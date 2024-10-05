from datetime import datetime, timedelta
import time
import math
import logging
import httpx
import json

from app.core.config import consts, logging
import app.models.main as model
import app.models.enum as enum

logger = logging.getLogger("api")


class ExceptionApi(Exception):
    pass


class RequestAsync():
    async def get(self, url: str, params=None):

        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, params=params)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            message = f"[{self.__class__.__name__}]: GET - {
                url}({params}) -> {response.text}"
            logger.error(message)
            raise ExceptionApi(message)


class ApiBase:

    DEFAULT_FEE = 0.0001
    BATCH_SIZE = 1000

    def __init__(self, trader_model: model.TraderModel):
        self._trader_model = trader_model
        self._request_async = RequestAsync()

    @staticmethod
    def getUnixTimeMsByDatetime(original_datetime: datetime) -> int:
        """
        Calculates the Unix timestamp in milliseconds for the datetime.
        Args:
            original_datetime (datetime): The datetime object.
        Returns:
            int: The Unix timestamp in milliseconds.
        """
        if original_datetime:
            return int(original_datetime.timestamp() * 1000)
        else:
            return None

    @staticmethod
    def getDatetimeByUnixTimeMs(timestamp: int) -> datetime:
        """
        Converts a Unix timestamp in milliseconds to a datetime object.
        Args:
            timestamp (int): The Unix timestamp in milliseconds.
        Returns:
            datetime: The datetime object.
        """

        return datetime.fromtimestamp(timestamp / 1000.0)

    @staticmethod
    def getTimezoneDifference() -> int:
        """
        Calculates the difference in hours between the local timezone and UTC.
        Returns:
            int: The timezone difference in hours.
        """

        local_time = datetime.now()
        utc_time = datetime.utcnow()
        delta = local_time - utc_time

        return math.ceil(delta.total_seconds() / 3600)

    def get_end_datetime(self, interval: str, **kwargs) -> datetime:
        pass
        # TODO

    def get_history_data(self, hd_param: model.HistoryDataParamModel, **kwargs) -> model.HistoryDataModel:
        pass
        # TODO

    async def get_symbols(self, **kwargs) -> dict[model.SymbolModel]:
        pass

    async def get_symbol_fee(self, symbol: str) -> float:
        return self.DEFAULT_FEE

    async def ping_server(self, **kwargs) -> bool:
        return False

    def get_endpoint(self) -> str:
        return ""

    def _map_interval(self, api_interval: str = None, interval: enum.IntervalEnum = None):
        if api_interval:
            return interval
        elif interval:
            return api_interval

    def _get_url(self, path: str) -> str:
        return self.get_endpoint() + path

    def _get_float_from_dict(self, name: str, dictionary: dict):
        if dictionary and name in dictionary and dictionary[name] != "":
            return float(dictionary[name])
        else:
            return 0
