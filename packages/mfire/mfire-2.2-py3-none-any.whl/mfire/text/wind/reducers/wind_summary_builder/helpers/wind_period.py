from __future__ import annotations

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Generic, Optional, TypeVar

import numpy as np
import xarray as xr

from mfire.text.wind.reducers.wind_summary_builder.helpers.summary_helper import (
    SummaryKeysMixin,
)
from mfire.text.wind.reducers.wind_summary_builder.pandas_wind_summary import (
    PandasWindSummary,
)
from mfire.utils.date import Datetime, Period, Timedelta

WindElement = TypeVar("WindElement")


class WindPeriod(SummaryKeysMixin, ABC, Generic[WindElement]):
    """WindPeriod abstract class."""

    def __init__(
        self, begin_time: Datetime, end_time: Datetime, wind_element: WindElement
    ):
        if begin_time > end_time:
            raise ValueError(f"begin_time '{begin_time}' > end_time '{end_time}'")
        self._period: Period = Period(begin_time, end_time)
        self._wind_element: WindElement = wind_element

    @property
    def wind_element(self) -> WindElement:
        return self._wind_element

    @wind_element.setter
    def wind_element(self, wind_element: WindElement) -> None:
        self._wind_element = wind_element

    @property
    def begin_time(self) -> Datetime:
        """begin_time

        Returns:
            Datetime: Beginning of the period
        """
        return self._period.begin_time

    @property
    def end_time(self) -> Datetime:
        """end_time

        Returns:
            Datetime: End of the period
        """
        return self._period.end_time

    @property
    def period(self) -> Period:
        return self._period

    @property
    def duration(self) -> Timedelta:
        return Timedelta(self.end_time - self.begin_time)

    def __eq__(self, other: Optional[WindPeriod]) -> bool:
        if other is None:
            return False
        return self.period == other.period and self.wind_element == other.wind_element

    @abstractmethod
    def __add__(self, other: WindPeriod):
        pass

    def __hash__(self) -> int:
        return hash(
            (
                self.period,
                self.wind_element,
            )
        )

    def summarize(self, reference_datetime: Datetime) -> dict:
        """Summarize the WindPeriod instance."""
        return {
            self.BEGIN_TIME_MARKER: self.begin_time.describe_as_period(
                reference_datetime
            ),
            self.END_TIME_MARKER: self.end_time.describe_as_period(reference_datetime),
            self.TIME_DESC: self.period.describe(reference_datetime),
        }


class BaseWindPeriodFinder(ABC, Generic[WindElement]):
    """BaseWindPeriodFinder class."""

    COL_PERIOD: str
    COL_PERIOD_KEPT: str

    def __init__(
        self,
        data_array: xr.DataArray,
        pd_summary: PandasWindSummary,
        valid_times: np.ndarray,
    ):
        self._terms_data: OrderedDict[Datetime, Optional[WindElement]]

        self._terms_data = self._get_terms_data(data_array, pd_summary, valid_times)
        self._valid_time: list[Datetime] = list(self._terms_data.keys())
        self._valid_time_index_max: int = len(self._valid_time) - 1
        self._ind: int = 0

    @property
    def terms_data(self) -> OrderedDict[Datetime, WindElement]:
        """Get the data of each term as an ordered dictionary."""
        return self._terms_data

    @abstractmethod
    def _get_terms_data(
        self,
        data_array: xr.DataArray,
        pd_summary: PandasWindSummary,
        valid_times: np.ndarray,
    ) -> OrderedDict[Datetime, Optional[WindElement]]:
        """Get the data of each term contained in a DataArray."""
        pass

    @staticmethod
    def _add_periods_to_pd_summary(
        periods_list: list[WindPeriod],
        pd_summary: PandasWindSummary,
        col_name: str,
    ):
        """Add the periods of a list in a PandasWindSummary."""
        pd_summary.create_column(col_name)

        cnt = 0

        for period in periods_list:
            loc: slice = slice(
                period.begin_time.as_np_datetime64(),
                period.end_time.as_np_datetime64(),
            )
            pd_summary.data.loc[loc, col_name] = cnt
            cnt += 1

    @abstractmethod
    def _find_periods(self) -> list[WindPeriod]:
        """Find all wind periods as a list."""
        pass

    @abstractmethod
    def post_process_periods(self, periods_list: list[WindPeriod]) -> list[WindPeriod]:
        """Post process found periods."""
        pass

    def run(self, pd_summary: Optional[PandasWindSummary] = None) -> list[WindPeriod]:
        """Run the period finder."""
        periods_list: list[WindPeriod] = self._find_periods()

        # Update pd_summary with wind direction and all periods
        if pd_summary:
            self._add_periods_to_pd_summary(periods_list, pd_summary, self.COL_PERIOD)

        if periods_list:
            periods_list = self.post_process_periods(periods_list)

            # Update pd_summary with kept periods
            if pd_summary:
                self._add_periods_to_pd_summary(
                    periods_list, pd_summary, self.COL_PERIOD_KEPT
                )

        return periods_list
