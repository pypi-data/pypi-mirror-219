#!/usr/bin/env python
import os
import glob
import pathlib
import warnings

import datetime as dt
import numpy as np
import xarray as xr
from loguru import logger

from gfatpy import utils
from gfatpy.radar.utils import RADAR_INFO


warnings.filterwarnings("ignore")


__author__ = "Bravo-Aranda, Juan Antonio"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Bravo-Aranda, Juan Antonio"
__email__ = "jabravo@ugr.es"
__status__ = "Production"

""" DEFAULT AUXILIAR INFO
"""

def reader_xarray(
    filelist: list[str] | str,
    properties: list[str] = [],
) -> xr.Dataset:

    def select_properties(dataset: xr.Dataset, properties: list | str) -> xr.Dataset:
        """select_properties function creates a new dataset with 'properties' (list).

        Args:
            dataset (xr.Dataset): radar dataset
            properties (list | str): list of radar property names

        Returns:
            xr.Dataset: radar dataset
        """

        if len(properties) > 0:
            if isinstance(properties, str):
                properties = [properties]
            if isinstance(properties, np.ndarray):
                properties = properties.tolist()

            # find properties
            for _property in [*dataset.variables.keys()]:
                if _property not in properties:                                            
                    dataset = dataset.drop_vars(_property)                
        return dataset

    #load the files
    radar = None
    for fn in filelist:
        with xr.open_dataset(
            fn, chunks={}
        ) as _dx:
            _dx = select_properties(_dx, properties)
        if not radar:
            radar = _dx
        else:
            # concat only variables that have "time" dimension.
            # rest of variables keep values from first dataset
            try:
                radar = xr.concat(
                    [radar, _dx],
                    dim="time",
                    data_vars="minimal",
                    coords="minimal",
                    compat="override",
                )
            except Exception as e:
                logger.critical(f"Dataset in {fn} not concatenated")
                raise e
    return radar