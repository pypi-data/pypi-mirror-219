import os
from pathlib import Path

import datetime

from gfatpy.lidar.utils import LIDAR_INFO
from gfatpy.utils.io import find_nearest_filepath


def GHK_simulator(
    lidar_nick: str,
    calibrator: str,
    target_date: datetime.date,
    output_dir: Path,
    channel: str | None = None,
) -> list[Path]:

    if not output_dir.exists() or not output_dir.is_dir():
        raise NotADirectoryError(f"{output_dir} not found.")

    lidar_name: str = LIDAR_INFO["metadata"]["nick2name"][lidar_nick]

    if channel is None:
        channels = LIDAR_INFO["lidars"][lidar_name]["GHK_channels"]
    else:
        channels = [channel]
    output_paths = []
    for channel_ in channels:
        # Ini file for each channel

        ini_filepath = find_GHK_ini_file(
            lidar_nick, channel_, target_date, calibrator=calibrator
        )

        if not ini_filepath.exists():
            raise FileNotFoundError(f"Ini file not found: {ini_filepath}.")

        output_path_ = run_GHK_simulator(ini_filepath, output_dir)
        if isinstance(output_path_, Path):
            output_paths.append(output_path_)
    return output_paths


def find_GHK_ini_file(
    lidar_nick: str,
    channel: str,
    target_date: datetime.date,
    calibrator: str = "rot",
    ini_dir: Path | None = None,
) -> Path:

    if ini_dir is None:
        dir = Path(__file__).parent.absolute()
        ini_dir = dir / "GHK" / "system_settings"

    if not ini_dir.exists() or not ini_dir.is_dir():
        raise NotADirectoryError(f"{ini_dir} not found.")

    ini_path = find_nearest_filepath(
        ini_dir,
        f"optic_input_{lidar_nick}_{calibrator}_{channel}*.py",
        5,
        datetime.datetime(target_date.year, target_date.month, target_date.day),
    )
    return ini_path


def run_GHK_simulator(ini_path: Path, output_dir: Path) -> Path:
    # run GHK: uses ghk_inp_fn as Input. Generates ghk_param_fn

    # if not ini_path.exists():
    #     raise FileNotFoundError('Ini path not found.')

    depo_path = Path(__file__).parent.absolute()

    GHK_program = depo_path / "GHK" / "GHK_0.9.8h_Py3.7.py"

    output_dir.mkdir(parents=True, exist_ok=True)

    os.system(f"python {GHK_program} {ini_path} {output_dir.absolute()}")

    output_path = [*output_dir.rglob(f"*{ini_path.name.split('.')[0]}*.dat")]

    if isinstance(output_path, list) and len(output_path) == 1:
        output_path = output_path[0]
        return output_path
    else:
        raise FileNotFoundError(f"Output file not found in {output_dir}.")
