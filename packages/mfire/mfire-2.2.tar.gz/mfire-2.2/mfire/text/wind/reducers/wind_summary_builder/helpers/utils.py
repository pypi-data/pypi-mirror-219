from __future__ import annotations

from typing import Any, Union
import xarray as xr

from mfire.text.wind.reducers.wind_summary_builder.helpers.wind_enum import WindType


class WindFingerprint:
    """WindFingerprint class.

    It contains the typle of the term types and can be serialized as a string.
    """

    def __init__(
        self, wind_types: Union[list[WindType], set[WindType], tuple[WindType]]
    ):
        self.data = tuple(wind_types)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "".join((str(wind_type.value) for wind_type in self.data))

    def __repr__(self):
        return self.__str__()


def coords_dict_from_xr_coords(coords: xr.Coordinate, replace: dict) -> dict:
    """Replace somme coordinates of a given instance of xr.Coordinate."""
    coords_new: dict = {}
    for coord in coords.keys():
        if coord in replace:
            coords_new[coord] = replace[coord]
        else:
            coords_new[coord] = coords[coord].values

    return coords_new


def get_dict_value_from_keys_path(input_dict: dict, keys_path: list) -> Any:
    """Get a dictionary value from a key path."""
    value: Any = input_dict

    for key in keys_path:
        value: dict = value.get(key)
        if value is None:
            break

    return value
