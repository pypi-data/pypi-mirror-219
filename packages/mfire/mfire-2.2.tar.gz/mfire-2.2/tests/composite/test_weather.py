from pathlib import Path

import pytest
import xarray as xr

from mfire.composite import LocalisationConfig, WeatherComposite


class TestWeatherComposite:
    def test_wrong_field(self):
        with pytest.raises(
            ValueError,
            match="Wrong field: [], expected ['wwmf', 'precip', 'rain', 'snow', 'lpn']",
        ):
            WeatherComposite(
                id="weather", params={}, units={}, localisation=LocalisationConfig()
            )

    def test_check_condition(self):
        weather_compo = WeatherComposite(
            id="tempe",
            params={
                "tempe": {
                    "file": Path(""),
                    "selection": None,
                    "grid_name": "",
                    "name": "",
                }
            },
            units={},
            localisation=LocalisationConfig(),
        )
        assert weather_compo.check_condition is False

    def test_altitudes(self):
        weather_compo = WeatherComposite(
            id="tempe",
            params={
                "tempe": {
                    "file": Path(""),
                    "selection": None,
                    "grid_name": "franxl1s100",
                    "name": "",
                }
            },
            units={},
            localisation=LocalisationConfig(),
        )

        assert weather_compo.altitudes("weather") is None

        alt = weather_compo.altitudes("tempe")
        assert isinstance(alt, xr.DataArray)
        assert alt.name == "franxl1s100"
