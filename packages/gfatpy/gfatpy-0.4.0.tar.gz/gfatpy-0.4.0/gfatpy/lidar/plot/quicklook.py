from typing import Literal, Tuple

import matplotlib
import numpy as np
import xarray as xr
from loguru import logger
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from gfatpy.utils import plot

BoundsType = tuple[float, float] | Literal["auto", "limits"]


def get_norm(
    rcs: np.ndarray,
    scale_bounds: BoundsType,
    color_resolution: int = 128,
) -> matplotlib.colors.BoundaryNorm:

    match scale_bounds:
        case "auto":
            bounds = np.linspace(0, rcs.max() * 0.6, 128)
        case "limits":
            bounds = np.linspace(rcs.min(), rcs.max(), 128)
        case _:
            bounds = np.linspace(*scale_bounds, 128)

    norm = matplotlib.colors.BoundaryNorm(boundaries=bounds, ncolors=2**8, clip=False)
    logger.debug(f"Color bounds min - max: {bounds.min()} - {bounds.max()}")

    return norm


def apply_labels(ax: matplotlib.axes.Axes, data_array: xr.DataArray) -> None:  # type: ignore
    # TODO: Other titles will later be added with config param
    plot.title1(data_array.name, 2)
    plot.title2(np.atleast_1d(data_array.time.mean().dt.date.values)[0].isoformat(), 2)
    # plot.title3(
    #     "{} ({:.1f}N, {:.1f}E)".format(
    #         data_array.attrs.get("site_location"),
    #         float(data_array.attrs["geospatial_lat_min"]),
    #         float(data_array.attrs["geospatial_lon_min"]),
    #     ),
    #     2,
    # )

    plot.watermark(ax, zoom=0.6, alpha=0.6)


def apply_gap_size(ax: matplotlib.axes.Axes, data_array) -> None:  # type: ignore
    diff = data_array.time[1:].values - data_array.time[0:-1].values
    gap_size = 2 * int(
        np.ceil(
            np.median(np.median(diff).astype("timedelta64[s]").astype("float") / 60)
        )
    )

    plot.gapsizer(
        ax,
        data_array.time.values.astype("M8[ms]").astype("O"),
        data_array.range.values,
        gap_size,
        "#c7c7c7",
    )


# TODO: this should be the default implemetation rather than filelist argument
def quicklook_xarray(
    data_array: xr.DataArray,
    /,
    is_rcs: bool = True,
    scale_bounds: BoundsType = "auto",
    colormap: str | matplotlib.colors.Colormap = "jet",
) -> Tuple[Figure, Axes]:
    """Plot a quicklook of a xarray.DataArray

    Args:
        data_array (xr.DataArray): Lidar signal or rcs from `lidar.preprocess`
        is_rcs (bool, optional): To indicate if the data is RCS or not. Defaults to True.
        scale_bounds (BoundsType, optional): scale bounds for the colorbar. Defaults to "auto".
        colormap (str | matplotlib.colors.Colormap, optional): colormap of the colorbar. Defaults to "jet".

    Returns:
        tuple[Figure, Axes]: Figure and Axes objects
    """

    try:
        if is_rcs:
            rcs = data_array.values
        else:
            rcs = data_array.values * data_array.range.values**2

        fig, ax = plt.subplots(figsize=(15, 5))
        norm = get_norm(rcs, scale_bounds)

        q = ax.pcolormesh(
            data_array.time, data_array.range, rcs.T, cmap=colormap, norm=norm
        )

        ax.set_xlabel(r"Time, $[UTC]$")
        ax.set_ylabel(r"Height, $[m, \, agl]$")
        ax.set_ylim(0)

        apply_labels(ax, data_array=data_array)
        apply_gap_size(ax, data_array=data_array)

        fig.colorbar(q)

        q.cmap.set_over("white")  # type: ignore
    except Exception as e:
        raise e
    return fig, ax
