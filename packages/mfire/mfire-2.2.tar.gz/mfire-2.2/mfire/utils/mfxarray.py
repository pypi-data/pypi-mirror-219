"""
interface au module xarray
toutes les fonctions,méthodes, attributs
apportés par xarray sont distribués à partir d'ici
ainsi partout ailleurs dans le code
il ne doit plus y avoir d'appel direct à xarray
cela permet de contrôler le comportement de xarray
notamment pour  datarray.where
"""
import xarray as xr


@xr.register_dataarray_accessor("wheretype")
class TypeAccessor:
    """
    Ajout un attribut wheretype aux datarray
    et les méthodes suivantes
    qui permettent de convertir le résultat d'un where dans le type souhaité
    """

    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    def bool(self, *args, **kwargs):
        return self._obj.where(*args, **kwargs).astype("bool", copy=False)

    def f32(self, *args, **kwargs):
        return self._obj.where(*args, **kwargs).astype("float32", copy=False)


DataArray = xr.DataArray
Dataset = xr.Dataset
merge = xr.merge
"""
remplacé en utilisant l'équivalent numpy
fmax = xr.ufuncs.fmax
"""
align = xr.align
apply_ufunc = xr.apply_ufunc
concat = xr.concat
"""
remplacé directement par xr.DataArray dans le code l'utilisant
xda = xr.core.dataarray.DataArray
"""
ones_like = xr.ones_like
open_dataarray = xr.open_dataarray
open_dataset = xr.open_dataset
set_options = xr.set_options
