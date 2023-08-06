from pathlib import Path
from tempfile import gettempdir
from typing import Any, Optional, Union
from uuid import uuid4

import numpy as np
import pandas as pd
import xarray as xr

from mfire.settings import get_logger
from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_enum import WindType

LOGGER = get_logger(name="pands_wind_summary.mod", bind="pands_wind_summary")


class PandasWindSummary:
    """PandasWindSummary class.

    Class used to keep wind data characteristics and information.
    """

    COL_WIND_BLOCK: str = "w_block"
    COL_FLAGGED_BLOCK: str = "flagged_block"
    COL_WD_LOWER_BOUND: str = "wd_lbound"
    COL_WD_UPPER_BOUND: str = "wd_ubound"
    COL_WD_MIDDLE: str = "wd_middle"
    COL_WD_SYMPO: str = "wd_sympo"
    COL_WD_PERIOD: str = "wd_period"
    COL_WD_PERIOD_KEPT: str = "wd_period_kept"
    COL_WF_PERIOD: str = "wf_period"
    COL_WF_PERIOD_KEPT: str = "wf_period_kept"
    COL_WF_MAX: str = "wf_max"
    COL_WT: str = "wt"
    COL_WF_T3: str = "t3_wf"
    VALID_TIME_INDEX: str = "valid_time"
    TYPE_3_WF_MAX: str = "type_3_wf_max"

    def __init__(
        self,
        valid_time: Optional[Union[xr.DataArray, np.ndarray, list]] = None,
        file_path: Optional[Path] = None,
    ) -> None:
        self.data: pd.DataFrame

        if valid_time is not None:
            self.data = self.initialize_from_valid_time(valid_time)
        elif file_path is not None:
            self.data = self.initialize_from_file(file_path)
        else:
            raise ValueError("No input argument value was found!")

    def initialize_from_valid_time(self, valid_time: xr.DataArray):
        """Create an empty DataFrame from a valid_time DataArray."""
        data = pd.DataFrame(
            index=pd.Series(valid_time),
            columns=[
                self.COL_WT,
                self.COL_WF_MAX,
            ],
            copy=False,
        )
        data.index.name = self.VALID_TIME_INDEX
        return data

    @staticmethod
    def initialize_from_file(file_path: Path):
        """Read a pickle file."""
        data = pd.read_pickle(file_path)
        return data

    def create_column(self, col_name: str, init_value: Optional[Any] = None) -> None:
        """Create a column."""
        if col_name not in self.data:
            self.data[col_name] = init_value

    def add_wf_max_column(self, data_wf: xr.DataArray):
        """Add the wind force max column (called wf_max).

        For each term line, this column is filled by the maximum value of the wind force
        of the term.
        """
        wf_max = []
        for valid_time in self.data.index:
            wf_max_cur: np.float64 = np.float64(
                np.max(data_wf.sel(valid_time=valid_time).values)
            )
            # wf_max.append(wf_max_cur.round(1))
            wf_max.append(wf_max_cur)

        self.data[self.COL_WF_MAX] = wf_max

    def find_type_3_wf_max(self, store: Optional[bool] = True) -> np.float64:
        """Find the maximum of the wf_max column."""
        type_3_rows = self.data[self.data[self.COL_WT] == WindType.TYPE_3.value]
        if type_3_rows.empty:
            raise pd.errors.EmptyDataError("No wind type terms found !")

        type_3_wf_max: np.float64 = np.float64(np.max(type_3_rows[self.COL_WF_MAX]))

        # Set type_3_wf_max in Data Frame attributes
        if store:
            self.add_attr(self.TYPE_3_WF_MAX, type_3_wf_max)

        return type_3_wf_max

    def remove_rows_from_valid_times(self, valid_times: np.ndarray):
        """Remove rows from a valid_times array."""
        index_numpy: np.ndarray = self.data.index.to_numpy()
        mask = np.isin(index_numpy, valid_times)

        mask_array = np.ma.masked_array(index_numpy, mask)
        self.data.drop(mask_array[np.where(~mask_array.mask)], inplace=True)

    def add_attr(self, attr_name: str, attr_value):
        """Add an attribute to the data."""
        self.data.attrs[attr_name] = attr_value

    def initialize_wind_blocks(self) -> int:
        """Initialize the wind block column (called w_block)."""
        self.data[self.COL_WIND_BLOCK] = None

        wt_up_col_num: int = self.data.columns.get_loc(self.COL_WT)
        block_col_num: int = self.data.columns.get_loc(self.COL_WIND_BLOCK)

        i: int = 0
        cnt: int = -1
        upper_bound: int = len(self.data)

        while i < upper_bound:

            wind_type_ref: int = self.data.iloc[i, wt_up_col_num]

            cnt += 1
            self.data.iloc[i, block_col_num] = cnt

            j = i + 1

            while j < upper_bound:
                wind_type: int = self.data.iloc[j, wt_up_col_num]
                if wind_type != wind_type_ref:
                    break
                self.data.iloc[j, block_col_num] = cnt
                j += 1

            i = j

        loc = self.data[self.COL_WIND_BLOCK].notnull()
        return len(pd.unique(self.data[loc][self.COL_WIND_BLOCK]))

    def to_pickle(self, file_path: Optional[Path] = None) -> Path:
        """Export he data to a pickle file."""
        if file_path is None:
            filename: str = f"pd_summary_{uuid4().hex}.pkl"
            file_path = Path(gettempdir(), filename)
        LOGGER.debug(f"--> pandas summary pkl file path: {file_path}")
        self.data.to_pickle(str(file_path))
        return file_path
