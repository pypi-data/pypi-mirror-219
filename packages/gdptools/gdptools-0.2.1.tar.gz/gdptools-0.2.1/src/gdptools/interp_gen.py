from typing import Literal, Optional, Union
from gdptools.agg.agg_engines import InterpEngine, SerialInterp
from gdptools.data.user_data import UserData

STATSMETHODS = Literal['all', 'mean', 'median', 'std', 'max', 'min']
INTERPENGINES = Literal['serial']
INTERPWRITERS = Literal['csv']

INTERP_ENGINE_TYPES = type(SerialInterp)


class InterpGen:
    """Class for interpolation calculation."""

    def __init__(
            self,
            user_data: UserData,
            pt_spacing: Union[float, int, None],
            stat_method: STATSMETHODS,
            interp_engine: INTERPENGINES,
            interp_writer: INTERPWRITERS,
            mask_data: Union[float, int, None],
            out_path: Optional[Union[str, None]] = None,
            file_prefix: Optional[Union[str, None]] = None,
            append_date: Optional[bool] = False,
            jobs: Optional[int] = -1,
    ) -> None:
        """__init__ Initialize InterpGen class.

        _extended_summary_

        Args:
            user_data (UserData): _description_
            pt_spacing (Union[float, int, None]): _description_
            stat_method (STATSMETHODS): _description_
            interp_engine (INTERPENGINES): _description_
            interp_writer (INTERPWRITERS): _description_
            mask_data (Union[float, int, None]): _description_
            out_path (Optional[Union[str, None]], optional): _description_. Defaults to None.
            file_prefix (Optional[Union[str, None]], optional): _description_. Defaults to None.
            append_date (Optional[bool], optional): _description_. Defaults to False.
            jobs (Optional[int], optional): _description_. Defaults to -1.
        """
        self.user_data = user_data
        self.pt_spacing = pt_spacing
        self.stat_method = stat_method
        self.interp_engine = interp_engine
        self.interp_writer = interp_writer
        self.mask_data = mask_data
        self.out_path = out_path
        self.file_prefix = file_prefix
        self.append_date = append_date
        self.jobs = jobs
        self._set_interp_engine()

    def calculate_interp(self) -> None:
        """Calculate interpolation."""
        self.interp = self.interp().run(
            user_data=self.user_data,
            pt_spacing=self.pt_spacing,
            stat=self.stat_method,
            mask_data=self.mask_data
        )
        self.interp.calculate_interp()

    def _set_interp_engine(self):
        self.interp: INTERP_ENGINE_TYPES

        engines = {"serial": InterpEngine}
        try:
            self.interp = engines[self.interp_engine]
        except Exception as exc:
            raise TypeError(
                f"interp_engine: {self.interp_engine} not in {INTERPENGINES}"
            ) from exc

    def _set_writer(self):
        if self._agg_writer != "none" and (
            (self._out_path is None) or (self._file_prefix is None)
        ):
            raise ValueError(
                f"If agg_writer not none, then out_path: {self._out_path}"
                f" and file_prefix: {self._file_prefix} must be set."
            )
        self.__writer: WRITER_TYPES

        if self._agg_writer == "none":
            self.__writer = None
        else:
            writers = {
                "csv": CSVWriter,
                "parquet": ParquetWriter,
                "netcdf": NetCDFWriter,
                "json": JSONWriter,
            }
            try:
                self.__writer = writers[self._agg_writer]
            except Exception as exc:
                raise TypeError(
                    f"agg_writer: {self._agg_writer} not in {AGGWRITERS}"
                ) from exc