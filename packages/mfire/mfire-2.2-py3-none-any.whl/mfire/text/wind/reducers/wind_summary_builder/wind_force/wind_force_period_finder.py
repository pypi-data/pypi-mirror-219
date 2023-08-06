from __future__ import annotations

from collections import OrderedDict
import numpy as np
from typing import Any, Optional

import xarray as xr

from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_period import (
    BaseWindPeriodFinder,
)
from mfire.text.wind.reducers.wind_summary_builder.pandas_wind_summary import (
    PandasWindSummary,
)
from mfire.utils.date import Datetime

from .wind_force import WindForce, WindForcePeriod


class WindForcePeriodFinder(BaseWindPeriodFinder[WindForce]):

    COL_PERIOD: str = PandasWindSummary.COL_WF_PERIOD
    COL_PERIOD_KEPT: str = PandasWindSummary.COL_WF_PERIOD_KEPT

    def _get_terms_data(
        self,
        data_array: xr.DataArray,
        pd_summary: PandasWindSummary,
        valid_times: np.ndarray,
    ) -> OrderedDict[Datetime, Optional[Any]]:
        """Get the data of each term contained in a DataArray."""

        res: OrderedDict = OrderedDict()

        pd_summary.create_column(pd_summary.COL_WF_T3)

        for valid_time in valid_times:
            date_cur: Datetime = Datetime(valid_time)
            wind_force: WindForce = WindForce.from_term_data_array(
                data_array.sel(valid_time=valid_time)
            )
            res[date_cur] = wind_force

            loc = pd_summary.data.index == valid_time
            pd_summary.data.loc[loc, pd_summary.COL_WF_T3] = wind_force.repr_value

        return res

    def post_process_periods(
        self, periods_list: list[WindForcePeriod]
    ) -> list[WindForcePeriod]:
        """Post process found periods."""
        return periods_list

    def _find_periods(self) -> list[WindForcePeriod]:
        """Find all wind force periods as a list."""
        period_cur: Optional[WindForcePeriod] = None
        periods_list = []

        # Initialize the index
        self._ind = 0

        while self._ind <= self._valid_time_index_max:

            date_cur: Datetime = Datetime(self._valid_time[self._ind])
            wind_force_cur: WindForce = self._terms_data[date_cur]

            if period_cur is None:
                period_cur = WindForcePeriod(date_cur, date_cur, wind_force_cur)
            else:
                update_res: bool = period_cur.update(date_cur, wind_force_cur)
                if update_res is False:
                    periods_list.append(period_cur)
                    period_cur = None
                    continue

            self._ind += 1

        if period_cur is not None:
            periods_list.append(period_cur)

        return periods_list
