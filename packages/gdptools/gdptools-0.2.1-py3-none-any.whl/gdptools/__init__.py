"""Top-level package for pygeoapi plugin: Gdptools."""
import logging

from .agg_gen import AggGen
from .agg_gen import InterpGen
from .data.user_data import ClimRCatData
from .data.user_data import ODAPCatData
from .data.user_data import UserCatData
from .data.user_data import UserTiffData
from .weight_gen import WeightGen
from .zonal_gen import ZonalGen

__author__ = "Richard McDonald"
__email__ = "rmcd@usgs.gov"
__version__ = "0.2.1"

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "WeightGen",
    "AggGen",
    "ZonalGen",
    "ODAPCatData",
    "ClimRCatData",
    "UserCatData",
    "InterpGen",
    "UserTiffData",
]
