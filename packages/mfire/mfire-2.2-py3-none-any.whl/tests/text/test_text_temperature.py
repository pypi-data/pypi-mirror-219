from pathlib import Path

from mfire.composite import WeatherComposite
from mfire.settings import TEMPLATES_FILENAMES, Settings
from mfire.text.temperature import (
    TemperatureBuilder,
    TemperatureReducer,
    TemperatureSelector,
)
from mfire.text.text_manager import TextManager
from mfire.utils import JsonFile, recursive_format

# ==============================
# Testing a Text SYNTHESIS
# ==============================

path = Path(
    "./data/20210916T0000/promethee/FRANXL1S100/R_SN_DRIFT__SOL.0016_0048_0001.netcdf"
)

ROOT_DIR = Path(__file__).absolute().parent.parent
TEST_DATA_DIR = ROOT_DIR / "test_data/text_tempe"

TEMPLATES = JsonFile(
    TEMPLATES_FILENAMES[Settings().language]["synthesis"]["temperature"]
).load()


def test_component():
    """
    teste la validité d'un objet composant type texte à partir d'un fichier json
    """
    data = recursive_format(
        JsonFile(TEST_DATA_DIR / "config.promethee-prod_temperature.json").load(),
        values={
            "altitudes_dir": Settings().altitudes_dirname,
            "test_data_dir": TEST_DATA_DIR,
        },
    )
    component = data["e1d59d7a-8bc3-4ad6-b7ff-a8c9db091ee3"]["components"][0]
    weather_compo = component["weathers"][0]

    # génération du texte de synthèses
    text_manager = TextManager(component=component)
    # the geos netcdf only contains one mask and this masks only contains
    # one point with the coordinates (longitude=1.44, latitude=43.62)
    generated_text = text_manager.compute(geo_id="c7930c74-845e-4f26-b1cc-66d95d87f105")

    # recherche de la clé pour trouver les différents synonymes possibles
    selector = TemperatureSelector()
    builder = TemperatureBuilder()
    reducer = TemperatureReducer()
    compo = WeatherComposite(**weather_compo)
    builder.reduction = reducer.compute(compo=compo)
    key = builder.find_template_key(selector)

    # we wanna make sure the template keys haven't changed
    assert (
        key == "P1_Z0_1_MIN_1_MAX"
    ), f"Wrong key: expected P1_Z0_1_MIN_1_MAX, got {key}"

    # these are the min and max temperate values
    # at the single coordinante that is in the mask
    tn = "4"
    tx = "10"

    text_from_template = TEMPLATES[key][0]
    period = "De cet après-midi à demain à la mi-journée"
    text_from_template = text_from_template.replace("{period}", period)
    text_from_template = text_from_template.replace("{general_tempe_mini_high_min}", tn)
    text_from_template = text_from_template.replace("{general_tempe_mini_high_max}", tn)
    text_from_template = text_from_template.replace("{general_tempe_unit}", "°C")
    text_from_template = text_from_template.replace("{general_tempe_maxi_high_min}", tx)
    text_from_template = text_from_template.replace("{general_tempe_maxi_high_max}", tx)
    text_from_template = text_from_template + "\n"

    # we apply the postprocessing to the text generated from the template
    builder.text = text_from_template
    builder.post_process()
    text_from_template = builder.text
    assert (
        generated_text == f"De vendredi 12 16h à samedi 13 15h :\n{text_from_template}"
    )


def test_component_condition():
    """
    teste la validité d'un objet composant type texte avec une condition
    à partir d'un fichier json
    """
    data: dict = recursive_format(
        JsonFile(
            str(TEST_DATA_DIR / "config.promethee-prod_temperature_condition.json")
        ).load(),
        values={
            "altitudes_dir": str(Settings().altitudes_dirname),
            "test_data_dir": str(TEST_DATA_DIR),
        },
    )
    component = data["e1d59d7a-8bc3-4ad6-b7ff-a8c9db091ee3"]["components"][0]

    # génération du texte de synthèses
    text_manager = TextManager(component=component)
    # the geos netcdf only contains one mask and this masks only contains
    # one point with the coordinates (longitude=1.44, latitude=43.62)
    generated_text = text_manager.compute(geo_id="c7930c74-845e-4f26-b1cc-66d95d87f105")

    assert generated_text == "De vendredi 12 16h à samedi 13 15h :\n\n"
