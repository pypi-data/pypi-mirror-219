from __future__ import annotations

import copy
from datetime import timedelta
from typing import Callable, Optional

import numpy as np
import pandas as pd
import xarray as xr

from mfire.settings import get_logger
from mfire.text.wind.exceptions import WindSynthesisError
from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_enum import WindType
from mfire.text.wind.reducers.wind_summary_builder.pandas_wind_summary import (
    PandasWindSummary,
)
from mfire.text.wind.reducers.wind_summary_builder.wind_direction import (
    WindDirectionPeriodFinder,
)
from mfire.text.wind.reducers.wind_summary_builder.wind_force import (
    WindForcePeriodFinder,
)
from mfire.utils.date import Datetime, Timedelta

from .wind_block import WindBlock
from .wind_direction_period_finder import HighWindDirectionPeriodFinder

LOGGER = get_logger(name="case3_summary_builder.mod", bind="case3_summary_builder")


class BlocksBuilder:
    """BlocksBuilder class."""

    BLOCKS_MERGE_TRIES: int = 5
    TIME_SLICE_12H: timedelta = Timedelta(timedelta(hours=12))

    def __init__(self):
        """Initialize the BlocksBuilder.

        During the process, _ind attribute travels in the _blocks index and allow to
        update it.
        """
        self._blocks: list[WindBlock] = []
        self._blocks_len: int = 0
        self._ind: int = 0
        self.wf_max: np.float = 0

        self._blocks_nbr_max: int = 0
        self._period_between_min: Timedelta = Timedelta(hours=0)
        self._block_duration_min: Timedelta = Timedelta(hours=0)

    @property
    def blocks(self) -> list[WindBlock]:
        """Get all blocks even low typed blocks."""
        return self._blocks

    @property
    def flagged_blocks(self) -> list[WindBlock]:
        """Get flagged blocks."""
        return [block for block in self.blocks if block.flag is True]

    def _reset_blocks(self, pd_summary: PandasWindSummary):
        """Reset the _blocks attribute.

        At the end of this method, all blocks are flagged (ie has the True flag).
        """
        self._blocks: list[WindBlock] = self._get_wind_blocks(pd_summary)
        self._blocks_len = len(self._blocks)

    def _reset_ind(self):
        """Reset _ind attribute."""
        self._ind = 0

    @staticmethod
    def _get_surveillance_period_duration(pd_summary: PandasWindSummary) -> Timedelta:
        """Get the duration of the surveillance period."""
        valid_time_start: pd.Timestamp = pd_summary.data.index[0]
        valid_time_stop: pd.Timestamp = pd_summary.data.index[-1]
        diff: pd.Timedelta = valid_time_stop - valid_time_start
        period_duration: Timedelta = Timedelta(diff.to_pytimedelta())
        return period_duration

    def _set_parameters(self, pd_summary: PandasWindSummary):
        """Set parameters."""
        # Get duration period
        period_duration: timedelta = self._get_surveillance_period_duration(pd_summary)

        # Set parameters
        self._blocks_nbr_max: int = int(np.ceil(period_duration / self.TIME_SLICE_12H))
        self._period_between_min: Timedelta = Timedelta(period_duration / 6)
        self._block_duration_min: Timedelta = self._period_between_min

        LOGGER.debug(f"blocks_nbr_max: {self._blocks_nbr_max}")
        LOGGER.debug(f"period_between_min: {self._period_between_min}")
        LOGGER.debug(f"block_duration_min: {self._block_duration_min}")

    def _remove_current_block(self):
        """Remove the current block."""
        self._blocks.pop(self._ind)
        self._blocks_len -= 1

    def _merge_block_cur_with_prev_or_next(
        self,
        block_cur: WindBlock,
        block_prev: Optional[WindBlock],
        block_next: Optional[WindBlock],
        wt_select_func: Optional[Callable] = None,
    ) -> WindBlock:
        """Merge the current block with the previous or the next."""
        block_new: WindBlock

        if block_prev:

            if block_next:
                if block_prev.duration <= block_next.duration:
                    block_new = block_cur.merge(block_prev, wt_select_func)
                    self._blocks[self._ind - 1] = block_new
                    self._remove_current_block()
                else:
                    block_new = block_cur.merge(block_next, wt_select_func)
                    self._blocks[self._ind + 1] = block_new
                    self._remove_current_block()
            else:
                block_new = block_cur.merge(block_prev, wt_select_func)
                self._blocks[self._ind - 1] = block_new
                self._remove_current_block()

        elif block_next:
            block_new = block_cur.merge(block_next, wt_select_func)
            self._blocks[self._ind + 1] = block_new
            self._remove_current_block()

        else:
            block_new = block_cur

        self._ind += 1
        return block_new

    @staticmethod
    def _get_wind_blocks(pd_summary: PandasWindSummary) -> list[WindBlock]:
        """Get WindBlocks from the PandasWindSummary."""
        blocks_cnt: int = pd_summary.initialize_wind_blocks()
        blocks = []

        for i in range(blocks_cnt):
            loc = pd_summary.data[pd_summary.COL_WIND_BLOCK] == i
            df: pd.DataFrame = pd_summary.data[loc]
            wind_type_value: int = df.loc[df.index[0], pd_summary.COL_WT]
            wind_block: WindBlock = WindBlock(
                Datetime(df.index[0].to_pydatetime()),
                Datetime(df.index[-1].to_pydatetime()),
                WindType(wind_type_value),
            )
            blocks.append(wind_block)

        return blocks

    def _remove_short_type3_blocks(self, pd_summary: PandasWindSummary) -> None:
        """Remove short type 3 blocks (with a length <= 3 and not with the max wind)."""
        self._reset_ind()

        # Get the index of the block with the maximum wind force

        while self._ind < self._blocks_len:

            block_cur: WindBlock = self._blocks[self._ind]

            # If block_cur is not a Type 3
            if block_cur.wind_type != WindType.TYPE_3:
                self._ind += 1
                continue

            # Check if block_cur has the max wind force and keep it in this case
            loc: slice = slice(
                block_cur.begin_time.as_np_datetime64(),
                block_cur.end_time.as_np_datetime64(),
            )
            rows = pd_summary.data[loc]
            wf_max: np.float64 = rows[pd_summary.COL_WF_MAX].max()

            if wf_max == self.wf_max:
                block_cur.flag = True
                self._ind += 1
                continue

            if block_cur.duration >= self._period_between_min:
                block_cur.flag = True
                self._ind += 1
                continue

            duration_prev: Timedelta = (
                self._blocks[self._ind - 1].duration if self._ind > 0 else None
            )
            duration_next: Timedelta = (
                self._blocks[self._ind + 1].duration
                if self._ind < self._blocks_len
                else None
            )

            cond: bool = (
                duration_prev is not None
                and duration_prev > self._period_between_min
                and duration_next is not None
                and duration_next > self._period_between_min
            )

            if cond is True:
                block_cur.flag = False
                self._ind += 1
            else:
                block_hw_prev: Optional[WindBlock] = None  # Wind type 3
                block_hw_next: Optional[WindBlock] = None  # Wind type 3
                block_prev: Optional[WindBlock] = None  # Wind type 2
                block_next: Optional[WindBlock] = None  # Wind type 2

                if self._ind >= 2 and block_prev is None:
                    block_prev = self._blocks[self._ind - 1]
                    block_hw_prev = self._blocks[self._ind - 2]  # noqa: F841

                if self._ind <= self._blocks_len - 2:
                    block_next = self._blocks[self._ind + 1]
                    block_hw_next = self._blocks[self._ind + 2]  # noqa: F841

                # Try to merge block_cur with previous or next block
                block_cur = self._merge_block_cur_with_prev_or_next(
                    block_cur, block_prev, block_next, min
                )

                if self._ind == self._blocks_len - 1:
                    continue

                # Try to merge block_cur with previous or next block
                self._merge_block_cur_with_prev_or_next(
                    block_cur, block_hw_prev, block_hw_next, max
                )

    def _merge_type3_side_by_side_blocks(self) -> None:
        """Merge all type 3 side by side blocks."""
        self._reset_ind()

        while self._ind < self._blocks_len:

            block_cur: WindBlock = self._blocks[self._ind]

            if block_cur.wind_type == WindType.TYPE_3:

                j = self._ind + 1

                if j < self._blocks_len:
                    block_next: WindBlock = self._blocks[j]
                    if block_next.wind_type == WindType.TYPE_3:
                        block_cur = block_cur.merge(block_next, max)
                        self._blocks[j] = block_cur
                        self._remove_current_block()

            self._ind += 1

    def _try_to_merge_blocks(self) -> None:
        """Try to merge blocks.

        For each type 2  block, try to merge it with a type 3 block next to it. In a
        second time, this function try to merge all type 3  side by side blocks.
        """
        self._reset_ind()

        while self._ind < self._blocks_len:

            block_cur: WindBlock = self._blocks[self._ind]

            if block_cur.wind_type == WindType.TYPE_3:
                self._ind += 1

            # Wind type 1 and 2
            else:
                # If current term is the first or the last term, then it can not be
                # merged respectively with the next or the previous type 3 block
                if self._ind in [0, self._blocks_len - 1]:
                    block_cur.flag = False
                    self._ind += 1
                    continue

                if block_cur.duration > self._period_between_min:
                    block_cur.flag = False
                    self._ind += 1
                elif block_cur.flag is False:
                    self._ind += 1
                else:
                    block_prev: Optional[WindBlock] = (
                        self._blocks[self._ind - 1] if self._ind > 0 else None
                    )
                    block_next: Optional[WindBlock] = (
                        self._blocks[self._ind + 1]
                        if self._ind < self._blocks_len
                        else None
                    )

                    flag_prev: Optional[bool] = block_prev.flag if block_prev else None
                    flag_next: Optional[bool] = block_next.flag if block_next else None

                    if not flag_prev and not flag_next:
                        block_cur.flag = False
                        self._ind += 1
                    else:
                        self._merge_block_cur_with_prev_or_next(
                            block_cur, block_prev, block_next, max
                        )

        self._merge_type3_side_by_side_blocks()

    def get_flagged_blocks_indices(self) -> tuple[list[int], int]:
        """Get the index of the flagged blocks."""
        flagged_blocks_ind: list[int] = []
        cnt: int = 0

        for i, block in enumerate(self._blocks):
            if block.flag is True:
                flagged_blocks_ind.append(i)
                cnt += 1

        return flagged_blocks_ind, cnt

    def _try_to_reduce_blocks_number(self) -> bool:
        """Try to merge the 2 closest flagged blocks."""
        flagged_blocks_ind, t3_blocks_cnt = self.get_flagged_blocks_indices()
        space_min: Timedelta = self.blocks[-1].end_time - self.blocks[0].begin_time
        ind: Optional[int] = None

        for i in range(t3_blocks_cnt - 1):
            i0: int = flagged_blocks_ind[i]
            i1: int = flagged_blocks_ind[i + 1]

            space = self.blocks[i1].begin_time - self.blocks[i0].end_time
            if space <= space_min:
                space_min = space
                ind = i0

        # If a min space between 2 blocks has been found, then we merge those and keep
        # only the resulting block
        if ind:
            self._ind = ind
            block_new: WindBlock = self.blocks[self._ind].merge(
                self.blocks[self._ind + 1]
            )
            self._blocks[self._ind + 1] = block_new
            self._remove_current_block()
            return True

        return False

    def _blocks_merging_post_process(self) -> None:
        """Post process the block merging."""
        flagged_blocks_cnt: int = len(self.flagged_blocks)

        if flagged_blocks_cnt == 0:
            raise WindSynthesisError("No blocks of type 3 have been found")

        elif flagged_blocks_cnt <= self._blocks_nbr_max:
            return

        else:
            LOGGER.warning("A reduction of the Blocks number is needed")
            while flagged_blocks_cnt > self._blocks_nbr_max:
                reduce_res: bool = self._try_to_reduce_blocks_number()

                if reduce_res is False:
                    raise WindSynthesisError(
                        "Failed to reduce the number of type 3 blocks"
                    )

                flagged_blocks_cnt: int = len(self.flagged_blocks)

    def _merge_blocks(self) -> None:
        """Merge blocks as many as possible."""

        for i in range(self.BLOCKS_MERGE_TRIES):

            blocks_tmp: list[WindBlock] = copy.deepcopy(self._blocks)

            self._try_to_merge_blocks()

            if self._blocks == blocks_tmp:
                self._blocks_merging_post_process()
                return

        raise WindSynthesisError(f"Merge of blocks failed: {self.blocks}")

    def _add_flagged_blocks_in_pd_summary(self, pd_summary: PandasWindSummary) -> None:
        """Add "flagged_blocks column in the given PandasWindSummary."""
        pd_summary.create_column(pd_summary.COL_FLAGGED_BLOCK)

        for cnt, block in enumerate(self._blocks):
            if block.flag is False:
                continue
            lower_bound: np.datetime64 = self._blocks[cnt].begin_time.as_np_datetime64()
            upper_bound: np.datetime64 = self._blocks[cnt].end_time.as_np_datetime64()

            pd_summary.data.loc[
                lower_bound:upper_bound, pd_summary.COL_FLAGGED_BLOCK
            ] = cnt

    @staticmethod
    def _get_valid_time_of_block(block: WindBlock, pd_summary: PandasWindSummary):
        """Get the valid_time of a block regarding its begin_time, end_time and type."""
        df_index: pd.Index = pd_summary.data.index

        loc = pd_summary.data[
            (df_index >= block.begin_time.as_np_datetime64())
            & (df_index <= block.end_time.as_np_datetime64())
            & (pd_summary.data[pd_summary.COL_WT] == block.wind_type.value)
        ]
        valid_time: np.ndarray = loc.index.to_numpy()
        return valid_time

    def _get_periods_of_blocks(
        self,
        data_wd: xr.DataArray,
        data_wf: xr.DataArray,
        pd_summary: PandasWindSummary,
    ) -> None:
        """Compute wind direction and force periods of blocks.

        For type 2 blocks, only the wind direction periods is computed.

        Raises
        ------
        ValueError
            If HighWindDirectionPeriodFinder instance raises a ValueError.
        """

        for i, block in enumerate(self._blocks):

            wind_direction_finder: WindDirectionPeriodFinder

            if block.flag is False:  # Wind of type 2
                data_wd_tmp: xr.DataArray = data_wd.sel(
                    valid_time=slice(
                        block.begin_time.as_np_datetime64(),
                        block.end_time.as_np_datetime64(),
                    )
                )

                wind_direction_finder = WindDirectionPeriodFinder(
                    data_wd_tmp,
                    pd_summary,
                    self._get_valid_time_of_block(block, pd_summary),
                )

            else:  # Wind of type 3
                # Keep only terms with type 3 terms
                loc: slice = slice(
                    block.begin_time.as_np_datetime64(),
                    block.end_time.as_np_datetime64(),
                )
                rows: pd.DataFrame = pd_summary.data[loc]
                rows = rows[rows[pd_summary.COL_WT] == WindType.TYPE_3.value]
                kept_term_dates: np.ndarray = rows.index.to_numpy()

                # Get wind direction of type 3 terms (directions of terms with other
                # type are not kept)
                data_wd_tmp: xr.DataArray = data_wd.sel(valid_time=kept_term_dates)

                # Get valid_time of the current type 3 block
                valid_time: np.ndarray = self._get_valid_time_of_block(
                    block, pd_summary
                )

                wind_direction_finder = HighWindDirectionPeriodFinder(
                    data_wd_tmp, pd_summary, valid_time
                )

                # Get wind force of type 3 terms (wind forces of terms with other
                # type are not kept)
                data_wf_tmp: xr.DataArray = data_wf.sel(valid_time=kept_term_dates)

                # Get wind force periods of type 3 terms
                wind_force_finder: WindForcePeriodFinder = WindForcePeriodFinder(
                    data_wf_tmp, pd_summary, valid_time
                )
                self._blocks[i].wf_periods = wind_force_finder.run(pd_summary)

            # Get wind direction periods
            self._blocks[i].wd_periods = wind_direction_finder.run(pd_summary)

    def run(
        self,
        pd_summary: PandasWindSummary,
        data_wf: xr.DataArray,
        data_wd: xr.DataArray,
    ) -> list[WindBlock]:
        """Run the builder.

        Its unflagged all resting low typed blocks (type 1 and 2) and all short type 3
        blocks as well.
        """
        # Set parameters
        self._set_parameters(pd_summary)

        # Get max wind force
        self.wf_max = pd_summary.find_type_3_wf_max()

        # Reset blocks list
        self._reset_blocks(pd_summary)

        # Find the wind force max and remove short type 3 blocks
        self._remove_short_type3_blocks(pd_summary)

        # Merge blocks
        self._merge_blocks()

        self._add_flagged_blocks_in_pd_summary(pd_summary)

        # Get wind force periods of type 3 blocks and wind direction periods of type 2
        # and 3 blocks
        self._get_periods_of_blocks(data_wd, data_wf, pd_summary)

        return self.blocks
