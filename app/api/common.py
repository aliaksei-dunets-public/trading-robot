from datetime import datetime, timedelta
import time
import math
import logging
import httpx
import json
import pandas as pd

from app.core.config import consts, logging
import app.model.models as model
import app.model.enums as enum

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
            message = f"[{
                self.__class__.__name__}]: GET - {url}({params}) -> {response.text}"
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

    async def get_history_data(self, hd_param: model.HistoryDataParamModel, **kwargs) -> model.HistoryDataModel:

        df: pd.DataFrame = pd.DataFrame()

        limit = hd_param.limit

        # Determine the number of full batches
        full_batches = limit // self.BATCH_SIZE

        # Boolean importing parameters closed_bars in order to get only closed bar for the current moment
        # If closed_bars indicator is True -> calculated endTime for the API
        local_datetime = datetime.now()
        closed_datetime = self.get_end_datetime(
            interval=hd_param.interval, original_datetime=local_datetime, closed=hd_param.closed)

        # Execute full batches
        for _ in range(full_batches):
            hd_param.set_limit(self.BATCH_SIZE)
            batch_history_data = await self._get_history_dataframe(
                hd_param=hd_param,
                end=self.getUnixTimeMsByDatetime(closed_datetime),
            )

            if not batch_history_data.empty:
                df = pd.concat([df, batch_history_data])

            df = df.sort_index()

            # Get the latest date of the batch
            # pd.to_datetime(df.head(1).index.values[0])
            last_datetime = df.index[0].to_pydatetime()

            closed_datetime = self._get_next_batch_end_datetime(
                end_datetime=last_datetime, interval=hd_param.interval)

        # Execute the remaining elements
        rest_of_limit = limit % self.BATCH_SIZE
        if rest_of_limit > 0:
            hd_param.set_limit(rest_of_limit)
            batch_history_data = await self._get_history_dataframe(
                hd_param=hd_param,
                end=self.getUnixTimeMsByDatetime(closed_datetime),
            )

            df = pd.concat([df, batch_history_data])

        # Create HistoryDataModel
        history_data_mdl = model.HistoryDataModel(
            symbol=hd_param.symbol,
            interval=hd_param.interval,
            limit=limit,
            data=df.sort_index(),
        )

        return history_data_mdl

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

    async def _get_history_dataframe(
        self, hd_param: model.HistoryDataParamModel, start=None, end=None, **kwargs
    ) -> model.HistoryDataModel:
        pass

    def _get_next_batch_end_datetime(
        self, end_datetime: datetime, interval: enum.IntervalEnum, batch_size: int = 1000
    ):
        next_datetime_delta = None

        if interval == enum.IntervalEnum.MIN_1:
            next_datetime_delta = timedelta(minutes=1)
        elif interval == enum.IntervalEnum.MIN_5:
            next_datetime_delta = timedelta(minutes=5)
        elif interval == enum.IntervalEnum.MIN_15:
            next_datetime_delta = timedelta(minutes=15)
        elif interval == enum.IntervalEnum.MIN_30:
            next_datetime_delta = timedelta(minutes=30)
        elif interval == enum.IntervalEnum.HOUR_1:
            next_datetime_delta = timedelta(hours=1)
        elif interval == enum.IntervalEnum.HOUR_4:
            next_datetime_delta = timedelta(hours=4)
        elif interval == enum.IntervalEnum.DAY_1:
            next_datetime_delta = timedelta(days=1)
        elif interval == enum.IntervalEnum.WEEK_1:
            next_datetime_delta = timedelta(days=7)
        else:
            return end_datetime

        return end_datetime - next_datetime_delta
