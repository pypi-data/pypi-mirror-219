from __future__ import annotations

import copy
from collections import OrderedDict
from functools import reduce
from typing import Optional

import numpy as np
import xarray as xr

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_period import (
    BaseWindPeriodFinder,
)
from mfire.text.wind.reducers.wind_summary_builder.pandas_wind_summary import (
    PandasWindSummary,
)
from mfire.utils.date import Datetime

from .wind_direction import WindDirection, WindDirectionPeriod

# Logging
LOGGER = get_logger(name="wind_summary_builder.mod", bind="wind_summary_builder")


class WindDirectionPeriodFinder(BaseWindPeriodFinder[WindDirection]):

    COL_PERIOD: str = PandasWindSummary.COL_WD_PERIOD
    COL_PERIOD_KEPT: str = PandasWindSummary.COL_WD_PERIOD_KEPT
    DEGREES_SECTOR_SIZE: float = 22.5
    TERM_DIRECTION_SIZE_MAX: float = 4 * DEGREES_SECTOR_SIZE
    MULTIPLE_TERMS_DIRECTION_SIZE_MAX: float = 6 * DEGREES_SECTOR_SIZE
    PERIOD_HOURS_MIN: np.timedelta64 = np.timedelta64(2, "h")
    PERCENT_MIN: float = 100.0

    def check_terms(self) -> bool:
        """Check all data terms."""
        return False if None in self._terms_data.values() else True

    @staticmethod
    def _get_unique_values_of_wd_array(wd_array: np.ndarray) -> list:
        """Get all unique values of a wind direction array."""
        unique, count = np.unique(wd_array, return_counts=True)
        unique_counts = list(zip(unique, count))
        unique_counts.sort(key=lambda e: e[1], reverse=True)
        return unique_counts

    def _get_most_populated_wind_directions_of_wd_ndarray(
        self, wd_array: np.ndarray
    ) -> Optional[WindDirection]:
        """Get the most populated wind direction of an array."""
        not_nan_count: int = np.count_nonzero(~np.isnan(wd_array))
        unique_counts: list = self._get_unique_values_of_wd_array(wd_array)

        met_values: list = []
        met_points_counter: int = 0

        for value, count in unique_counts:

            if np.isnan(value):
                continue

            met_points_counter += count
            met_values.append(value)
            percent = met_points_counter * 100.0 / not_nan_count

            if percent >= self.PERCENT_MIN:
                return WindDirection(met_values)

        return None

    def _create_wind_direction_instance(
        self, degrees: list[float]
    ) -> Optional[WindDirection]:
        """Create a WindDirection from a degrees list."""
        wind_direction = WindDirection(copy.deepcopy(degrees))
        check: bool = wind_direction.check_size(self.TERM_DIRECTION_SIZE_MAX)
        return wind_direction if check else None

    def _get_terms_data(
        self,
        data_array: xr.DataArray,
        pd_summary: PandasWindSummary,
        valid_times: np.ndarray,
    ) -> OrderedDict[Datetime, Optional[WindDirection]]:
        """Get the data of each term contained in a DataArray."""
        res: OrderedDict = OrderedDict()
        wd: WindDirection

        # Create pandas summary columns
        pd_summary.create_column(pd_summary.COL_WD_LOWER_BOUND)
        pd_summary.create_column(pd_summary.COL_WD_UPPER_BOUND)
        pd_summary.create_column(pd_summary.COL_WD_MIDDLE)
        pd_summary.create_column(pd_summary.COL_WD_SYMPO)

        for valid_time in valid_times:
            date_cur: Datetime = Datetime(valid_time)
            wd = self._get_most_populated_wind_directions_of_wd_ndarray(
                data_array.sel(valid_time=valid_time).values
            )

            if wd is None:
                res[date_cur] = None
                continue

            loc = pd_summary.data.index == valid_time
            pd_summary.data.loc[loc, pd_summary.COL_WD_LOWER_BOUND] = wd.lower_bound
            pd_summary.data.loc[loc, pd_summary.COL_WD_UPPER_BOUND] = wd.upper_bound
            pd_summary.data.loc[loc, pd_summary.COL_WD_MIDDLE] = wd.middle

            # Keep wind direction if its check is OK
            check: bool = wd.check_size(self.TERM_DIRECTION_SIZE_MAX)
            if check:
                res[date_cur] = wd
                pd_summary.data.loc[loc, pd_summary.COL_WD_SYMPO] = wd.sympo_code
            else:
                res[date_cur] = None

        return res

    def _period_start_finder(self, date_cur: Datetime) -> Optional[WindDirectionPeriod]:
        """Try to find a WindDirectionPeriod start.

        We need to have consecutive term along at least PERIOD_HOURS_MIN with the same
        Wind Direction.

        Returns
        -------
        Optional[WindDirectionPeriod]
            A WindDirectionPeriod if the finder succeeded, else None.
        """
        j: int = self._ind

        while (
            j <= self._valid_time_index_max
            and self._valid_time[j] - date_cur < self.PERIOD_HOURS_MIN
        ):
            if j == self._valid_time_index_max:
                self._ind = self._valid_time_index_max
                return None

            wind_direction_cur: Optional[WindDirection] = self._terms_data[
                self._valid_time[j]
            ]

            if wind_direction_cur is None:
                self._ind += 1
                return None
            j += 1

        wind_direction: WindDirection = reduce(
            (lambda w1, w2: w1 + w2),
            [self._terms_data[self._valid_time[i]] for i in range(self._ind, j + 1)],
        )

        if wind_direction.check_size(self.MULTIPLE_TERMS_DIRECTION_SIZE_MAX):
            period_cur = WindDirectionPeriod(
                self._valid_time[self._ind], self._valid_time[j], wind_direction
            )
            self._ind = j
            return period_cur

        self._ind += 1

        return None

    def _get_wind_direction_periods(self):
        """Get WindDirectionPeriods."""
        print(f"self.terms_data: {self.terms_data}")

        if self._valid_time_index_max == 0:
            return []

        date_last_term: Datetime = self._valid_time[self._valid_time_index_max]
        period_cur: Optional[WindDirectionPeriod] = None
        periods = []
        wind_direction_cur: Optional[WindDirection]
        wind_direction_new: WindDirection

        # Initialize the index
        self._ind = 0

        while self._ind <= self._valid_time_index_max:
            date_cur: Datetime = self._valid_time[self._ind]

            if period_cur is None:
                # If there is not enough terms to have a period, we break to return
                # periods list
                if date_last_term - date_cur < self.PERIOD_HOURS_MIN:
                    break

                # Search period start
                period_cur = self._period_start_finder(date_cur)
            else:
                wind_direction_cur: WindDirection = self._terms_data[
                    self._valid_time[self._ind]
                ]

                if wind_direction_cur is not None:

                    # Try to update the current period with wind_direction_new
                    update_res: bool = period_cur.update(
                        date_cur,
                        wind_direction_cur,
                        self.MULTIPLE_TERMS_DIRECTION_SIZE_MAX,
                    )

                    # If update ok and not the last term, then continue
                    if update_res is True and self._ind < self._valid_time_index_max:
                        self._ind += 1
                        continue

                # Else, keep the period_cur
                periods.append(period_cur)
                period_cur = None

        print(f"periods: {periods}")

        return periods

    def _check_description_period_coverage(self, periods_list) -> bool:
        """Check if the beginning and the end of the description period are covered.

        It checks if:
        - the first period start at the beginning of the descriptive period
        - the last period ends et the end of the descriptive period.
        """
        if (
            periods_list[0].begin_time == self._valid_time[0]
            and periods_list[-1].end_time == self._valid_time[-1]
        ):
            return True
        return False

    def _find_periods(self) -> list[WindDirectionPeriod]:
        """Find all wind direction periods as a list.

        If a term has no wind direction, then the result is an empty list.
        """
        if self.check_terms() is False:
            periods_list = []
        else:
            periods_list: list[WindDirectionPeriod] = self._get_wind_direction_periods()

        return periods_list

    def post_process_periods(
        self, periods_list: list[WindDirectionPeriod]
    ) -> list[WindDirectionPeriod]:
        """Post process found periods."""

        periods_nbr = len(periods_list)

        if self._check_description_period_coverage(periods_list):

            # If a WindDirectionPeriod found: just keep this period
            if periods_nbr == 1:
                pass

            # Else keep the first and the last periods
            else:
                periods_list = [periods_list[0], periods_list[-1]]
        else:
            periods_list = []

        return periods_list
