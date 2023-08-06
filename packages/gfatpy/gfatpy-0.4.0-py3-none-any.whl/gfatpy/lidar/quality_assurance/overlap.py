import datetime as dt
from pathlib import Path
import numpy as np
import xarray as xr

from gfatpy.utils.utils import numpy_to_datetime
from gfatpy.lidar.preprocessing import preprocess
from gfatpy.lidar.file_manager import channel2info


def retrieve_ff_overlap(
    filepath: Path | str,
    hour_range: tuple[float, float],
    output_dir: Path,
    norm_range: tuple[float, float] = (2500, 3500),
    rel_dif_threshold: float = 2.5,
) -> Path | None:
    """Retrieve ff overlap from a near-to-far module lidar ratio

    Args:
        filepath (Path | str): Lidar file path
        hour_range (tuple[float, float]): Hour range to calculate the overlap
        norm_range (tuple[float, float], optional): Range to normalized signals. Defaults to (2500, 3500).
        rel_dif_threshold (float, optional): Relative difference threshold. Overlap function will be rejected if it causes a relative difference larger than this threshold. Defaults to 2.5 %.
        output_dir (Path, optional): output folder path. Defaults to Path.cwd().

    Raises:
        FileNotFoundError: Lidar file not found
        ValueError: Hour range must be a tuple of two floats
        ValueError: Not enough profiles in file to cover the selected time range [<50%]
        ValueError: Could not calculate overlap for 355 nm
        ValueError: Could not calculate overlap for 532 nm
        ValueError: Could not calculate overlap for 1064 nm
        ValueError: Could not calculate overlap for any channel

    Returns:
        Path | None : Path to the overlap file
    """

    if isinstance(filepath, str):
        filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File {filepath} not found")

    if hour_range[0] > hour_range[1]:
        raise ValueError("hour_range[0] must be lower than hour_range[1]")

    # Check time period is within file time range
    raw = xr.open_dataset(filepath)

    # Get date from filename
    date_ = numpy_to_datetime(raw.time[2].values)
    if date_ is None:
        raise ValueError("Could not get date from filename")
    date = dt.datetime(date_.year, date_.month, date_.day)

    time_range = (
        (date + dt.timedelta(hours=hour_range[0])),
        (date + dt.timedelta(hours=hour_range[-1])),
    )
    time_resol = (raw.time[1] - raw.time[0]).item() / 1e9
    expected_profile_number = (
        time_range[1] - time_range[0]
    ).total_seconds() / time_resol

    if raw.sel(time=slice(*time_range)).time.size < 0.5 * expected_profile_number:
        raise ValueError(
            "Not enough profiles in file to cover the selected time range [<50%]"
        )

    raw.close()

    # Preprocess lidar file
    lidar_ = preprocess(
        filepath
    )  # FIXME: add crop_ranges and gluing_products and apply_dt as arguments

    # Select time range
    lidar = lidar_.sel(time=slice(*time_range))

    # Retrieve overlap at 355, 532, 1064 nm
    channels = []
    try:
        overlap355 = ff_overlap_from_channels(
            lidar,
            "355fpa",
            "355npa",
            norm_range=norm_range,
            rel_dif_threshold=rel_dif_threshold,
        )
        channels.append("355fpa")
    except:
        overlap355 = None
        raise ValueError("Could not calculate overlap for 355 nm")
    try:
        overlap532 = ff_overlap_from_channels(
            lidar,
            "532fta",
            "532npa",
            norm_range=norm_range,
            rel_dif_threshold=rel_dif_threshold,
        )
        channels.append("532fta")
    except:
        overlap532 = None
        raise ValueError("Could not calculate overlap for 532 nm")
    try:
        overlap1064 = ff_overlap_from_channels(
            lidar,
            "1064fta",
            "1064nta",
            norm_range=norm_range,
            rel_dif_threshold=rel_dif_threshold,
        )
        channels.append("1064fta")
    except:
        overlap1064 = None
        raise ValueError("Could not calculate overlap for 1064 nm")

    # Merge overlap data

    overlap_matrix = np.zeros((len(lidar.range), len(channels)))
    if overlap355 is not None and overlap532 is not None and overlap1064 is not None:
        overlap_matrix[:, 0] = overlap355.values
        overlap_matrix[:, 1] = overlap532.values
        overlap_matrix[:, 2] = overlap1064.values
    elif overlap355 is not None and overlap532 is not None:
        overlap_matrix[:, 0] = overlap355.values
        overlap_matrix[:, 1] = overlap532.values
    elif overlap355 is not None and overlap1064 is not None:
        overlap_matrix[:, 0] = overlap355.values
        overlap_matrix[:, 2] = overlap1064.values
    elif overlap532 is not None and overlap1064 is not None:
        overlap_matrix[:, 1] = overlap532.values
        overlap_matrix[:, 2] = overlap1064.values
    elif overlap355 is not None:
        overlap_matrix[:, 0] = overlap355.values
    elif overlap532 is not None:
        overlap_matrix[:, 1] = overlap532.values
    elif overlap1064 is not None:
        overlap_matrix[:, 2] = overlap1064.values
    else:
        overlap_matrix = None
        raise ValueError("Could not calculate overlap for any channel")

    if overlap_matrix is not None:
        # Create DataArray
        overlap = xr.DataArray(
            overlap_matrix,
            dims=("range", "channel"),
            coords={"range": lidar.range.values, "channel": channels},
        )

        # Create output folder
        if not output_dir.exists() and not output_dir.is_dir():
            output_dir.mkdir(parents=True)

        time_min = numpy_to_datetime(lidar.time[0].values)
        if time_min is None:
            raise ValueError("Could not get time from filename")
        time_min = time_min.strftime("%H%M")

        time_max = numpy_to_datetime(lidar.time[-1].values)
        if time_max is None:
            raise ValueError("Could not get time from filename")
        time_max = time_max.strftime("%H%M")

        # Create output filename
        if not output_dir.exists() or not output_dir.is_dir():
            raise FileNotFoundError(f"Output directory {output_dir} does not exist")

        output_path = (
            output_dir
            / f'overlap_alh_ff_{date.strftime("%Y%m%d")}_{time_min}-{time_max}.nc'
        )

        # save overlap files
        overlap.to_netcdf(output_path)
        print(f"Overlap saved in {output_path}")
    else:
        raise ValueError("Could not calculate overlap for any channel")
    return output_path


def ff_overlap_from_channels(
    lidar_dataset: xr.Dataset,
    channel_ff: str,
    channel_nf: str,
    norm_range: tuple[float, float] = (2500, 3500),
    rel_dif_threshold: float = 2.5,
) -> xr.DataArray:

    info_ff = channel2info(channel_ff)
    info_nf = channel2info(channel_nf)

    if info_nf[0] != info_ff[0]:
        raise ValueError(
            f"Channels {channel_ff} and {channel_nf} must have the same wavelength"
        )

    # Select time, range to normalize and range to calculate overlap
    nf = lidar_dataset[f"signal_{channel_nf}"].mean("time") / lidar_dataset[
        f"signal_{channel_nf}"
    ].mean("time").sel(range=slice(*norm_range)).mean("range")
    ff = lidar_dataset[f"signal_{channel_ff}"].mean("time") / lidar_dataset[
        f"signal_{channel_ff}"
    ].mean("time").sel(range=slice(*norm_range)).mean("range")

    # Overlap
    overlap_raw = ff / nf

    # Upper limit
    overlap = overlap_raw.copy()
    median = overlap.rolling(range=11, center=True).median("range")
    max_overlap = overlap.range[1 - median.values < 0][0]
    overlap[overlap.range > max_overlap] = 1.0

    # Lower limit
    rel_dif = 100 * (nf - ff / overlap) / nf
    overlap[(overlap.range < 100)] = np.nan
    overlap[rel_dif > rel_dif_threshold] = np.nan

    # Upper limit
    overlap[overlap.range > max_overlap] = 1.0

    # Assign attributes
    attrs = ["location", "system"]
    for attr_ in attrs:
        overlap.attrs[attr_] = lidar_dataset.attrs[attr_]

    overlap.attrs["history"] = dt.datetime.now().strftime(
        "Created %a %b %d %H:%M:%S %Y"
    )
    overlap.attrs["wavelength"] = info_nf[0]
    overlap.attrs["channel_ff"] = channel_ff
    overlap.attrs["channel_nf"] = channel_nf

    return overlap
