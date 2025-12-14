import numpy as np
import bagpipes_dev as pipes

from utils import convert_spectrum_units

def generate_bagpipes_spectrum(
    sfh,
    dust,
    nebular,
    redshift,):
    """
    Returns model flux on input wavelength grid.
    All heavy logic lives here.
    """
    sfh_type = sfh["type"]
    model_components = {
        "redshift": redshift,
        sfh_type: sfh,
        "dust": dust,
        "nebular": nebular,
    }
    model = pipes.model_galaxy(model_components, spec_wavs=np.linspace(3000, 9000, 200))
    return model.wavelengths, model.spectrum_full
