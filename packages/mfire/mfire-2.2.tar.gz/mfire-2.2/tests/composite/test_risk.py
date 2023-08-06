import logging
from pathlib import Path

import numpy as np
import pytest

from mfire.composite import EventBertrandComposite, EventComposite, LevelComposite


@pytest.fixture(scope="module")
def data_dirname(working_dir):
    return working_dir / "data"


def get_mask_file(dirname):
    return dirname / "mask.nc"


def get_RR_mask(dirname):
    return dirname / "RR_mask.nc"


def get_altitude_file(dirname):
    return dirname / "altitude.nc"


def get_plain_event(dirname):
    """
    le seuil de 2 est remplacé par 1.99999 car depuis le passage des données en float32
    la comparaison a exactement 2 n'apporte pas les mêmes résultats
    """
    field_file = dirname / "field.nc"
    event = {
        "field": {
            "file": field_file,
            "selection": {
                "slice": {"valid_time": ["20191210T010000", "20191210T030000"]}
            },
            "grid_name": "mask",
            "name": "field",
        },
        "category": "quantitative",
        "plain": {"comparison_op": "supegal", "threshold": 1.99999, "units": "°C"},
        "aggregation": {"method": "requiredDensity", "kwargs": {"dr": 0.3}},
        "altitude": {
            "filename": get_altitude_file(dirname),
        },
        "compute_list": ["density", "extrema", "representative", "summary"],
    }

    return event


def get_plain_weighted(dirname):
    event = get_plain_event(dirname)
    fcentral = dirname / "central_mask.nc"
    event["aggregation"] = {
        "method": "requiredDensityWeighted",
        "kwargs": {
            "dr": 0.34,
            "central_mask_id": {"file": fcentral, "mask_id": "Central"},
            "outer_weight": "1",
            "central_weight": "10",
        },
    }
    return event


def get_bertrand_event(dirname):
    field_file = dirname / "RR6.nc"
    RR1_file = dirname / "RR1.nc"
    event = {
        "field": {
            "file": field_file,
            "selection": {
                "slice": {"valid_time": ["20191210T000000", "20191210T120000"]}
            },
            "grid_name": "mask",
            "name": "RR6",
        },
        "field_1": {
            "file": RR1_file,
            "selection": {
                "slice": {"valid_time": ["20191210T000000", "20191210T120000"]}
            },
            "grid_name": "mask",
            "name": "RR1",
        },
        "cum_period": 6,
        "category": "quantitative",
        "altitude": {
            "filename": get_RR_mask(dirname),
        },
        "plain": {"comparison_op": "supegal", "threshold": 20, "units": "mm"},
        "time_dimension": "valid_time",
        "compute_list": ["density", "extrema", "representative", "summary"],
    }
    return event


def get_bertrand_event_from_RR3(dirname):
    field_file = dirname / "RR6_b.nc"
    RR1_file = dirname / "RR3.nc"
    event = {
        "field": {
            "file": field_file,
            "selection": {
                "slice": {"valid_time": ["20191210T020000", "20191210T110000"]}
            },
            "grid_name": "mask",
            "name": "RR6_b",
        },
        "field_1": {
            "file": RR1_file,
            "selection": {
                "slice": {"valid_time": ["20191210T020000", "20191210T110000"]}
            },
            "grid_name": "mask",
            "name": "RR3",
        },
        "cum_period": 6,
        "category": "quantitative",
        "altitude": {
            "filename": get_RR_mask(dirname),
        },
        "plain": {"comparison_op": "supegal", "threshold": 20, "units": "mm"},
        "time_dimension": "valid_time",
        "compute_list": ["density", "extrema", "representative", "summary"],
    }
    return event


def get_mean_bertrand_event(dirname):
    event = get_bertrand_event(dirname)
    event["aggregation"] = {"method": "mean"}
    return event


def get_drr_bertrand_event(dirname):
    event = get_bertrand_event(dirname)
    event["aggregation"] = {"method": "requiredDensity", "kwargs": {"dr": 0.76}}
    return event


def get_mountain_event(dirname):
    field_file = dirname / "field.nc"
    altitude_file = dirname / "altitude.nc"
    event = {
        "field": {
            "file": field_file,
            "selection": {
                "slice": {"valid_time": ["20191210T010000", "20191210T030000"]}
            },
            "grid_name": "mask",
            "name": "field",
        },
        "category": "quantitative",
        "mountain_altitude": 1200,
        "altitude": {
            "filename": altitude_file,
        },
        "plain": {"comparison_op": "sup", "threshold": 2, "units": "degC"},
        "mountain": {"comparison_op": "supegal", "threshold": 4, "units": "degreeC"},
        "aggregation": {"method": "requiredDensity", "kwargs": {"dr": 0.1}},
        "compute_list": ["density", "extrema", "representative", "summary"],
    }
    return event


def get_downstream_risk(dirname):
    field_file = dirname / "field.nc"
    dict_risk_downstream = {
        "level": 1,
        "probability": "no",
        "aggregation_type": "downStream",
        "logical_op_list": ["and"],
        "aggregation": {"method": "requiredDensity", "kwargs": {"dr": 30 / 100}},
        "elements_event": [
            {
                "field": {
                    "file": field_file,
                    "selection": {
                        "slice": {"valid_time": ["20191210T010000", "20191210T030000"]}
                    },
                    "grid_name": "mask",
                    "name": "field",
                },
                "plain": {"comparison_op": "sup", "threshold": 1, "units": "degC"},
                "category": "quantitative",
                "altitude": {
                    "filename": get_altitude_file(dirname),
                },
                "geos": {"file": get_mask_file(dirname)},
                "aggregation_aval": {
                    "method": "requiredDensity",
                    "kwargs": {"dr": 30 / 100},
                },
                "compute_list": ["density", "extrema", "representative", "summary"],
            },
            {
                "field": {
                    "file": field_file,
                    "selection": {
                        "slice": {"valid_time": ["20191210T010000", "20191210T030000"]}
                    },
                    "grid_name": "mask",
                    "name": "field",
                },
                "plain": {"comparison_op": "infegal", "threshold": 3, "units": "degC"},
                "category": "quantitative",
                "altitude": {
                    "filename": get_altitude_file(dirname),
                },
                "geos": {"file": get_mask_file(dirname)},
                "aggregation_aval": {
                    "method": "requiredDensity",
                    "kwargs": {"dr": 30 / 100},
                },
                "compute_list": ["density", "extrema", "representative", "summary"],
            },
        ],
        "localisation": {
            "compass_split": True,
            "altitude_split": True,
        },
        "compute_list": ["density", "extrema", "representative", "summary"],
    }
    return dict_risk_downstream


def get_downstream_alt(dirname):
    field_file = dirname / "field.nc"
    altitude_file = dirname / "altitude.nc"
    dict_risk = {
        "level": 1,
        "probability": "no",
        "aggregation_type": "downStream",
        "logical_op_list": ["or"],
        "aggregation": {"method": "requiredDensity", "kwargs": {"dr": 63 / 100}},
        "altitude": {
            "filename": altitude_file,
        },
        "elements_event": [
            {
                "field": {
                    "file": field_file,
                    "selection": {
                        "slice": {"valid_time": ["20191210T010000", "20191210T030000"]}
                    },
                    "grid_name": "mask",
                    "name": "field",
                },
                "category": "quantitative",
                "mountain_altitude": 1200,
                "altitude": {
                    "filename": altitude_file,
                },
                "geos": {"file": get_mask_file(dirname)},
                "plain": {"comparison_op": "sup", "threshold": 3, "units": "degC"},
                "mountain": {
                    "comparison_op": "supegal",
                    "threshold": 1,
                    "units": "degC",
                },
                "aggregation_aval": {
                    "method": "requiredDensity",
                    "kwargs": {"dr": 63 / 100},
                },
                "compute_list": ["density", "extrema", "representative", "summary"],
            },
            {
                "field": {
                    "file": field_file,
                    "selection": {
                        "slice": {"valid_time": ["20191210T010000", "20191210T030000"]}
                    },
                    "grid_name": "mask",
                    "name": "field",
                },
                "plain": {"comparison_op": "infegal", "threshold": 0, "units": "degC"},
                "category": "quantitative",
                "altitude": {
                    "filename": altitude_file,
                },
                "geos": {"file": get_mask_file(dirname)},
                "aggregation_aval": {
                    "method": "requiredDensity",
                    "kwargs": {"dr": 63 / 100},
                },
                "compute_list": ["density", "extrema", "representative", "summary"],
            },
        ],
        "localisation": {
            "compass_split": True,
            "altitude_split": True,
        },
        "compute_list": ["density", "extrema", "representative", "summary"],
    }
    return dict_risk


def get_upstream_risk(dirname):
    field_file = dirname / "field.nc"
    dict_risk_upstream = {
        "name": "Vent Moyen",
        "level": 1,
        "probability": "no",
        "aggregation_type": "upStream",
        "logical_op_list": ["and"],
        "elements_event": [
            {
                "field": {
                    "file": field_file,
                    "selection": {
                        "slice": {"valid_time": ["20191210T010000", "20191210T030000"]}
                    },
                    "grid_name": "mask",
                    "name": "field",
                },
                "plain": {"comparison_op": "sup", "threshold": 3, "units": "degC"},
                "aggregation": {"method": "requiredDensity", "kwargs": {"dr": 0.3}},
                "category": "quantitative",
                "geos": {"file": get_mask_file(dirname)},
                "altitude": {
                    "filename": get_altitude_file(dirname),
                },
                "compute_list": ["density", "extrema", "representative", "summary"],
            },
            {
                "field": {
                    "file": field_file,
                    "selection": {
                        "slice": {"valid_time": ["20191210T010000", "20191210T030000"]}
                    },
                    "grid_name": "mask",
                    "name": "field",
                },
                "plain": {
                    "comparison_op": "infegal",
                    "threshold": 2.55,
                    "units": "degC",
                },
                "aggregation": {"method": "mean"},
                "category": "quantitative",
                "geos": {"file": get_mask_file(dirname)},
                "altitude": {
                    "filename": get_altitude_file(dirname),
                },
                "compute_list": ["density", "extrema", "representative", "summary"],
            },
        ],
        "localisation": {
            "compass_split": True,
            "altitude_split": True,
        },
        "compute_list": ["density", "extrema", "representative", "summary"],
    }
    return dict_risk_upstream


bertrand_array1 = np.array(
    [
        [
            [
                False,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ],
            [
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
            ],
        ],
        [
            [
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
            ],
            [
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
            ],
        ],
    ]
)


bertrand_array = np.array(
    [
        [
            [
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                False,
            ],
            [
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
            ],
        ],
        [
            [
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
            ],
            [
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
            ],
        ],
    ]
)


class TestEvent:
    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_event_plain(self, data_dirname: Path):
        """
        Permet de tester si la definition d'un  evenement unitaire se passe bien
        avec un modèle de conf récent utilisant la nouvelle version de config
        Ici on test :
          - le fait de pouvoir aggreger avec ddr et deux densites differentes
          - le fait de pouvoir aggreger avec la moyenne
        """
        event = get_plain_event(data_dirname)
        print(event)
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event = EventComposite(**temp_kwargs)
        assert hasattr(element_event, "field")
        assert hasattr(element_event, "geos")

        da_risk = element_event.compute()
        assert da_risk.shape == (2, 2)
        assert np.all(da_risk.values == np.array([[False, True], [True, True]]))

        # On test avec un autre threshold
        event_bis = get_plain_event(data_dirname)
        event_bis["aggregation"] = {"method": "requiredDensity", "kwargs": {"dr": 0.68}}
        temp_kwargs_bis = {}
        temp_kwargs_bis.update(**event_bis)
        temp_kwargs_bis.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event_bis = EventComposite(**temp_kwargs_bis)
        da_risk_bis = element_event_bis.compute()
        assert np.all(da_risk_bis.values == np.array([[False, False], [False, True]]))

        # On test une methode d'aggregation before
        event_plain = get_plain_event(data_dirname)
        event_plain["aggregation"] = {"method": "mean"}
        temp_kwargs_plain = {}
        temp_kwargs_plain.update(**event_plain)
        temp_kwargs_plain.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event_plain = EventComposite(**temp_kwargs_plain)

        da_plain = element_event_plain.compute()
        assert da_plain.shape == (2, 2)
        logging.info(da_plain.values)
        assert np.all(da_plain.values == np.array([[False, False], [True, True]]))

    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_weighted_plain(self, data_dirname: Path):
        """
        Permet de tester si la definition d'un  evenement unitaire se passe bien
        avec un modèle de conf récent utilisant la nouvelle version de config
        Ici on test la densité pondérée et conditionnelle
        """
        event = get_plain_weighted(data_dirname)
        event.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event = EventComposite(**event)
        da_risk = element_event.compute()
        assert np.all(da_risk.values == np.array([[True, False], [True, True]]))

        # On change de seuil pour qu'il n'y ai aucun risque allumé
        event_bis = get_plain_weighted(data_dirname)
        event_bis.update({"geos": {"file": get_mask_file(data_dirname)}})
        event_bis["aggregation"]["kwargs"]["dr"] = 0.94
        element_event_bis = EventComposite(**event_bis)
        da_risk = element_event_bis.compute()
        assert np.all(da_risk.values == np.array([[False, False], [False, False]]))

        # On passe en conditionnelle
        event_cond = get_plain_weighted(data_dirname)
        event_cond.update({"geos": {"file": get_mask_file(data_dirname)}})
        event_cond["aggregation"]["method"] = "requiredDensityConditional"
        fcentral = data_dirname / "central_mask.nc"
        event_cond["aggregation"]["kwargs"] = {
            "dr": 0.94,
            "central_mask_id": {"file": fcentral, "mask_id": "Central"},
        }
        element_event_cond = EventComposite(**event_cond)
        da_risk = element_event_cond.compute()
        assert np.all(da_risk.values == np.array([[True, False], [True, False]]))

    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_retour_plain(self, data_dirname: Path):
        """
        On test ici les retours pour un evt sur la plaine
        avec un modèle de conf récent utilisant la nouvelle version de config
        """
        event = get_plain_event(data_dirname)
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event = EventComposite(**temp_kwargs)
        element_event.compute()
        da_plain = element_event.values_ds

        # On va verifier les cles dans le dataset
        assert hasattr(da_plain, "min_plain")
        assert hasattr(da_plain, "rep_value_plain")
        assert hasattr(da_plain, "density")
        assert hasattr(da_plain, "occurrence_event")
        assert np.all(
            da_plain["rep_value_plain"].values.round(4) == np.array([[1, 2], [4, 4]])
        )
        assert np.all(
            da_plain["min_plain"].values.round(4) == np.array([[-2, -2], [0, 0]])
        )
        assert da_plain["units"] == "°C"
        assert np.all(
            da_plain["density"].values.round(4)
            == np.array([[0.28666667, 0.32923077], [0.67666667, 0.68615385]]).round(4)
        )

    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_event_mountain(self, data_dirname: Path):
        """
        On va tester les evenements en considerant qu'on a une montagne a 1200m.
        Le modèle de conf est récent et utilise la nouvelle version de config
        """
        event = get_mountain_event(data_dirname)
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event = EventComposite(**temp_kwargs)
        logging.error(str(element_event))
        da_risk = element_event.compute()
        assert np.all(da_risk.values == np.array([[True, False], [True, True]]))

        # On change le threshold en montagne et on change de densite requise
        event = get_mountain_event(data_dirname)
        event["mountain"]["threshold"] = -1.0
        event["aggregation"]["kwargs"]["dr"] = 0.3
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event = EventComposite(**temp_kwargs)
        logging.error(str(element_event))
        da_risk = element_event.compute()
        assert np.all(da_risk.values == np.array([[False, True], [True, True]]))

        # On change de methode (on passe a la moyenne)
        event = get_mountain_event(data_dirname)
        event["aggregation"] = {"method": "mean"}
        event["mountain"]["threshold"] = 0.6
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event = EventComposite(**temp_kwargs)
        logging.error(str(element_event))
        da_risk = element_event.compute()
        assert np.all(da_risk.values == np.array([[False, True], [True, True]]))

        # On change de threshold en montagne et on regarde si tout fonctionne encore.
        event = get_mountain_event(data_dirname)
        event["aggregation"] = {"method": "mean"}
        event["mountain"]["threshold"] = 1
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event = EventComposite(**temp_kwargs)
        logging.error(str(element_event))
        da_risk = element_event.compute()
        assert np.all(da_risk.values == np.array([[False, False], [True, True]]))

    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_retour_montain(self, data_dirname: Path):
        event = get_mountain_event(data_dirname)
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event = EventComposite(**temp_kwargs)
        element_event.compute()
        da = element_event.values_ds
        assert hasattr(da, "min_plain")
        assert hasattr(da, "min_mountain")
        assert hasattr(da, "rep_value_plain")
        assert hasattr(da, "rep_value_mountain")
        assert hasattr(da, "density")
        assert np.all(
            da["density"].values.round(4)
            == np.array([[0.10333333, 0.08307692], [0.46333333, 0.46153846]]).round(4)
        )
        assert np.all(
            da["min_mountain"].values.round(4) == np.array([[-2, -2], [0, 0]]).round(4)
        )
        assert np.all(
            da["min_plain"].values.round(4) == np.array([[-2, -2], [0, 0]]).round(4)
        )
        assert np.all(
            da["rep_value_plain"].values.round(4) == np.array([[3, 3], [5, 5]]).round(4)
        )
        assert np.all(
            da["rep_value_mountain"].values.round(4)
            == np.array([[3, 3], [5, 5]]).round(4)
        )

        # On regarde si ca fonctionne aussi pour la moyenne
        event = get_mountain_event(data_dirname)
        event["aggregation"] = {"method": "mean"}
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update({"geos": {"file": get_mask_file(data_dirname)}})
        element_event = EventComposite(**temp_kwargs)
        element_event.compute()
        da = element_event.values_ds
        assert np.all(
            da["rep_value_mountain"].values.round(4)
            == np.array([[0.5502, 0.7162], [2.4168, 2.3752]], dtype=np.float32).round(4)
        )
        assert np.all(
            da["rep_value_plain"].values.round(4)
            == np.array([[0.391, 0.4593], [2.5118, 2.6407]], dtype=np.float32).round(4)
        )

    @pytest.mark.filterwarnings("ignore: invalid value")
    @pytest.mark.filterwarnings("ignore: All-Nan")
    def test_event_bertrand(self, data_dirname: Path):
        """
        On va tester bertrand
        Avec un modèle de conf récent utilisant la nouvelle version de config
        """
        event = get_bertrand_event(data_dirname)
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update(
            {"process": "Bertrand", "geos": {"file": get_RR_mask(data_dirname)}}
        )
        element_event = EventBertrandComposite(**temp_kwargs)
        da_risk = element_event.compute()
        assert np.all(da_risk.isel(id=0).values == bertrand_array1)

        # On test un second risque (cette fois ci avec un niveau plus faible)
        event = get_bertrand_event(data_dirname)
        event["plain"]["threshold"] = 5
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update(
            {"process": "Bertrand", "geos": {"file": get_RR_mask(data_dirname)}}
        )
        element_event = EventBertrandComposite(**temp_kwargs)
        da_risk = element_event.compute()
        assert np.all(da_risk.isel(id=0).values == bertrand_array)

    @pytest.mark.filterwarnings("ignore: invalid value")
    @pytest.mark.filterwarnings("ignore: All-Nan")
    def test_event_bertrand_from_RR3(self, data_dirname: Path):
        # On test si on se base sur des RR3
        event = get_bertrand_event_from_RR3(data_dirname)
        event.update(
            {"process": "Bertrand", "geos": {"file": get_RR_mask(data_dirname)}}
        )
        element_event = EventBertrandComposite(**event)
        da_risk = element_event.compute()
        assert np.all(
            da_risk.isel(id=0).values
            == np.array(
                [
                    [[True, True, False, False], [False, False, False, False]],
                    [[True, True, False, False], [True, True, False, False]],
                ]
            )
        )

    @pytest.mark.filterwarnings("ignore: invalid value")
    @pytest.mark.filterwarnings("ignore: All-Nan")
    def test_mean_bertrand(self, data_dirname: Path):
        event = get_mean_bertrand_event(data_dirname)
        event["plain"]["threshold"] = 5
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update(
            {"process": "Bertrand", "geos": {"file": get_RR_mask(data_dirname)}}
        )
        element_event = EventBertrandComposite(**temp_kwargs)
        da_risk = element_event.compute()
        assert np.all(
            da_risk.values
            == np.array(
                [
                    [False, True],
                    [True, True],
                    [True, True],
                    [True, True],
                    [True, True],
                    [True, True],
                    [True, True],
                    [True, True],
                    [True, True],
                    [True, True],
                    [True, True],
                    [False, True],
                    [False, False],
                ]
            )
        )
        # On va tester valeur représentative et valeurs extremes
        da = element_event.values_ds
        assert np.all(
            da["rep_value_plain"].values.round(4)
            == np.array(
                [
                    [24.75, 28.0],
                    [24.75, 28.0],
                    [24.75, 28.0],
                    [24.75, 28.0],
                    [24.75, 28.0],
                    [24.75, 28.0],
                    [24.25, 27.0],
                    [18.0, 17.0],
                    [14.5, 16.0],
                    [11.75, 16.0],
                    [10.5, 16.0],
                    [8.75, 14.0],
                    [8.5, 14.0],
                ]
            )
        )

        assert np.all(
            da["max_plain"].values
            == np.array(
                [
                    [28.0, 28.0],
                    [28.0, 28.0],
                    [28.0, 28.0],
                    [28.0, 28.0],
                    [28.0, 28.0],
                    [28.0, 28.0],
                    [27.0, 27.0],
                    [21.0, 17.0],
                    [16.0, 16.0],
                    [16.0, 16.0],
                    [16.0, 16.0],
                    [14.0, 14.0],
                    [14.0, 14.0],
                ]
            )
        )

        assert np.all(
            da["min_plain"].values
            == np.array(
                [
                    [18.0, 28.0],
                    [18.0, 28.0],
                    [18.0, 28.0],
                    [18.0, 28.0],
                    [18.0, 28.0],
                    [18.0, 28.0],
                    [18.0, 27.0],
                    [17.0, 17.0],
                    [10.0, 16.0],
                    [6.0, 16.0],
                    [4.0, 16.0],
                    [1.0, 14.0],
                    [1.0, 14.0],
                ]
            )
        )

    @pytest.mark.filterwarnings("ignore: invalid value")
    @pytest.mark.filterwarnings("ignore: All-Nan")
    def test_drr_bertrand(self, data_dirname: Path):
        event = get_drr_bertrand_event(data_dirname)
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update(
            {"process": "Bertrand", "geos": {"file": get_RR_mask(data_dirname)}}
        )
        element_event = EventBertrandComposite(**temp_kwargs)
        da_risk = element_event.compute()
        assert np.all(
            da_risk.isel(id=0).values
            == np.array(
                [
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                ]
            )
        )
        assert np.all(
            da_risk.isel(id=1).values
            == np.array(
                [
                    False,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                ]
            )
        )
        da = element_event.values_ds
        assert np.all(
            da["rep_value_plain"].values.round(4)
            == np.array(
                [
                    [23.04, 28.0],
                    [23.04, 28.0],
                    [23.04, 28.0],
                    [23.04, 28.0],
                    [23.04, 28.0],
                    [23.04, 28.0],
                    [23.04, 27.0],
                    [17.0, 17.0],
                    [14.32, 16.0],
                    [8.16, 16.0],
                    [5.44, 16.0],
                    [4.6, 14.0],
                    [3.88, 14.0],
                ]
            ).round(4)
        )

        event = get_drr_bertrand_event(data_dirname)
        event["plain"]["threshold"] = 5
        temp_kwargs = {}
        temp_kwargs.update(**event)
        temp_kwargs.update(
            {"process": "Bertrand", "geos": {"file": get_RR_mask(data_dirname)}}
        )
        element_event = EventBertrandComposite(**temp_kwargs)
        da_risk = element_event.compute()
        assert np.all(
            da_risk.isel(id=0).values
            == np.array(
                [
                    False,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    False,
                    False,
                    False,
                    False,
                ]
            )
        )
        assert np.all(
            da_risk.isel(id=1).values
            == np.array(
                [
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    False,
                ]
            )
        )


class TestRisk:
    @pytest.fixture(scope="class")
    def data_dirname(self, working_dir):
        return working_dir / "data"

    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_downstream(self, data_dirname: Path):
        dict_risk = get_downstream_risk(data_dirname)
        dict_risk.update(
            {
                "geos": {"file": get_mask_file(data_dirname)},
            }
        )
        risk_handler = LevelComposite(**dict_risk)
        dout = risk_handler.compute()
        print(dout)
        drisk = dout["occurrence"]
        assert np.all(drisk.values == np.array([[False, True], [True, True]]))

        # Be carreful : the density is computed for each event (and not for the
        # event combination)
        assert np.all(
            dout["risk_density"].values.round(4)
            == np.array([[0.28666667, 0.32923077], [0.36333333, 0.33846154]]).round(4)
        )
        # Densite de chaque evenement maintenant
        assert np.all(
            dout["density"].values.round(4)
            == np.array(
                [
                    [[0.28666667, 0.32923077], [0.67666667, 0.68615385]],
                    [[1.0, 1.0], [0.68666667, 0.65230769]],
                ]
            ).round(4)
        )
        # Valeurs representative sur la plaine
        assert np.all(
            dout["rep_value_plain"].values.round(4)
            == np.array([[[1, 2], [4, 4]], [[-1, 0], [1, 1]]]).round(4)
        )
        # Mini et maxi
        assert np.all(
            dout["max_plain"].values.round(4)
            == np.array([[[3, 3], [5, 5]], [[3, 3], [5, 5]]]).round(4)
        )
        assert np.all(
            dout["min_plain"].values.round(4)
            == np.array([[[-2, -2], [0, 0]], [[-2, -2], [0, 0]]]).round(4)
        )

        # On test maintenant avec une aggregation par la moyenne
        dict_risk = get_downstream_risk(data_dirname)
        dict_risk.update(
            {
                "geos": {"file": get_mask_file(data_dirname)},
            }
        )
        dict_risk["aggregation"] = {"method": "mean"}
        for elt in dict_risk["elements_event"]:
            elt["aggregation_aval"] = {"method": "mean"}

        risk_handler = LevelComposite(**dict_risk)
        dout = risk_handler.compute()
        drisk = dout["occurrence"]
        assert np.all(
            dout["rep_value_plain"].values.round(4)
            == np.array(
                [
                    [[0.4225, 0.5284], [2.4925, 2.5684]],
                    [[0.4225, 0.5284], [2.4925, 2.5684]],
                ],
                dtype=np.float32,
            ).round(4)
        )

    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_upstream(self, data_dirname: Path):
        dict_risk = get_upstream_risk(data_dirname)
        dict_risk.update(
            {
                "geos": {"file": get_mask_file(data_dirname)},
            }
        )
        risk_handler = LevelComposite(**dict_risk)
        dout = risk_handler.compute()
        drisk = dout["occurrence"]
        assert np.all(drisk.values == np.array([[False, False], [True, False]]))
        assert np.all(
            dout["density"].values.round(4)
            == np.array(
                [
                    [[0.0, 0.0], [0.31333333, 0.34769231]],
                    [[0.86666667, 0.87384615], [0.49, 0.46769231]],
                ]
            ).round(4)
        )
        assert np.all(
            dout["rep_value_plain"].values.round(4)
            == np.array(
                [[[1.0, 2.0], [4.0, 4.0]], [[0.4225, 0.5284], [2.4925, 2.5684]]]
            ).round(4)
        )

    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_downstream_alt(self, data_dirname: Path):
        dict_risk = get_downstream_alt(data_dirname)
        dict_risk.update(
            {
                "geos": {"file": get_mask_file(data_dirname)},
            }
        )
        risk_handler = LevelComposite(**dict_risk)
        dout = risk_handler.compute()
        drisk = dout["occurrence"]
        assert np.all(drisk.values == np.array([[False, True], [False, True]]))
        assert np.all(
            dout["density"].values.round(4)
            == np.array(
                [
                    [[0.1, 0.14769231], [0.42666667, 0.50769231]],
                    [[0.52, 0.49230769], [0.17, 0.16]],
                ]
            ).round(4)
        )
        assert np.all(
            dout.rep_value_mountain.isel(evt=0).values.round(4)
            == np.array([[0, 0], [2, 2]]).round(4)
        )
        assert np.all(
            dout.rep_value_plain.values.round(4)
            == np.array([[[0, 0], [2, 2]], [[1, 1], [3, 3]]]).round(4)
        )
