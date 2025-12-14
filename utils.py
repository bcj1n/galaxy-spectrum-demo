import numpy as np
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70., Om0=0.3)

def convert_spectrum_units(spectrum, spec_units, out_units='ergscma'):
    """
    Convert the units of the spectrum to the desired output units.
    Supported input units are "ergscma" (erg/s/cm^2/AA), "mujy" (microJy) and "mag" (AB magnitude).
    Supported output units are "ergscma", "mujy" and "mag".
    """
    conversion = 10**-29*2.9979*10**18/spectrum[:, 0]**2
    spec_out = spectrum.copy()

    if not spec_units == out_units:
        if spec_units == "mujy" and out_units == "ergscma":
            spec_out[:, 1:] *= np.tile(conversion, (spec_out.shape[1]-1, 1)).T
     
        elif spec_units == "ergscma" and out_units == "mujy":
            spec_out[:, 1:] /= np.tile(conversion, (spec_out.shape[1]-1, 1)).T

        elif spec_units == "ergscma" and out_units == "mag":
            spec_out[:, 1:] /= np.tile(conversion, (spec_out.shape[1]-1, 1)).T
            spec_out[:, 1:] = -2.5 * np.log10(spec_out[:, 1:]/3631.*10**-6)
        else:
            raise ValueError(f"Conversion from {spec_units} to {out_units} not implemented yet.")

    return spec_out