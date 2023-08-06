import os
from pathlib import Path
from typing import overload, Any
import numpy as np
from datetime import datetime

from scipy.signal import savgol_filter
from scipy.integrate import cumulative_trapezoid, cumtrapz
import xarray as xr

from .types import ParamsDict, LidarInfoType
from gfatpy.atmo import atmo, ecmwf
from gfatpy.utils.io import read_yaml

""" MODULE For General Lidar Utilities
"""

# LIDAR SYSTEM INFO
INFO_FILE = Path(__file__).parent.absolute() / "info.yml"
LIDAR_INFO: LidarInfoType = read_yaml(INFO_FILE)

INFO_PLOT_FILE = Path(__file__).parent.absolute() / "plot" / "info.yml"
LIDAR_PLOT_INFO = read_yaml(INFO_PLOT_FILE)


@overload
def signal_to_rcs(signal: xr.DataArray, ranges: xr.DataArray) -> xr.DataArray:
    ...


@overload
def signal_to_rcs(
    signal: np.ndarray[Any, np.dtype[np.float64]],
    ranges: np.ndarray[Any, np.dtype[np.float64]],
) -> np.ndarray[Any, np.dtype[np.float64]]:
    ...


def signal_to_rcs(signal, ranges):
    """Convert Lidar Signal to range-corrected signal

    Args:
        signal (np.ndarray[Any, np.dtype[np.float64]] | xr.DataArray): Lidar signal
        ranges (np.ndarray[Any, np.dtype[np.float64]] | xr.DataArray): Lidar ranges of signal

    Returns:
         xr.DataArray | np.ndarray[Any, np.dtype[np.float64]]: Range-corrected signal

    """
    return signal * ranges**2


@overload
def rcs_to_signal(rcs: xr.DataArray, ranges: xr.DataArray) -> xr.DataArray:
    ...


@overload
def rcs_to_signal(rcs: np.ndarray, ranges: np.ndarray) -> np.ndarray:
    ...


def rcs_to_signal(rcs, ranges):
    return rcs / ranges**2


def smooth_signal(signal, method="savgol", savgol_kwargs: dict | None = None):
    """Smooth Lidar Signal

    Args:
        signal ([type]): [description]
        method (str, optional): [description]. Defaults to 'savgol'.
    """

    if method == "savgol":
        if savgol_kwargs is None:
            savgol_kwargs = {"window_length": 21, "polyorder": 2}
        smoothed_signal = savgol_filter(signal, **savgol_kwargs)
    else:
        raise NotImplementedError(f"{method} has not been implemented yet")

    return smoothed_signal


def estimate_snr(signal, window=5):
    """[summary]

    Args:
        signal ([type]): [description]
    """

    # ventana: numero impar
    if window % 2 == 0:
        window += 1
    subw = window // 2

    n = len(signal)
    avg = np.zeros(n) * np.nan
    std = np.zeros(n) * np.nan

    for i in range(n):
        ind_delta_min = i - subw if i - subw >= 0 else 0
        ind_delta_max = i + subw if i + subw < n else n - 1

        si = signal[ind_delta_min : (ind_delta_max + 1)]
        avg[i] = np.nanmean(si)
        std[i] = np.nanstd(si)

        # print("%i, %i, %i" % (i, ind_delta_min, ind_delta_max + 1))
        # print(signal[ind_delta_min:(ind_delta_max+1)])
    snr = avg / std

    return snr, avg, std


def get_lidar_name_from_filename(fn):
    """Get Lidar System Name from L1a File Name
    Args:
        fn (function): [description]
    """
    lidar_nick = os.path.basename(fn).split("_")[0]
    if lidar_nick in LIDAR_INFO["metadata"]["nick2name"].keys():
        lidar = lidar_nick
    else:
        lidar = None
    return lidar


def sigmoid(x, x0, k, coeff: float = 1, offset: float = 0):
    y = 1 / (1 + np.exp(-k * (x - x0)))
    return (coeff * y) + offset


def extrapolate_beta_with_angstrom(
    beta_ref: np.ndarray,
    wavelength_ref: float,
    wavelength_target: float,
    angstrom_exponent: float | np.ndarray,
) -> np.ndarray:
    return beta_ref * (wavelength_target / wavelength_ref) ** -angstrom_exponent


def generate_particle_backscatter(
    ranges: np.ndarray,
    wavelength: float,
    fine_ae: float,
    coarse_ae: float,
    fine_beta532: float = 2.5e-6,
    coarse_beta532: float = 2.0e-6,
) -> np.ndarray:
    """_summary_

    Args:
        ranges (np.ndarray): ranges
        wavelength (float): wavelength
        fine_ae (float): fine-mode Angstrom exponent
        coarse_ae (float): coarse-mode Angstrom exponent
        fine_beta532 (float, optional): fine-mode backscatter coefficient at 532 nm. Defaults to 2.5e-6.
        coarse_beta532 (float, optional): coarse-mode backscatter coefficient at 532 nm. Defaults to 2.0e-6.

    Returns:
        np.ndarray: particle backscatter coefficient profile
    """

    beta_part_fine = sigmoid(
        ranges, 2500, 1 / 60, coeff=-fine_beta532, offset=fine_beta532
    )
    beta_part_coarse = sigmoid(
        ranges, 5000, 1 / 60, coeff=-coarse_beta532, offset=coarse_beta532
    )

    beta_part_fine = extrapolate_beta_with_angstrom(
        beta_part_fine, 532, wavelength, 1.5
    )

    return beta_part_fine + beta_part_coarse


def generate_synthetic_signal(
    ranges: np.ndarray,
    wavelength: float = 532,
    wavelength_raman: float | None = None,
    overlap_midpoint: float = 600,
    k_lidar: float = 4e9,
    paralell_perpendicular_ratio: float = 0.33,
    particle_lr: float = 45,
    force_zero_aer_after_bin: int | None = None,
) -> tuple[np.ndarray, np.ndarray | None, ParamsDict]:
    """It generates synthetic lidar signal.

    Args:
        ranges (np.ndarray): Range
        wavelength (float, optional): Wavelength. Defaults to 532.
        overlap_midpoint (float, optional): _description_. Defaults to 600.
        k_lidar (float, optional): Lidar constant calibration. Defaults to 4e9.
        wavelength_raman (float | None, optional): Raman wavelength. Defaults to None. If None, signal is elastic.
        paralell_perpendicular_ratio (float, optional): _description_. Defaults to 0.33.
        particle_lratio (float, optional): _description_. Defaults to 45.
        force_zero_aer_after_bin (int | None, optional): _description_. Defaults to None.

    Returns:
        tuple[np.ndarray, ParamsDict]: _description_
    """

    z = ranges

    # Overlap
    overlap = sigmoid(
        z,
        overlap_midpoint,
        1 / 50,
        offset=0,
    )

    overlap[overlap < 9e-3] = 0
    overlap[overlap > 0.999] = 1

    # Molecular elastic
    ecmwf_data = ecmwf.get_ecmwf_temperature_preasure(datetime(2022, 9, 3), heights=z)
    atmo_data = atmo.molecular_properties(
        wavelength,
        np.array(ecmwf_data.pressure.values),
        np.array(ecmwf_data.temperature.values),
        heights=z,
    )

    beta_mol = atmo_data["molecular_beta"].values
    alpha_mol = atmo_data["molecular_alpha"].values

    # Particle elastic
    # 0.33 para polvo desértico
    # 0.0034 para parte molecular
    # Calcular beta_part parallel = total*(1-0.33)
    # Calcular beta_part perpendicular = total*(0.33)
    # Análogo con otro coeficiente para la parte molecular

    fine_ae = 1.5
    coarse_ae = 0

    beta_part = generate_particle_backscatter(
        ranges, wavelength, fine_ae=fine_ae, coarse_ae=coarse_ae
    )
    alpha_part = particle_lr * beta_part

    part_accum_ext = cumulative_trapezoid(alpha_part, z, initial=0)
    mol_accum_ext = cumulative_trapezoid(alpha_mol, z, initial=0)
    # accumulated_extinction = cumulative_trapezoid(alpha_part + alpha_mol, z, initial=0) # TODO: separate part and mol
    T_elastic = np.exp(-part_accum_ext - mol_accum_ext)  # type: ignore

    P_elastic = k_lidar * (overlap / z**2) * (beta_part + beta_mol) * T_elastic**2

    params: ParamsDict = {
        "particle_alpha": alpha_part,
        "particle_beta": beta_part,
        "molecular_alpha": alpha_mol,
        "molecular_beta": beta_mol,
        "molecular_beta_att": atmo_data["attenuated_molecular_beta"].values,
        "particle_accum_ext": part_accum_ext,
        "molecular_accum_ext": mol_accum_ext,
        "transmittance": T_elastic,
        "overlap": overlap,
        "k_lidar": k_lidar,
        "angstrom_exponent_coarse": coarse_ae,
        "angstrom_exponent_fine": fine_ae,
    }

    if wavelength_raman is not None:
        atmo_data = atmo.molecular_properties(
            wavelength_raman,
            np.array(ecmwf_data.pressure.values),
            np.array(ecmwf_data.temperature.values),
            heights=z,
        )
        beta_mol_raman = atmo_data["molecular_beta"]
        alpha_mol_raman = atmo_data["molecular_alpha"]

        beta_part_raman = generate_particle_backscatter(
            ranges, wavelength_raman, fine_ae=fine_ae, coarse_ae=coarse_ae
        )
        alpha_part_raman = particle_lr * beta_part_raman

        part_accum_ext_raman = cumulative_trapezoid(alpha_part_raman, z, initial=0)
        mol_accum_ext_raman = cumulative_trapezoid(alpha_mol_raman, z, initial=0)
        # accumulated_extinction = cumulative_trapezoid(alpha_part + alpha_mol, z, initial=0) # TODO: separate part and mol
        T_raman = np.exp(-part_accum_ext_raman - mol_accum_ext_raman)  # type: ignore

        P_raman = k_lidar * (overlap / z**2) * (beta_mol_raman) * T_elastic * T_raman

        params["particle_beta_raman"] = beta_part_raman
        params["particle_alpha_raman"] = alpha_part_raman
        params["molecular_alpha_raman"] = alpha_mol_raman.values
        params["molecular_beta_raman"] = beta_mol_raman.values
        params["particle_accum_ext_raman"] = part_accum_ext_raman
        params["molecular_accum_ext_raman"] = mol_accum_ext_raman
    else:
        P_raman = None

    if force_zero_aer_after_bin is not None:
        alpha_part[force_zero_aer_after_bin:] = 0
        beta_part[force_zero_aer_after_bin:] = 0

    return P_elastic, P_raman, params


def integrate_from_reference(integrand, x, reference_index):
    """

    at x[ref_index], the integral equals = 0
    """
    # integrate above reference
    int_above_ref = cumtrapz(integrand[reference_index:], x=x[reference_index:])

    # integrate below reference
    int_below_ref = cumtrapz(
        integrand[: reference_index + 1][::-1], x=x[: reference_index + 1][::-1]
    )[::-1]

    return np.concatenate([int_below_ref, np.zeros(1), int_above_ref])


def optical_depth(extinction, height, ref_index=0):
    """
    Integrate extinction profile along height: r'$\tau(z) = \int_0^z d\dseta \alpha(\dseta)$'
    """

    return integrate_from_reference(extinction, height, reference_index=ref_index)


import numpy as np


def refill_overlap(
    atmospheric_profile: np.ndarray[Any, np.dtype[np.float64]],
    height: np.ndarray[Any, np.dtype[np.float64]],
    fulloverlap_height: float = 600,
    fill_with: float | None = None,
) -> np.ndarray[Any, np.dtype[np.float64]]:
    """Fill overlap region [0-`fulloverlap_height`] of the profile `atmospheric_profile` with the value `fill_with` provided by the user. If None, fill with the value at `fulloverlap_height`.

    Args:
        atmospheric_profile (np.ndarray): Atmospheric profile
        height (np.ndarray): Range profile in meters
        fulloverlap_height (float, optional): Fulloverlap height in meters. Defaults to 600 m.
        fill_with (float, optional): Value to fill the overlap region. Defaults to None.

    Returns:
        np.ndarray: Profile `atmospheric_profile` with the overlap region filled.
    """
    if fulloverlap_height < height[0] or fulloverlap_height > height[-1]:
        raise ValueError(
            "The fulloverlap_height is outside the range of height values."
        )

    idx_overlap = np.abs(height - fulloverlap_height).argmin()

    if fill_with is None:
        fill_with = atmospheric_profile[idx_overlap]

    new_profile = np.copy(atmospheric_profile)
    new_profile[:idx_overlap] = fill_with

    return new_profile
