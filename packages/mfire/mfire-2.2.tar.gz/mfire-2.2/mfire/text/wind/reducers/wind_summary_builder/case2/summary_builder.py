from __future__ import annotations

import xarray as xr

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.base_case_summary_builder import (
    BaseCaseSummaryBuilder,
)
from mfire.text.wind.reducers.wind_summary_builder.helpers.mixins import (
    SummaryBuilderMixin,
)
from mfire.text.wind.reducers.wind_summary_builder.helpers.summary_helper import (
    SummaryKeysMixin,
    SummaryValuesMixin,
)
from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_enum import (
    WindCase,
    WindType,
)
from mfire.text.wind.reducers.wind_summary_builder.pandas_wind_summary import (
    PandasWindSummary,
)
from mfire.text.wind.reducers.wind_summary_builder.wind_direction import (
    WindDirectionPeriod,
    WindDirectionPeriodFinder,
)

LOGGER = get_logger(name="case2_summary_builder.mod", bind="case2_summary_builder")


class Case2SummaryBuilder(
    SummaryBuilderMixin, SummaryKeysMixin, SummaryValuesMixin, BaseCaseSummaryBuilder
):
    def _get_wind_force_intensity(self, wind_types_set: set[WindType]) -> str:
        """Get the textual wind force intensity from the wind types."""

        if WindType.TYPE_1 in wind_types_set:
            return self.WF_INTENSITY_LOW_MIDDLE
        return self.WF_INTENSITY_MIDDLE

    def run(
        self,
        pd_summary: PandasWindSummary,
        reference_datetime,
        data_wd: xr.DataArray,
        wind_types_set_origin: set[WindType],
    ) -> dict:
        """Run the summary builder."""

        # Get wind directions with WindDirectionPeriodFinder
        loc = pd_summary.data[pd_summary.COL_WT] == WindType.TYPE_2.value
        wind_direction_finder = WindDirectionPeriodFinder(
            data_wd, pd_summary, loc.index
        )
        periods: list[WindDirectionPeriod] = wind_direction_finder.run(pd_summary)

        # Compute and return the summary
        self._summary = {
            self.WD_PERIODS: [p.summarize(reference_datetime) for p in periods],
            self.WF_INTENSITY: self._get_wind_force_intensity(wind_types_set_origin),
        }
        self._set_summary_wind_case(WindCase.CASE_2)

        return self._summary
