"""A module defining all Particle classes. Particles are the primary objects for ptm data extraction"""

import numpy as np
from pathlib import Path
import xarray as xr
import pandas as pd
from datetime import datetime as dt
from abc import ABC, abstractmethod
from typing import Union
from types import GeneratorType
#from netCDF4 import Dataset

from tfv.mldatetime import *
from tfv.miscellaneous import Expression


class Particles(ABC):

    def __init__(self,
        file: Union[Path, str, xr.Dataset],
        is_spherical: bool,
        lazy_load: bool,
        warmup: Union[str, pd.Timedelta],
    ):
        """Initializes Extractor object with a ptm results file i.e A TUFLOW FV netCDF4 results file."""

        # Store file path string as attribute
        self.file = file
        self.is_spherical = is_spherical

        # Convert warmup
        if isinstance(warmup, str):
            warmup = pd.Timedelta(warmup)

        # Prepare static Extractor attributes
        self.__prep_file_handle__(lazy_load, warmup)
        self.__prep_2d_geometry__()
        self.__prep_3d_geometry__()

    @abstractmethod
    def get_raw_data(self, variable: str, ii: int):
        """
        Query to extract raw data at a time step (if time-varying).

        Parameters
        ----------
        variable : string
            Name of time varying data set to be extracted.
        ii : integer
            The time vector index at which to extract the data.

        Returns
        -------
        data : np.ndarray
            The raw data as 1D or 2D numpy array
        """
        pass

    @abstractmethod
    def get_mask_vector(self, ii: int):
        """
        Query to extract an array that defines invalid model data.

        Parameters
        ----------
        ii : integer
            Time index at which to extract the mask array.

        Returns
        -------
        mask : np.ndarray
            Logical index, True if model cells/nodes are invalid (i.e dry cells).

        """
        pass

    @abstractmethod
    def get_vertical_selection(self, ii: int, datum: str, limits: tuple):
        """
        Query to extract logical index of particles within a given vertical selection at given time step.

        Parameters
        ----------
        ii : integer
            Time index at which to extract the selection.
        datum : {'sigma', 'depth', 'height', 'elevation'}
            Vertical depth-averaging datum i.e sigma, depth, height, elevation, top, bottom.
        limits : tuple
            Vertical depth-averaging limits (z1, z2) relative to vertical datum.

        Returns
        -------
        lgi : np.ndarray
            A logical index for particles within specified limits. True if particle is in limits.
        """
        pass

    @abstractmethod
    def __prep_file_handle__(self):
        """Command which prepares the file handle for the extractor class"""

    @abstractmethod
    def __prep_time_vector__(self):
        """Command which prepares the result time stamp vector relative to python epoch"""

    @abstractmethod
    def __prep_2d_geometry__(self):
        """Command which prepares the result 2D mesh geometry"""

    @abstractmethod
    def __prep_3d_geometry__(self):
        """Command which prepares the result 2D mesh geometry"""


class FvParticles(Particles):
    """
        Class that extracts particle data from a TUFLOW FV PTM netCDF4 result file.

        Parameters
        ----------
        file : string
            Model result file path.

        Attributes
        ----------
        nt : int
            Number of time steps
        np : int
            Number of particles
        """

    def __init__(self,
        file: Union[Path, str, xr.Dataset],
        lazy_load: bool = True,
        is_spherical: bool = True,
        warmup: Union[str, pd.Timedelta] = "0D",
    ):
        super(FvParticles, self).__init__(file, is_spherical, lazy_load, warmup)

    @property
    def variables(self):
        return [
            x
            for x in self.ds.data_vars.keys()
            if "Time" in self.ds[x].dims
            if x not in ["Time", "stat"]
        ]

    @Expression.decorator
    def get_raw_data(self, variable: str, ii: int):
        if self.ds[variable].ndim > 1:
            return self.ds[variable][ii, :].values
        else:
            return self.ds[variable][:].values

    def get_mask_vector(self, ii: int):
        return self.ds['stat'][ii,:].values < 0

    def get_vertical_selection(self, ii: int, datum: str, limits: tuple):
        # Get raw data
        pz = self.ds['z'][ii,:].values
        pd = self.ds['depth'][ii,:].values
        wd = self.ds['water_depth'][ii,:].values

        # Get the mask based on inactive particles
        mask = self.get_mask_vector(ii)

        # Get water level (wl) and bed level (bl) for each particle
        wl = np.ma.masked_array(pz + pd, mask=mask, fill_value=-999)
        bl = np.ma.masked_array(wl - wd, mask=mask, fill_value=-999)

        # Convert the limits into elevation
        if datum == 'sigma':
            z1 = limits[0] * (wl - bl) + bl
            z2 = limits[1] * (wl - bl) + bl
        elif datum == 'height':
            z1 = limits[0] + bl
            z2 = limits[1] + bl
        elif datum == 'depth':
            z1 = wl - limits[1]
            z2 = wl - limits[0]
        elif datum == 'elevation':
            z1 = limits[0]
            z2 = limits[1]
        else:
            return None

        # Return logical index of cells in limits
        return (z1.filled() <= pz) & (pz <= z2.filled())

    def __prep_file_handle__(self, lazy_load: bool, warmup: pd.Timedelta):
        # Assert the file exists
        if isinstance(self.file, str):
            self.file = Path(self.file)
            assert Path(
                self.file
            ).exists(), f"No such file or directory: \n{self.file.as_posix()}"
        elif isinstance(self.file, Path):
            assert (
                self.file.exists()
            ), f"No such file or directory: \n{self.file.as_posix()}"

        # ToDO: Refactor this if statement
        single_file = any([isinstance(self.file, x) for x in [str, Path]])
        multi_file = any([isinstance(self.file, x) for x in [list, GeneratorType]])

        # Direct xarray object passthrough
        if isinstance(self.file, xr.Dataset):
            self.ds = self.file
            self.__prep_time_vector__()

        # Normal file open
        elif (lazy_load == False) & single_file:
            self.ds = xr.open_dataset(self.file, decode_times=False)
            self.__prep_time_vector__()
            self.ds = _discard_warmup(self.ds, warmup)

        # Open as an out of memory dataset (single file)
        elif (lazy_load == True) & single_file:
            self.ds = xr.open_mfdataset([self.file], decode_times=False)
            self.__prep_time_vector__()

        # Require individual file loop loading
        elif multi_file:
            self.ds = _open_mf_tfv_dataset(self.file, warmup=warmup)
            self.time_vector = pd.to_datetime(self.ds["Time"].values)
            self.nt = self.time_vector.size

        else:
            msg = [
                "Unclear file(s) type",
                "Please supply either a str/path, a list of files, or an xr.Dataset",
                "",
            ]
            assert False, "\n".join(msg)

    def __prep_time_vector__(self):
        # Define fv epoch relative to python epoch
        fv_epoch = pd.Timestamp(1990, 1, 1)

        # Prepare time vector relative to python epoch
        # This if statement is a future check for when xarray starts decoding FV results
        if isinstance(self.ds["Time"].values[0], np.datetime64):
            self.time_vector = pd.to_datetime(self.ds["Time"].values)
        else:
            self.time_vector = (
                pd.to_timedelta(self.ds["Time"].values, unit="h") + fv_epoch
            )
        self.nt = self.time_vector.size
        self.ds.assign_coords(Time=self.time_vector)  # needed due to existing time variable

    def __prep_2d_geometry__(self):
        self.np = self.ds['groupID'].size

    def __prep_3d_geometry__(self):
        pass

    # Inherit doc strings (needs to be done a better way with decorator as per matplotlib)
    get_raw_data.__doc__ = Particles.get_raw_data.__doc__
    get_mask_vector.__doc__ = Particles.get_mask_vector.__doc__
    get_vertical_selection.__doc__ = Particles.get_vertical_selection.__doc__
