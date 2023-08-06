"""Tests for .helper functions."""
from pathlib import Path
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory
from typing import Any

import geopandas as gpd  # type: ignore
import numpy as np
import pandas as pd  # type: ignore
import pytest
import xarray as xr

from gdptools import AggGen
from gdptools import ClimRCatData
from gdptools import UserCatData
from gdptools import WeightGen

gm_vars = ["tmmn", "tmmx", "pr"]


@pytest.fixture
def climr_dict(vars: list[str] = gm_vars) -> dict[str, Any]:
    """Return parameter json."""
    climater_cat = "https://mikejohnson51.github.io/climateR-catalogs/catalog.parquet"
    cat = pd.read_parquet(climater_cat)

    _id = "gridmet"  # noqa
    var_params = [
        cat.query(
            "id == @_id & variable == @_var", local_dict={"_id": _id, "_var": _var}
        ).to_dict(orient="records")[0]
        for _var in vars
    ]
    return dict(zip(vars, var_params))  # noqa B905


@pytest.fixture()
def get_gdf() -> gpd.GeoDataFrame:
    """Create GeoDataFrame."""
    return gpd.read_file("./tests/data/DRB/DRB_4326.shp")


@pytest.fixture()
def get_xarray() -> xr.Dataset:
    """Create xarray Dataset."""
    return xr.open_dataset("./tests/data/DRB/o_of_b_test.nc")


@pytest.fixture()
def get_file_path(tmp_path: Path) -> Path:
    """Get temp file path."""
    return tmp_path / "test.csv"


@pytest.fixture()
def get_out_path(tmp_path: Path) -> Path:
    """Get temp file output path."""
    return tmp_path


data_crs = 4326
x_coord = "lon"
y_coord = "lat"
t_coord = "time"
sdate = "2021-01-01"
edate = "2021-01-31"
var = ["Tair"]
shp_crs = 4326
shp_poly_idx = "huc12"
wght_gen_crs = 6931


def test_serial_climrcatdata(climr_dict, get_gdf, get_out_path):
    """Test Serial versions."""
    user_data = ClimRCatData(
        cat_dict=climr_dict,
        f_feature=get_gdf,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )
    tempfile = NamedTemporaryFile()
    wght_gen = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=tempfile.name,  # type: ignore
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="csv",
        weights=tempfile.name,
        out_path=tmpdir.name,
        file_prefix="gm_drb_test",
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # np.savez(
    #     "./tests/data/DRB/gm_drb.npz",
    #     tmin=_df.daily_minimum_temperature.values,
    #     tmax=_df.daily_maximum_temperature.values,
    #     pr=_df.precipitation_amount.values,
    # )

    test_data = np.load("./tests/data/DRB/gm_drb.npz")

    np.testing.assert_allclose(
        _df.daily_maximum_temperature.values,
        test_data["tmax"],
        rtol=1e-4,
        verbose=True,
    )

    np.testing.assert_allclose(
        _df.daily_minimum_temperature.values,
        test_data["tmin"],
        rtol=1e-4,
        verbose=True,
    )

    np.testing.assert_allclose(
        _df.precipitation_amount.values,
        test_data["pr"],
        rtol=1e-4,
        verbose=True,
    )
    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_df, xr.Dataset)

    ofile = get_out_path / tempfile.name
    assert ofile.exists()


def test_serial_usercatdata(get_xarray, get_gdf, get_out_path):
    """Test Serial versions."""
    sdate = "2021-01-01T00:00"
    edate = "2021-01-01T02:00"
    user_data = UserCatData(
        ds=get_xarray,
        proj_ds=data_crs,
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        var=var,
        f_feature=get_gdf,
        proj_feature=shp_crs,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )  # type: ignore

    tempfile = NamedTemporaryFile()

    wght_gen = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=tempfile.name,  # type: ignore
        weight_gen_crs=wght_gen_crs,
    )

    _wghts = wght_gen.calculate_weights()

    assert isinstance(_wghts, pd.DataFrame)

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_mean",
        agg_engine="serial",
        agg_writer="csv",
        weights=tempfile.name,
        out_path=tmpdir.name,
        # weights=tempfile.name,
        # out_path="./tests/data/DRB/",
        file_prefix="tair",
    )

    _ngdf, _df = agg_gen.calculate_agg()

    # np.savez(
    #     "./tests/data/DRB/user_drb_usercatdata.npz",
    #     Tair=_df.Tair.values
    # )

    test_data = np.load("./tests/data/DRB/user_drb_usercatdata.npz")

    np.testing.assert_allclose(
        _df.Tair.values,
        test_data["Tair"],
        rtol=1e-4,
        verbose=True,
    )

    assert isinstance(_ngdf, gpd.GeoDataFrame)
    assert isinstance(_df, xr.Dataset)

    ofile = get_out_path / tempfile.name
    assert ofile.exists()
