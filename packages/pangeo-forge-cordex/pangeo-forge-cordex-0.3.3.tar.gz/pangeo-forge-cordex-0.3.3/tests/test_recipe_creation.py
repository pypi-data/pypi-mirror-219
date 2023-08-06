import pytest
import xarray as xr
from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.recipes import XarrayZarrRecipe

from pangeo_forge_cordex import logon, recipe_inputs_from_iids

iids = [
    "cordex.output.EUR-11.DMI.ECMWF-ERAINT.evaluation.r1i1p1.HIRHAM5.v1.mon.tas.v20140620",
    "cordex.output.EUR-11.GERICS.ECMWF-ERAINT.evaluation.r1i1p1.REMO2015.v1.mon.tas.v20180813",
]


@pytest.mark.parametrize("iid", iids)
def test_recipe_inputs(iid):
    sslcontext = logon()

    recipe_inputs = recipe_inputs_from_iids(iid, sslcontext)

    urls = recipe_inputs[iid]["urls"]
    recipe_kwargs = recipe_inputs[iid]["recipe_kwargs"]
    pattern_kwargs = recipe_inputs[iid]["pattern_kwargs"]

    pattern = pattern_from_file_sequence(urls, "time", **pattern_kwargs)
    recipe = XarrayZarrRecipe(
        pattern, xarray_concat_kwargs={"join": "exact"}, **recipe_kwargs
    )

    recipe_pruned = recipe.copy_pruned()
    run_function = recipe_pruned.to_function()

    run_function()

    ds = xr.open_zarr(recipe.target_mapper, consolidated=True)
    print(ds)
