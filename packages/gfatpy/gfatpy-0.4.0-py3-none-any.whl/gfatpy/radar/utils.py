import os
from pathlib import Path
from typing import overload
import math
import numpy as np
from datetime import datetime

from scipy.signal import savgol_filter
from scipy.integrate import cumulative_trapezoid
import xarray as xr

from .types import ParamsDict, RadarInfoType
from gfatpy.atmo import atmo, ecmwf
from gfatpy.utils.io import read_yaml

""" MODULE For General Lidar Utilities
"""

# RADAR SYSTEM INFO
INFO_FILE = Path(__file__).parent.absolute() / "info.yml"
RADAR_INFO: RadarInfoType = read_yaml(INFO_FILE)

INFO_PLOT_FILE = Path(__file__).parent.absolute() / "plot" / "info.yml"
RADAR_PLOT_INFO = read_yaml(INFO_PLOT_FILE)

class BinnedPSD():
    """Binned gamma particle size distribution (PSD).

    Callable class to provide a binned PSD with the given bin edges and PSD
    values.

    Args (constructor):
        The first argument to the constructor should specify n+1 bin edges,
        and the second should specify n bin_psd values.

    Args (call):
        D: the particle diameter.

    Returns (call):
        The PSD value for the given diameter.
        Returns 0 for all diameters outside the bins.
    """

    def __init__(self, bin_edges, bin_psd):
        if len(bin_edges) != len(bin_psd)+1:
            raise ValueError("There must be n+1 bin edges for n bins.")

        self.bin_edges = bin_edges
        self.bin_psd = bin_psd

    def psd_for_D(self, D):
        if not (self.bin_edges[0] < D <= self.bin_edges[-1]):
            return 0.0

        # binary search for the right bin
        start = 0
        end = len(self.bin_edges)
        while end-start > 1:
            half = (start+end)//2
            if self.bin_edges[start] < D <= self.bin_edges[half]:
                end = half
            else:
                start = half

        return self.bin_psd[start]

    def __call__(self, D):
        if np.shape(D) == (): # D is a scalar
            return self.psd_for_D(D)
        else:
            return np.array([self.psd_for_D(d) for d in D])

    def __eq__(self, other):
        if other is None:
            return False
        return len(self.bin_edges) == len(other.bin_edges) and (self.bin_edges == other.bin_edges).all() and (self.bin_psd == other.bin_psd).all() 


def getEdges():

    pars_class = np.zeros(shape=(32,2))
    bin_edges = np.zeros(shape=(33,1))

    #pars_class[:,0] : Center of Class [mm]
    #pars_class[:,1] : Width of Class [mm]
    pars_class[0:10,1] = 0.125
    pars_class[10:15,1] = 0.250
    pars_class[15:20,1] = 0.500
    pars_class[20:25,1] = 1.
    pars_class[25:30,1] = 2.
    pars_class[30:32,1] = 3.

    j = 0
    pars_class[0,0] = 0.062
    for i in range(1,32):
        if i < 10 or (i > 10 and i < 15) or (i > 15 and i < 20) or (i > 20 and i < 25) or (i > 25 and i < 30) or (i > 30):
            pars_class[i,0] = pars_class[i-1,0] + pars_class[i,1]

        const = [0.188, 0.375, 0.75, 1.5, 2.5]
        if i == 10 or i == 15 or i == 20 or i == 25 or i == 30:
            pars_class[i,0] = pars_class[i-1,0] + const[j]
            j = j + 1

    #print pars_class[i,0]
        bin_edges[i+1,0] = pars_class[i,0] + pars_class[i,1]/2


    bin_edges[0,0] = 0.
    bin_edges[1,0] = pars_class[0,0] + pars_class[0,1]/2 
    
    return bin_edges 

def histogram_intersection(h1, h2, bins):
   bins = np.diff(bins)
   sm = 0
   for i in range(len(bins)):
       sm += min(bins[i]*h1[i], bins[i]*h2[i])
   return sm


def pars2reflec(filepath_rainscat: Path | str, parsFilePath: Path | str, freq: float, surf_temp: float, startDate: datetime.date, stopDate: datetime.date) -> xr.Dataset: 
    # # Parsivel Ze
    freqstr = '%3.1f' % freq

    #Load scattering database
    if (surf_temp < 5):
        scattabstr = Path(r'./scattering_databases') / f"0.C_{freqstr}GHz.csv"
    elif  (5 <= surf_temp < 15):
        scattabstr = Path(r'./scattering_databases') / f"10.C_{freqstr}GHz.csv"
    else: 
        scattabstr = Path(r'./scattering_databases') / f"20.C_{freqstr}GHz.csv"        
    df = pd.read_csv(filename) 

    diameter = 'diameter[mm]'
    radarxs = 'radarsx[mm2]'
    wavelength = 'wavelength[mm]'
    temp = 'T[k]'
    extxs = 'extxs[mm2]'

    delta = 0.01
    upscale_end = (len(df)+1.)/100.
    diameter_ups = np.arange(delta,upscale_end,delta)

    #constants
    T = df.loc[1,temp]
    wavelen = df.loc[1,wavelength]
    K2 = 0.93

    #integration constant
    int_const = wavelen**4 / ((math.pi)**5 *K2)

    #reding meang volume diameter from parsivel
    print('parsFilePath')
    print(parsFilePath)
    pasrDS = xr.open_dataset(parsFilePath)    
       
    #select time range    
    before=( pd.to_datetime(startDate,format='%Y-%m-%d %H:%M') < pd.to_datetime(pasrDS["time"].data))
    after = ( pd.to_datetime(stopDate,format='%Y-%m-%d %H:%M') > pd.to_datetime(pasrDS["time"].data))
    mask_time = before & after
                          
    if not any(mask_time):
        print('No rain in this user-provided period.')
        return
    else:
        parstime = pasrDS["time"].data[mask_time]
        N = pasrDS['N'][:,mask_time]
        N = 10**N.T
        #print(N)
        
    #calculating Ze using parsivel SD    
    Zpars = np.zeros(N.shape[0])    
    if freq > 20:        
        #Ze parsivel using T-matrix at "freq" GHz
        for i in range(N.shape[0]):
            PSD = BinnedPSD(getEdges(),N[i])                                        
            y = PSD(diameter_ups)*df.loc[:,radarxs]
            Zpars[i] = int_const * y.sum()*delta
    else:
        #Ze parsivel in Rayleigh regime
        for i in range(N.shape[0]):
            PSD = BinnedPSD(getEdges(),N[i])
            d6 = PSD(diameter_ups)*df.loc[:,diameter]**6
            Zpars[i] = d6.sum()*delta 
      
    parsZe = 10 * np.log10(Zpars)
    pars = xr.Dataset({'parsZe': (['time'],  parsZe)}, coords={'time': parstime})
    return pars
