import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 2.5
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
mpl.rcParams['axes.labelsize'] = 18


from bagpipes_dev.plotting.plot_sfh import add_sfh
from bagpipes_dev.models.star_formation_history import star_formation_history
from utils import convert_spectrum_units

def plot_spectrum(wavelength, flux):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.text(0.05, 0.9, f"Wavelength range: {wavelength.min():.0f} - {wavelength.max():.0f} Å",
            transform=ax.transAxes)
    
    ax.plot(wavelength, flux)
    ax.set(ylim=(0, flux.max()*1.1))
    ax.set_xlabel("Observed Wavelength (Å)")
    ax.set_ylabel("AB Magnitude")
    ax.set_title("Model Galaxy Spectrum")
    return fig

def plot_spectrum_mag(wavelength, flux, redshift=None):
    fig, ax = plt.subplots(figsize=(6, 4))
    if redshift:
        ax.text(0.05, 0.9, f"Wavelength range: {wavelength.min()/(1+redshift):.0f} - {wavelength.max()/(1+redshift):.0f} Å (rest-frame)",
                transform=ax.transAxes)
        wav_lyA = 1215.67 * (1 + redshift)
    
    wav, mag = convert_spectrum_units(np.c_[wavelength, flux], spec_units='ergscma', out_units='mag').T
    ax.plot(wav, mag, color='sandybrown')
    ylim_upper = mag.min() - .12
    ylim_lower = min(mag[wav>wav_lyA].max() + .5, 31)
    ax.set(ylim=(ylim_lower, ylim_upper), xlim=(wav.min(), wav.max()))
    ax.set_ylabel("AB Magnitude")

    xticks = ax.get_xticks().tolist()
    ax.set_xticklabels([f"{x/10000:.1f}" for x in xticks])
    ax.set_xlabel("Observed Wavelength (microns)")
    if redshift:
        # upper tick to show rest-frame wavelength
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xticklabels([f"{x/(1+redshift)/10000:.2f}" for x in xticks],
                                fontsize=10)
        ax2.set_xlabel("Rest-frame Wavelength")
                           
    return fig

def plot_sfh(sfh, redshift):
    fig, ax = plt.subplots(figsize=(6, 4))
    sfh_type = sfh['type']
    ax.text(0.95, 0.9, f"{sfh_type.capitalize()} SFH",
            transform=ax.transAxes, ha='right')
    model_comp = {
        sfh_type: sfh,
        "redshift": redshift,
    }
    _sfh = star_formation_history(model_comp)
    ax.text(0.95, 0.8, f"log(Mstar)={_sfh.stellar_mass:.2f}",
            transform=ax.transAxes, ha='right')
    add_sfh(_sfh, ax)
    return fig