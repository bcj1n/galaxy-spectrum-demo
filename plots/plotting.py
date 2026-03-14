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

def annotate_lines(ax, redshift, fontsize=6):
    # mark common rest-frame emission lines in observed frame
    for line_wav, line_name in [(1216., r'Ly$\alpha$'),
                                (1549., r'C IV 1549'), (1909., r'C III] 1909'),
                                (3727., r'[O II] 3727'),
                                (3869., r'[Ne III] 3869'),
                                (4102., r'H$\delta$'), (4324., r'H$\gamma$'), (4861., r'H$\beta$'),
                                (4959., r'[O III] 4959'), (5007., r'[O III] 5007'),
                                (5876., r'He I 5876'),
                                (6563., r'H$\alpha$')]:
        ax.axvline(line_wav * (1. + redshift),
                color='gray', ls=':', lw=0.8, alpha=0.5)
        ax.text(line_wav * (1. + redshift), ax.get_ylim()[1],
                line_name, fontsize=fontsize, color='gray',
                rotation=90, va='top', ha='right')
    return None
    

def plot_spectrum(wavelength, flux):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.plot(wavelength, flux)
    ax.set(ylim=(0, flux.max()*1.1))
    ax.set_xlabel("Observed Wavelength (Å)")
    ax.set_ylabel("AB Magnitude")
    ax.set_title("Model Galaxy Spectrum")
    return fig

def plot_spectrum_mag(wavelength, flux, redshift=None):
    fig, ax = plt.subplots(figsize=(6, 4))
    if redshift:
        wav_lyA = 1215.67 * (1 + redshift)
    
    wav, mag = convert_spectrum_units(np.c_[wavelength, flux], spec_units='ergscma', out_units='mag').T
    ax.plot(wav, mag, color='sandybrown')
    ylim_upper = mag.min() - .12
    ylim_lower = min(mag[wav>wav_lyA].max() + .5, 31)
    ax.set(ylim=(ylim_lower, ylim_upper), xlim=(wav.min(), wav.max()))

    annotate_lines(ax, redshift)
    ax.set_ylabel("AB Magnitude")

    xticks = ax.get_xticks().tolist()
    ax.set_xticks(xticks)
    ax.set_xticklabels([f"{x/10000:.1f}" for x in xticks])
    ax.set_xlabel("Observed Wavelength (microns)")
    if redshift:
        # upper tick to show rest-frame wavelength
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xticks(xticks)
        ax2.set_xticklabels([f"{x/(1+redshift)/10000:.2f}" for x in xticks],
                                fontsize=10)
        ax2.set_xlabel("Rest-frame Wavelength")
                           
    return fig

def plot_sfh(sfh_list, redshift):
    fig, ax = plt.subplots(figsize=(6, 2))
    model_comp = { "redshift": redshift}
    for sfh in sfh_list:
        sfh_type = sfh['type']
        model_comp[sfh_type] = sfh
        #add_sfh(sfh, ax)
    _sfh = star_formation_history(model_comp)
    ax.text(0.95, 0.8, f"log(Mstar)={_sfh.stellar_mass:.2f}",
            transform=ax.transAxes, ha='right')
    add_sfh(_sfh, ax)
    return fig