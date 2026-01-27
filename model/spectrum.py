import numpy as np
import bagpipes_dev as pipes

from utils import convert_spectrum_units

def generate_bagpipes_spectrum(
    sfh_list,
    dust,
    nebular,
    redshift,):
    """
    Returns model flux on input wavelength grid.
    All heavy logic lives here.
    """
    model_components = {
        "redshift": redshift,
        "dust": dust,
        "nebular": nebular,
    }
    for sfh in sfh_list:
        sfh_type = sfh["type"]
        model_components[sfh_type] = sfh
    model = pipes.model_galaxy(model_components, spec_wavs=np.linspace(3000, 9000, 200))
    return model.wavelengths, model.spectrum_full
