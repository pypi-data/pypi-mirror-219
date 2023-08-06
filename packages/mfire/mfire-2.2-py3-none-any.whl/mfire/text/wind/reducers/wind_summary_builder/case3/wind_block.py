from __future__ import annotations

from datetime import timedelta
from typing import Callable, Optional

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.helpers.summary_helper import (
    SummaryKeysMixin,
)
from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_enum import WindType
from mfire.text.wind.reducers.wind_summary_builder.wind_direction import (
    WindDirectionPeriod,
)
from mfire.text.wind.reducers.wind_summary_builder.wind_force.wind_force import (
    WindForcePeriod,
)
from mfire.utils.date import Datetime, Period, Timedelta

LOGGER = get_logger(name="wind_block.mod", bind="wind_block")


class WindBlock(SummaryKeysMixin):
    """WindBlock class."""

    # TODO: it could be changed in the future, specially with a 3-hours step!
    TIME_STEP: Timedelta = Timedelta(timedelta(hours=1))
    WF_INTERVAL_SIZE: int = 5

    def __init__(self, begin_time: Datetime, end_time: Datetime, wind_type: WindType):
        self._period: Period = Period(begin_time, end_time)
        self._wind_type: WindType = wind_type
        self._flag: bool = True
        self._wf_periods: list[WindForcePeriod] = []
        self._wd_periods: list[WindDirectionPeriod] = []

    @property
    def period(self) -> Period:
        return self._period

    @property
    def wf_periods(self) -> list[WindForcePeriod]:
        return self._wf_periods

    @wf_periods.setter
    def wf_periods(self, wf_periods: Optional[list[WindForcePeriod]]) -> None:
        if not wf_periods:
            wf_periods = []
        if self._check_time_of_input_periods(wf_periods) is False:
            return
        self._wf_periods = wf_periods

    @property
    def wd_periods(self) -> list[WindDirectionPeriod]:
        return self._wd_periods

    @wd_periods.setter
    def wd_periods(self, wd_periods: Optional[list[WindDirectionPeriod]]) -> None:
        if not wd_periods:
            wd_periods = []
        if self._check_time_of_input_periods(wd_periods) is False:
            return
        self._wd_periods = wd_periods

    @property
    def wf_period_cnt(self) -> int:
        return len(self._wf_periods)

    @property
    def wd_period_cnt(self) -> int:
        return len(self._wd_periods)

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
    def duration(self) -> Timedelta:
        """Return the WindBlock duration."""
        return Timedelta(self.end_time - self.begin_time) + self.TIME_STEP

    @property
    def wind_type(self) -> WindType:
        """Get the WindBlock wind_type."""
        return self._wind_type

    @wind_type.setter
    def wind_type(self, wind_type: WindType) -> None:
        """Set the WindBlock wind_type."""
        self._wind_type = wind_type

    @property
    def flag(self) -> bool:
        """Get the WindBlock flag."""
        return self._flag

    @flag.setter
    def flag(self, flag: bool) -> None:
        """Set the WindBlock flag."""
        self._flag = flag

    def _check_input_period_times(
        self, period: WindForcePeriod | WindDirectionPeriod
    ) -> bool:
        """Check if input period feets block begin and end times."""
        if period.begin_time < self.begin_time:
            LOGGER.error(
                f"Input period.begin_time '{period.begin_time}' is < block begin_time "
                f"'{self.begin_time}'"
            )
            return False

        if period.end_time > self.end_time:
            LOGGER.error(
                f"Input period.end_time '{period.begin_time}' is < block end_time "
                f"'{self.begin_time}'"
            )
            return False

        return True

    def _check_time_of_input_periods(
        self, periods: list[WindForcePeriod] | list[WindDirectionPeriod]
    ) -> bool:
        """Check if input periods feets block begin and end times."""
        for period in periods:
            if self._check_input_period_times(period) is False:
                return False
        return True

    def merge(
        self, other: WindBlock, wt_select_func: Optional[Callable] = None
    ) -> WindBlock:
        """Merge the wind block with another one."""
        if wt_select_func is None:
            wt_select_func = max

        wind_type_value: int = wt_select_func(
            self._wind_type.value, other.wind_type.value
        )
        wind_type: WindType = WindType(wind_type_value)

        return WindBlock(
            Datetime(min(self.begin_time, other.begin_time)),
            Datetime(max(self.end_time, other.end_time)),
            wind_type,
        )

    def summarize(self, reference_datetime: Datetime) -> dict:
        """Summarise tha WindBlock as a dictionary."""
        summary: dict = {}

        summary.update(
            {
                self.WD_PERIODS: [
                    p.summarize(reference_datetime) for p in self.wd_periods
                ],
                self.WF_PERIODS: [
                    p.summarize(reference_datetime) for p in self.wf_periods
                ],
                self.TIME_DESC: self.period.describe(reference_datetime),
            }
        )

        return summary

    def __hash__(self) -> int:
        """Hash the WindBlock instance."""
        return hash(
            (
                self.begin_time,
                self.end_time,
                self._wind_type,
                self._flag,
            )
        )

    def __eq__(self, other: WindBlock) -> bool:
        """Check WindBlock equality."""
        return (
            self.begin_time == other.begin_time
            and self.end_time == other.end_time
            and self._wind_type == other.wind_type
            and self._flag == other.flag
            and self.wf_periods == other.wf_periods
            and self.wd_periods == other.wd_periods
        )

    def __repr__(self) -> str:
        """Serialize a WindBlock as a string representation."""
        return (
            f"{self.__class__.__name__}(begin_time={self.begin_time}, "
            f"end_time={self.end_time}, duration={self.duration}, "
            f"wind_type={self._wind_type}, flagged={self._flag}, "
            f"wind_direction_periods={self.wd_periods}, "
            f"wind_force_periods={self.wf_periods}, "
        )
