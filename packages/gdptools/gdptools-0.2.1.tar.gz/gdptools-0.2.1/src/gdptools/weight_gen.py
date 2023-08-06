"""Calculate weights."""
import time
from typing import Any
from typing import Literal
from typing import Optional
from typing import Union

import geopandas as gpd
import pandas as pd

from gdptools.data.user_data import UserData
from gdptools.data.weight_gen_data import WeightData
from gdptools.weights.calc_weight_engines import DaskWghtGenEngine
from gdptools.weights.calc_weight_engines import ParallelWghtGenEngine
from gdptools.weights.calc_weight_engines import SerialWghtGenEngine

WEIGHT_GEN_METHODS = Literal["serial", "parallel", "dask"]
""" Methods used in WghtGen class.

seerial: Iterates through polygons to calculate weights.  Sufficient for most cases.
parallel: Chunks polygons and distributes to available processors.  Provides a
substantial speedup when there is a large number of polygons.

Raises:
    TypeError: If value is not one of "serial" or "parallel".

Returns:
    _type_: str
"""


class WeightGen:
    """Class for weight calculation."""

    def __init__(
        self,
        *,
        user_data: UserData,
        method: WEIGHT_GEN_METHODS,
        weight_gen_crs: Any,
        output_file: Optional[Union[str, None]] = None,
        jobs: Optional[int] = -1,
        verbose: Optional[bool] = False,
    ) -> None:
        """Weight generation class.

        The WeightGen class is used to calculate weights for a given :class:`UserData`
        object.  Once initialized the The weights are calculated via the
        :meth:`calculate_weights` method.  The weights are returned as a pandas
        DataFrame and can be optionally save to a .csv file.  The DataFrame has the
        following columns:
        * target_id: The target polygon id
        * i_index The i index of the source grid
        * j_index The j index of the source grid
        * weight: The calculated weight for the target/source pair
        As long as the source grid and targe polygons remain the same, the weights file
        can be saved and reused for future calculations, for example if the user wants
        a different variable or statistic and does not want to recalculate the weights.

        Args:
            user_data (UserData): One of :class:`UserCatData`, :class:`ODAPCatData`,
                :class:`ClimateCatData`
            method (WEIGHT_GEN_METHODS): One of :data:`WEIGHT_GEN_METHODS`
            weight_gen_crs (Any): Any projection that can be used by
                pyproj.CRS.from_user_input
            output_file (Optional[Union[str, None]], optional): Sting of the
                /path/to/file or None if no output is desired. Defaults to None.
            jobs (Optional[int], optional): Optional, number of processors used in
                parallel or dask methods (dask uses dask bag). If set to default value
                (-1) jobs is defined as the number of processors available/2.
                In this case, because the data needs to be distributed amoung processors
                choosing half the processors available is a reasonable choice. Defaults
                to -1.
            verbose (Optional[bool], optional): If True then extra output is printed.
                Defaults to False.

        Raises:
            TypeError: If one of the method arguments does not match
                :data:`WEIGHT_GEN_METHODS`

        """
        self.user_data = user_data
        self.method = method
        if output_file is None:
            self.output_file = ""
        else:
            self.output_file = output_file
        self.weight_gen_crs = weight_gen_crs
        self.jobs = jobs
        self.verbose = verbose
        self._intersections: gpd.GeoDataFrame
        self.__calc_method: Union[
            SerialWghtGenEngine, ParallelWghtGenEngine, DaskWghtGenEngine
        ]
        if self.method == "serial":
            self.__calc_method = SerialWghtGenEngine()
            print("Using serial engine")
        elif self.method == "parallel":
            self.__calc_method = ParallelWghtGenEngine()
            print("Using parallel engine")
        elif self.method == "dask":
            self.__calc_method = DaskWghtGenEngine()
        else:
            raise TypeError(f"method: {self.method} not in [serial, parallel]")

    def calculate_weights(self, intersections: bool = False) -> pd.DataFrame:
        """Calculate weights.

        Args:
            intersections (bool): _description_. Defaults to False.

        Returns:
            pd.DataFrame: _description_
        """
        tstrt = time.perf_counter()
        self._weight_data: WeightData = self.user_data.prep_wght_data()
        tend = time.perf_counter()
        print(f"Data preparation finished in {tend - tstrt:0.4f} seconds")
        if intersections:
            print("Saving interesections in weight generation.")
            weights, self._intersections = self.__calc_method.calc_weights(
                target_poly=self._weight_data.feature,
                target_poly_idx=self._weight_data.id_feature,
                source_poly=self._weight_data.grid_cells,
                source_poly_idx=["i_index", "j_index"],
                source_type="grid",
                wght_gen_crs=self.weight_gen_crs,
                filename=self.output_file,
                intersections=intersections,
                jobs=self.jobs,
                verbose=self.verbose,
            )
        else:
            weights = self.__calc_method.calc_weights(
                target_poly=self._weight_data.feature,
                target_poly_idx=self._weight_data.id_feature,
                source_poly=self._weight_data.grid_cells,
                source_poly_idx=["i_index", "j_index"],
                source_type="grid",
                wght_gen_crs=self.weight_gen_crs,
                filename=self.output_file,
                intersections=intersections,
                jobs=self.jobs,
                verbose=self.verbose,
            )
        return weights

    @property
    def grid_cells(self) -> gpd.GeoDataFrame:
        """Return grid_cells."""
        if self._weight_data.grid_cells is None:
            print("grid_cells not calculated yet. Run calculate_weights().")
        return self._weight_data.grid_cells

    @property
    def intersections(self) -> gpd.GeoDataFrame:
        """Return intersections."""
        if self._intersections is None:
            print(
                "intersections not calculated, "
                "Run calculate_weights(intersectiosn=True)"
            )
        return self._intersections
