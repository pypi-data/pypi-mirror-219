from pathlib import Path
import matplotlib.pyplot as plt
import xarray as xr

from gfatpy.lidar.utils import signal_to_rcs


def plot_eta_start_calib(
    d: xr.Dataset,
    wavelength: int = 532,
    output_dir: Path | str | None = None,
    telescope: str = "x",
) -> Path | None:
    """_summary_

    Args:
        d (xr.Dataset): Eta star dataset
    """
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    elif output_dir is None:
        output_dir = Path.cwd()

    if not output_dir.exists() or not output_dir.is_dir():
        raise NotADirectoryError(f"{output_dir} not found.")

    try:
        channel_str = f"{wavelength}{telescope}"

        # FIXME: This search channels should be provisional and shoud be make by
        # passing a channels array with the eta star dataset
        variables: list[str] = list(d.variables.keys())  # type: ignore
        search_channels = filter(lambda v: v.startswith("eta_star_profile_"), variables)
        channel_names = list(map(lambda v: v[17:-1], search_channels))

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(15, 10), sharey=True)
        y_lim = (0, 12_000)
        # Title
        fig_title_1 = r"Calibration depolarization analysis"
        # % (time_start_dt.strftime("%Y%m%d"), time_start_dt.strftime("%H%M"),
        #     time_end_dt.strftime("%H%M"))
        # fig_title_2 = r"Channel %s. $\alpha_{misalign.}$ ($\circ$)= %4.2f $\pm$ %4.2f" \
        #                 % (wv_str, dw["alpha_%s" % ch_an], dw["alpha_error_%s" % ch_an])
        # fig_title_3 = r"Analog: Calib. factor [%3.1f - %3.1f km] = %6.4f $\pm$ %6.4f ; " \
        #                 r"$\epsilon_{misalig.}$ ($^\circ$) = %4.2f $\pm$ %4.2f" \
        #                 % (dw["cal_height_an"][0]*1e-3, dw["cal_height_an"][1]*1e-3,
        #                     dw["gain_ratio_Delta90_avg_%s" % ch_an], dw["gain_ratio_Delta90_std_%s" % ch_an],
        #                     dw["epsilon_%s" % ch_an], dw["epsilon_error_%s" % ch_an])
        # fig_title_4 = r"Photoncounting: Calib. factor [%3.1f - %3.1f km] = %6.4f $\pm$ %6.4f ; " \
        #                 r"$\epsilon_{misalig.}$ ($^\circ$) = %4.2f $\pm$ %4.2f" \
        #                 % (dw["cal_height_pc"][0]*1e-3, dw["cal_height_pc"][1]*1e-3,
        #                     dw["gain_ratio_Delta90_avg_%s" % ch_pc], dw["gain_ratio_Delta90_std_%s" % ch_pc],
        #                     dw["epsilon_%s" % ch_pc], dw["epsilon_error_%s" % ch_pc])

        plt.suptitle(f"{fig_title_1} \n")

        # ANALOG
        signal_to_rcs(d[f"signal_T_P45_{channel_str}a"], d.range).plot(
            ax=ax1, y="range", lw=2, c="lime", label=r"RCS$^T_{+45}$. AN"
        )  # type: ignore
        signal_to_rcs(d[f"signal_R_N45_{channel_str}a"], d.range).plot(
            ax=ax1, y="range", lw=2, c="darkgreen", label=r"RCS$^R_{-45}$. AN"
        )  # type: ignore
        signal_to_rcs(d[f"signal_T_N45_{channel_str}a"], d.range).plot(
            ax=ax1, y="range", lw=2, c="r", label=r"RCS$^T_{-45}$. AN"
        )  # type: ignore
        signal_to_rcs(d[f"signal_R_P45_{channel_str}a"], d.range).plot(
            ax=ax1, y="range", lw=2, c="darkred", label=r"RCS$^R_{+45}$. AN"
        )  # type: ignore

        # PHOTONCOUNTING
        signal_to_rcs(d[f"signal_T_P45_{channel_str}p"], d.range).plot(ax=ax1, y="range", lw=2, c="deepskyblue", label=r"RCS$^T_{+45}$. PC")  # type: ignore
        signal_to_rcs(d[f"signal_R_N45_{channel_str}p"], d.range).plot(
            ax=ax1, y="range", lw=2, c="b", label=r"RCS$^R_{-45}$. PC"
        )  # type: ignore
        signal_to_rcs(d[f"signal_T_N45_{channel_str}p"], d.range).plot(
            ax=ax1, y="range", lw=2, c="magenta", label=r"RCS$^T_{-45}$. PC"
        )  # type: ignore
        signal_to_rcs(d[f"signal_R_P45_{channel_str}p"], d.range).plot(
            ax=ax1, y="range", lw=2, c="darkmagenta", label=r"RCS$^R_{+45}$. PC"
        )  # type: ignore

        ax1.grid()
        ax1.axes.set_xlabel(r"RCS [a.u.]")
        ax1.axes.set_ylabel(r"Height [km, agl]")
        ax1.axes.set_ylim(y_lim)  # type: ignore
        ax1.axes.set_xscale("log")
        ax1.legend(fontsize="small", loc=2)

        (d[f"signal_R_P45_{channel_str}a"] / d[f"signal_T_P45_{channel_str}a"]).plot(
            ax=ax2, y="range", lw=2, c="blue", label=r"AN at +45"
        )  # type: ignore
        (d[f"signal_R_N45_{channel_str}a"] / d[f"signal_T_N45_{channel_str}a"]).plot(
            ax=ax2, y="range", lw=2, c="red", label=r"AN at -45"
        )  # type: ignore
        (d[f"signal_R_P45_{channel_str}p"] / d[f"signal_T_P45_{channel_str}p"]).plot(
            ax=ax2, y="range", lw=2, c="green", label=r"PC at +45"
        )  # type: ignore
        (d[f"signal_R_N45_{channel_str}p"] / d[f"signal_T_N45_{channel_str}p"]).plot(
            ax=ax2, y="range", lw=2, c="black", label=r"PC at -45"
        )  # type: ignore

        ax2.grid()
        ax2.axes.set_xlabel(r"Signal Ratio [R / T]")
        ax2.axes.set_ylabel(r"")
        ax2.legend(fontsize="small", loc=7)
        ax2.axes.set_xlim((0, 1))

        d[f"eta_star_profile_{channel_str}a"].plot(
            ax=ax3, y="range", c="g", label=r"AN"
        )  # type: ignore
        d[f"eta_star_profile_{channel_str}p"].plot(
            ax=ax3, y="range", c="m", label=r"PC"
        )  # type: ignore
        ax3.grid()
        ax3.axes.set_xlabel(r"Calibration Factor")
        ax3.axes.set_ylabel(r"")
        ax3.axes.set_xlim((0, 10))
        ax3.legend(fontsize="small", loc=7)
        # ax3.axes.set_xlim((0, 1))
    except ValueError:
        output_file = None
        raise ValueError

    if output_dir.exists() and output_dir.is_dir():
        calibration_datetime = d.attrs["calibration_datetime"]
        output_file = (
            output_dir / f"calibration_{channel_str}_{calibration_datetime}.png"
        )
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
    else:
        output_file = None
        raise FileNotFoundError("`output_dir` not found.")
    return output_file
