import pathlib
from datetime import datetime
from typing import List, Optional, Tuple
from pathlib import Path

import typer

from gfatpy.lidar.types import LidarName, MeasurementType, Telescope
from gfatpy.lidar.nc_convert.converter import convert_nc_by_date
from gfatpy.lidar.reader import reader_xarray
from gfatpy.lidar.quality_assurance.rayleigh_fit import rayleigh_fit_from_file


app = typer.Typer(no_args_is_help=True)


@app.command(
    help="Converts raw lidar data to l1 data",
    no_args_is_help=True,
)
@app.command(no_args_is_help=True)
def nc_convert(
    lidar_name: LidarName = typer.Option(..., "--lidar", "-l"),
    initial_date: datetime = typer.Option(..., "--initial-date", "-i"),
    data_dir: Path = typer.Option(
        ..., "--data-dir", "-d", readable=True, dir_okay=True, file_okay=False
    ),
    measurement_type: Optional[MeasurementType] = typer.Option(
        None, "--measurement-type", "-t"
    ),
    telescope: Optional[Telescope] = typer.Option(Telescope.xf, "--telescope")
    # final_date: Optional[datetime] = typer.Option(None, "--final-date", "-f"), TODO: If necessary implement this
):
    if telescope is None:
        telescope = Telescope.xf

    convert_nc_by_date(
        lidar_name=lidar_name,
        date=initial_date,
        data_dir=data_dir,
        measurement_type=measurement_type,
        telescope=telescope,
    )


@app.command(no_args_is_help=True)
def plot(
    lidar_name: LidarName = typer.Option(..., "--lidar", "-l"),
    initial_date: datetime = typer.Option(..., "--initial-date", "-i"),
    final_date: Optional[datetime] = typer.Option(None, "--final-date", "-f"),
):
    typer.echo(f"{lidar_name}")
    typer.echo(f"{initial_date}")
    typer.echo(f"{final_date}")


@app.command(no_args_is_help=True)
def reader(
    filelist: pathlib.Path = typer.Option(..., "--file-list", "-f"),
    initial_date: datetime = typer.Option(..., "--initial-date", "-i"),
    final_date: Optional[datetime] = typer.Option(None, "--final-date", "-f"),
    initial_range: Optional[float] = typer.Option(0.0, "--initial-range", "-g"),
    final_range: Optional[float] = typer.Option(30000.0, "--final-range", "-t"),
    percentage_required: Optional[float] = typer.Option(
        80.0, "--percentage-required", "-p"
    ),
    _channels: Optional[str] = typer.Option([], "--channels", "-c"),
):
    if _channels is None:
        channels = []
    elif isinstance(_channels, str):
        channels = _channels.split(",")

    elif isinstance(_channels, list):
        channels = _channels
    else:
        raise ValueError("channels must be a list or a string")

    typer.echo(f"{filelist}")
    typer.echo(f"{initial_date}")
    typer.echo(f"{final_date}")
    typer.echo(f"{initial_range}")
    typer.echo(f"{final_range}")
    typer.echo(f"{percentage_required}")
    typer.echo(f"{channels}")

    reader_xarray(
        filelist,
        date_ini=initial_date,
        date_end=final_date,
        ini_range=initial_range,
        end_range=final_range,
        percentage_required=percentage_required,
        channels=channels,
    )


@app.command(help="QA Rayleigh fit", no_args_is_help=True)
def rayleigh_fit(
    file: Path = typer.Option(
        ..., "--file", "-f", readable=True, dir_okay=False, file_okay=True
    ),
    initial_hour: int = typer.Option(None, "--initial-hour", "-i"),
    duration: int = typer.Option(None, "--duration", "-d"),
    channels: Optional[List[str]] = typer.Option(None, "--channels", "-c"),
    reference_range: Optional[Tuple[float, float] | None] = typer.Option(
        None, "--reference-range", "-r"
    ),
    smooth_window: Optional[float | None] = typer.Option(None, "--smooth-window", "-s"),
    save_fig: bool = typer.Option(False, "--save-fig", "-g"),
    output_dir: Path = typer.Option(
        ...,
        "--output-dir",
        "-o",
        readable=True,
        writable=True,
        dir_okay=True,
        file_okay=False,
    ),
):
    if channels is not None:
        assert len(channels) > 0, "At least one channel is required"

    if reference_range is None:
        reference_range = (7000, 8000)

    if smooth_window is None:
        smooth_window = 250

    rayleigh_fit_from_file(
        file=file,
        initial_hour=initial_hour,
        duration=duration,
        channels=channels,
        reference_range=reference_range,
        smooth_window=smooth_window,
        output_dir=output_dir,
        save_fig=save_fig,
    )
