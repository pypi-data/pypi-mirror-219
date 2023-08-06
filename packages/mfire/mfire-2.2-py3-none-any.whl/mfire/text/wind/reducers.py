from mfire.settings import get_logger, TEXT_ALGO
from mfire.text.base import BaseReducer
from mfire.utils.unit_converter import convert_dataarray
from mfire.utils.date import Datetime
from mfire.composite import WeatherComposite

# Logging
LOGGER = get_logger(name="wind_reducer.mod", bind="wind_reducer")


class WindReducer(BaseReducer):
    """Classe Reducer pour le module wind.

    La méthode "compute" ici prend en entrée un "WeatherComposite" contenant
    exactement un "field" "wind".

    Le résumé en sortie a la structure suivante:
    self.summary = {
        "general": {
            "start": <Datetime: date de début>,
            "stop": <Datetime: date de fin>,
            "paramètre": {
                "units": <str: unités>,
                "mini": {
                    "low": <float: valeur basse des minimales>,
                    "high": <float: valeur haute des minimales>,
                },
                "maxi": {
                    "low": <float: valeur basse des maximales>,
                    "high": <float: valeur haute des maximales>,
                }
            }
        },
        "meta": {
            "production_datetime": <Datetime: date de début de production>,
        }
    }
    """

    def init_summary(self) -> None:
        self.summary = {
            "general": {
                "start": "",
                "stop": "",
                "wind": {
                    "units": "",
                    "mini": {
                        "low": None,
                        "high": None,
                    },
                    "maxi": {
                        "low": None,
                        "high": None,
                    },
                },
                "direction": {
                    "units": "",
                    "mini": {
                        "low": None,
                        "high": None,
                    },
                    "maxi": {
                        "low": None,
                        "high": None,
                    },
                },
                "gust": {
                    "units": "",
                    "mini": {
                        "low": None,
                        "high": None,
                    },
                    "maxi": {
                        "low": None,
                        "high": None,
                    },
                },
            },
            "meta": {"production_datetime": ""},
        }

    def get_infos(self, param_da, compo, name) -> None:
        """méthode qui va chercher les informations de min, max, etc..

        Args:
            param_da (dataArray): resultat du compute du composant texte
            compo (weatherComponentComposite): composant texte
            name (str): nom du parametre
        """

        units = compo.units.get(
            name,
            TEXT_ALGO[compo.id][compo.algorithm]["params"][name]["default_units"],
        )

        # on gere les mini
        mini_da = param_da.min("valid_time", keep_attrs=True)
        mini_low = int(convert_dataarray(mini_da.min(keep_attrs=True), units).round())
        mini_high = int(convert_dataarray(mini_da.max(keep_attrs=True), units).round())

        # puis les maxi
        maxi_da = param_da.max("valid_time", keep_attrs=True)
        maxi_low = int(convert_dataarray(maxi_da.min(keep_attrs=True), units).round())
        maxi_high = int(convert_dataarray(maxi_da.max(keep_attrs=True), units).round())

        dico = dict(
            mini=dict(low=mini_low, high=mini_high),
            maxi=dict(low=maxi_low, high=maxi_high),
            units=units,
        )

        self.summary["general"][name] = dico

    def add_general_bloc(self, compo: WeatherComposite) -> None:
        """Méthode qui permet d'ajouter le bloc "general" au self.summary.

        Ce bloc "general" concerne toute la période et toutes les zones et permet
        de calculer les minimales et maximales.
        Args:
            compo (Composite): Composant sur lequels on se base pour produire le texte
        """
        start = []
        stop = []

        for name in compo.params.keys():

            param_da = compo.compute()[name].astype("float16")

            self.get_infos(param_da, compo, name)

            start.append(Datetime(param_da.valid_time.min().values))
            stop.append(Datetime(param_da.valid_time.max().values))

        self.summary["general"]["start"] = min(start)
        self.summary["general"]["stop"] = min(stop)

    def add_metadata(self, compo: WeatherComposite) -> None:
        """Méthode qui ajoute au summary les metadata d'intérêt.
        Args:
            compo (Composite): Composant sur lequels on se base pour produire le texte
        """
        self.summary["meta"]["production_datetime"] = compo.production_datetime

    def compute(self, compo: WeatherComposite, metadata: dict = None) -> dict:
        super().compute(compo=compo)
        self.init_summary()
        self.add_general_bloc(compo)
        self.add_metadata(compo)
        return self.summary
