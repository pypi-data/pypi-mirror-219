from pdb import set_trace
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Iterator

from linc import write_nc_legacy
from linc.config import get_config, Config
from loguru import logger

from gfatpy.utils.utils import parse_datetime
from ..file_manager import info2general_path, info2path
from ..types import LidarName, MeasurementType, Telescope
from .types import Measurement

CONFIGS_DIR = Path(__file__).parent / "configs"
DAYS_SEARCH_PAST = 5
RAW_FIRST_LETTERS = "RM"

logger.add(sys.stdout, level="INFO")


def convert_nc_by_date(
    date: datetime | str,
    lidar_name: LidarName = LidarName.mlh,
    measurement_type: MeasurementType | None = None,
    config_file: Path | str | None = None,
    data_dir: Path | str | None = None,
    telescope: Telescope = Telescope.xf,
) -> None:
    """Replaces the old lidar raw2l1 function

    Args:
        date (datetime | str): _description_
        lidar (LidarName, optional): _description_. Defaults to LidarName.mlh.
        measurement_type (MeasurementType | None, optional): _description_. Defaults to None.
        data_dir (Path | str | None, optional): _description_. Defaults to cwd.
    """
    if data_dir is None:
        data_dir = Path().cwd()
    elif isinstance(data_dir, str):
        data_dir = Path(data_dir)

    if not data_dir.exists() or not data_dir.is_dir():
        raise ValueError("Not found data_dir")

    if isinstance(config_file, str):
        config_file = Path(config_file)

    date = parse_datetime(date)
    config = search_config(lidar_name, config_file)
    origin_path = info2general_path(
        lidar_name.value, date=date, data_level="0a", data_dir=data_dir
    )

    prev_paths = [
        info2general_path(
            lidar_name.value,
            date=date - timedelta(days=n_day),
            data_level="0a",
            data_dir=data_dir,
        )
        for n_day in range(1, DAYS_SEARCH_PAST + 1)
    ]

    measurements = to_measurements(origin_path.glob("*"))
    measurements = filter_by_type(measurements, measurement_type)

    if len(measurements) != 0:
        logger.info(f"{len(measurements)} measurements found")
    else:
        logger.error(f"0 measurements found")
        raise FileNotFoundError()

    rs_processed = False
    ot_processed = False

    for measurement in measurements:
        if measurement.type not in [MeasurementType.DP, MeasurementType.TC]:
            if measurement.type == MeasurementType.RS:
                if rs_processed:
                    continue
                files = glob_all_from_type_and_close_date(
                    measurements, MeasurementType.RS, prev_paths, date
                )
                rs_processed = True
            elif measurement.type == MeasurementType.OT:
                if ot_processed:
                    continue
                files = glob_all_from_type_and_close_date(
                    measurements, MeasurementType.OT, prev_paths, date
                )
                ot_processed = True
            else:
                files = measurement.path.glob(f"{RAW_FIRST_LETTERS}*")
            result_path = info2path(
                lidar_name=lidar_name.value,
                channel=get_532_from_telescope(telescope),
                measurement_type=measurement.type.value,
                date=measurement.time,
                dir=data_dir,
            )
            result_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Writing {result_path.name}")
            write_nc_legacy(files, result_path, config=config)
        else:
            sub_mesurements = filter(lambda p: p.is_dir(), measurement.path.glob("*"))
            for sm in sub_mesurements:
                files = sm.glob(f"{RAW_FIRST_LETTERS}*")
                result_path = info2path(
                    lidar_name=lidar_name.value,
                    channel=get_532_from_telescope(telescope),
                    measurement_type=measurement.type.value,
                    signal_type=sm.name,
                    date=measurement.time,
                    dir=data_dir,
                )
                result_path.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"Writing {result_path.name}")
                write_nc_legacy(files, result_path, config=config)


def convert_nc_by_folder(
    dir: Path | str,
    date: datetime | str,
    output_dir: Path | str | None = None,
    lidar_name: LidarName = LidarName.mlh,
    measurement_type: MeasurementType | None = None,
    config_file: str | None = None,
    telescope: Telescope = Telescope.xf,
) -> None:

    if isinstance(dir, str):
        dir = Path(dir)

    if not dir.exists() or not dir.is_dir():
        raise ValueError("Not found data_dir")

    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    elif output_dir is None:
        output_dir = Path.cwd()

    if not output_dir.exists() or not output_dir.is_dir():
        raise ValueError("Not found output_dir")

    date = parse_datetime(date)
    set_trace()
    config = search_config(lidar_name, config_file)
    origin_path = dir

    measurements = to_measurements(origin_path.glob("*"))
    measurements = filter_by_type(measurements, measurement_type)

    if len(measurements) != 0:
        logger.info(f"{len(measurements)} measurements found")
    else:
        logger.error(f"0 measurements found")
        raise FileNotFoundError()

    rs_processed = False
    ot_processed = False

    for measurement in measurements:
        if measurement.type not in [MeasurementType.DP, MeasurementType.TC]:
            if measurement.type == MeasurementType.RS:

                if rs_processed:
                    continue
                files = glob_all_from_type_and_close_date(
                    measurements, MeasurementType.RS, [], date
                )
                rs_processed = True
            if measurement.type == MeasurementType.OT:
                if ot_processed:
                    continue
                files = glob_all_from_type_and_close_date(
                    measurements, MeasurementType.OT, [], date
                )
                ot_processed = True
            else:
                files = measurement.path.glob(f"{RAW_FIRST_LETTERS}*")
            result_path = info2path(
                lidar_name=lidar_name.value,
                channel=get_532_from_telescope(telescope),
                measurement_type=measurement.type.value,
                date=measurement.time,
                dir=output_dir,
            )
            result_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Writing {result_path.name}")
            write_nc_legacy(files, result_path, config=config)
        else:
            sub_mesurements = filter(lambda p: p.is_dir(), measurement.path.glob("*"))
            for sm in sub_mesurements:
                files = sm.glob(f"{RAW_FIRST_LETTERS}*")
                result_path = info2path(
                    lidar_name=lidar_name.value,
                    channel=get_532_from_telescope(telescope),
                    measurement_type=measurement.type.value,
                    date=measurement.time,
                    dir=output_dir,
                )
                result_path.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"Writing {result_path.name}")
                write_nc_legacy(files, result_path, config=config)


def search_config(
    lidar_name: LidarName, opt_config: Path | str | None = None
) -> Config:

    try_last_chance = False
    if isinstance(opt_config, Path):
        config_path = opt_config
    elif isinstance(opt_config, str):
        config_path = Path(opt_config)
        if not config_path.exists():
            try_last_chance = True
    elif opt_config is None:
        try_last_chance = True

    if try_last_chance:
        config_path = Path(CONFIGS_DIR / f"{lidar_name}.toml")
    else:
        raise FileNotFoundError(f"No configution file found in {opt_config}")

    if not config_path.exists():
        raise FileNotFoundError(f"No configution file found in {opt_config}")

    return get_config(config_path)


def filter_by_type(
    measurements: list[Measurement], mtype: MeasurementType | None = None
) -> list[Measurement]:
    match mtype:
        case MeasurementType.RS:
            measurements = list(
                filter(
                    lambda m: m.type in [MeasurementType.RS, MeasurementType.DC],
                    measurements,
                )
            )
        case MeasurementType.TC:
            measurements = list(
                filter(
                    lambda m: m.type in [MeasurementType.TC, MeasurementType.DC],
                    measurements,
                )
            )
        case MeasurementType.DP:
            measurements = list(
                filter(
                    lambda m: m.type in [MeasurementType.DP, MeasurementType.DC],
                    measurements,
                )
            )
        case MeasurementType.HF:
            measurements = list(
                filter(
                    lambda m: m.type in [MeasurementType.HF, MeasurementType.DC],
                    measurements,
                )
            )
        case MeasurementType.OT:
            measurements = list(
                filter(lambda m: m.type in [MeasurementType.OT], measurements)
            )
        case MeasurementType.DC:
            measurements = list(
                filter(lambda m: m.type in [MeasurementType.DC], measurements)
            )
        case None:
            return measurements
    return measurements


def glob_all_from_type_and_close_date(
    measurements: list[Measurement],
    mtype: MeasurementType,
    prev_paths: list[Path],
    date: datetime,
) -> list[Path]:
    paths: set[Path] = set({})

    # Group all groups of measurements into one array
    for meas in measurements:
        if meas.type == mtype:
            paths |= set(meas.path.glob(f"{RAW_FIRST_LETTERS}*"))

    # Aditionally, search in neighbor days from measurements of this day
    for prev_path in prev_paths:
        prev_measurements = prev_path.glob(f"{mtype.value}_*")
        for prev_measurement in prev_measurements:
            same_day_measurements = set(
                prev_measurement.glob(f"{RAW_FIRST_LETTERS}{to_licel_date_str(date)}*")
            )
            paths |= same_day_measurements  # Set union assignment

    return list(paths)


def to_measurements(glob: Iterator[Path]) -> list[Measurement]:
    measurements = []
    for path in glob:
        time = datetime.strptime(path.name[3:], r"%Y%m%d_%H%M")
        measurements.append(
            Measurement(type=MeasurementType(path.name[:2]), path=path, time=time)
        )

    return measurements


def get_532_from_telescope(telescope: Telescope = Telescope.xf) -> str:
    if telescope == telescope.xf:
        return "532xpa"
    elif telescope == telescope.ff:
        return "532fpa"
    elif telescope == telescope.nf:
        return "532npa"

    raise ValueError("Telescope type not recognized. Options are xf, ff, nf")


def to_licel_date_str(date: datetime) -> str:
    month_hex = f"{date.month:x}"
    return f'{date.strftime(r"%y")}{month_hex}{date.strftime(r"%d")}'
