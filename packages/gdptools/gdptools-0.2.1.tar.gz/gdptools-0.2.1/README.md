# Readme

[![PyPI](https://img.shields.io/pypi/v/gdptools.svg)](https://pypi.org/project/gdptools/)
[![conda](https://anaconda.org/conda-forge/gdptools/badges/version.svg)](https://anaconda.org/conda-forge/gdptools)
[![Latest Release](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/badges/release.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/releases)

[![Status](https://img.shields.io/pypi/status/gdptools.svg)](https://pypi.org/project/gdptools/)
[![Python Version](https://img.shields.io/pypi/pyversions/gdptools)](https://pypi.org/project/gdptools)

[![License](https://img.shields.io/pypi/l/gdptools)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)

[![Read the documentation at https://gdptools.readthedocs.io/](https://img.shields.io/readthedocs/gdptools/latest.svg?label=Read%20the%20Docs)](https://gdptools.readthedocs.io/)
[![pipeline status](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/pipeline.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)
[![coverage report](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/coverage.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://code.usgs.gov/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://code.usgs.gov/psf/black)
[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)
[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)

## Welcome

Welcome to gdptools, a python package for grid- or polyon-to-polygon area-weighted interpolation statistics.

![Welcome figure](./docs/assets/Welcom_fig.png)

<figcaption>Example grid-to-polygon interpolation.  A) Huc12 basins for Delaware River Watershed. B) Gridded monthly water evaporation amount (mm) from TerraClimate dataset. C) Area-weighted-average interpolation of gridded TerraClimate data to Huc12 polygons.</figcaption>

## Documentation

[gdptools documentation](https://gdptools.readthedocs.io/en/latest/)

## Features

- Grid-to-polygon interpolation of area-weighted statistics.
- Use [Mike Johnson's OPeNDAP catalog][1] to access over 1700 unique datasets.
- Use any gridded dataset that can be read by xarray.
- Uses spatial index methods for improving the efficiency of areal-wieght calculation detailed by [Geoff Boeing][2]

[1]: https://mikejohnson51.github.io/opendap.catalog/articles/catalog.html
[2]: https://geoffboeing.com/2016/10/r-tree-spatial-index-python/

### Example catalog datasets

|                                                                                                | Description                                                                                                                                                                                                                                                                                                    | Dates                      | Links |
| ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----- |
| **[BCCA](https://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#About)**     | Bias Corrected Constructed Analogs V2 Daily Climate Projections (BACA) contains projections of daily BCCA CMIP3 and CMIP5 projections of precipitation, daily maximum, and daily minimum temperature over the contiguous United States                                                                         | 1950 - 2100                |       |
| **[BCSD](https://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#About)**     | Bias Corrected Spatially Downscaled (BCSD) Monthly CMIP5 Climate Projections                                                                                                                                                                                                                                   | 1950 - 2100                |       |
| **[CHIRPS](https://www.chc.ucsb.edu/data/chirps)**                                             | Rainfall Estimates from Rain Gauge and Satellite Observations                                                                                                                                                                                                                                                  | 1980 - Current Month       |       |
| **[Daymet](https://daymet.ornl.gov/)**                                                         | Daymet provides long-term, continuous, gridded estimates of daily weather and climatology variables by interpolating and extrapolating ground-based observations through statistical modeling techniques.                                                                                                      | 1980 through previous year |       |
| **[LOCA](https://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#**About**)** | LOCA, which stands for Localized Constructed Analogs, is a technique for downscaling climate model projections of the future climate.                                                                                                                                                                          | 1950 - 2100                |       |
| **[MACA](https://www.climatologylab.org/maca.html)**                                           | Multivariate Adaptive Constructed Analogs (MACA) is a statistical method for downscaling Global Climate Models (GCMs) from their native coarse resolution to a higher spatial resolution that captures reflects observed patterns of daily near-surface meteorology and simulated changes in GCMs experiments. | 1950-2005 and 2006-2100    |       |
| **[PRISM-Monthly](https://cida.usgs.gov/thredds/catalog.html?dataset=cida.usgs.gov/prism_v2)** | Parameter-elevation Regressions on Independent Slopes                                                                                                                                                                                                                                                          | 1895-2020                  |       |
| **[TerraClimate](https://www.climatologylab.org/terraclimate.html)**                           | TerraClimate is a dataset of monthly climate and climatic water balance for global terrestrial surfaces from 1958-2019. These data provide important inputs for ecological and hydrological studies at global scales that require high spatial resolution and time-varying data.                               | 1958-2020                  |       |
| **[gridMET](https://www.climatologylab.org/gridmet.html)**                                     | daily high-spatial resolution (~4-km, 1/24th degree) surface meteorological data covering the contiguous US                                                                                                                                                                                                    | 1979-yesterday             |       |

## Data Requirements

### Data - xarray (gridded data) and Geopandas (Polygon data)

- [Xarray](https://docs.xarray.dev/en/stable/)

  - Any endpoint that can be read by xarray and contains projected coordinates.
    - The endpoint can be supplied by the OPeNDAP catalog or from a user-supplied end-point.
  - Projection: any projection that can be read by proj.CRS (similar to Geopandas)

- [Geopandas](https://geopandas.org/en/stable/)
  - Any file that can be read by Geopandas
  - Projection: any projection that can be read by proj.CRS

## Installation

You can install _Gdptools_ via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):

        pip install gdptools

or install via [conda](https://anaconda.org/) from [conda-forge](https://anaconda.org/conda-forge/gdptools):

       conda install -c conda-forge gdptools

## Usage

Please see the example notebooks for detailes.

### Catalog Examples

- [OPeNDAP Catalog Example](./docs/terraclime_et.ipynb)

### Non-catalog Examples

- [Non-catalog example - gridMET](./docs/Gridmet_non_catalog.ipynb)
- [Non-catalog example - Merra-2](./docs/Merra-2-example.ipynb)

## Contributing

Contributions are very welcome. To learn more, see the Contributor Guide\_.

## License

Distributed under the terms of the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/legalcode), _Gdptools_ is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/issues) along with a detailed description.

## Credits

This project was generated from [@hillc-usgs](https://code.usgs.gov/hillc-usgs)'s [Pygeoapi Plugin Cookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter) template.
