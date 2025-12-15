import streamlit as st
import numpy as np

from model.spectrum import generate_bagpipes_spectrum
from plots.plotting import plot_spectrum, plot_spectrum_mag, plot_sfh
from utils import cosmo

st.set_page_config(
    page_title="Galaxy Spectrum Modeling Demo | Interactive SED Explorer",
    page_icon="🌌",
    layout="wide"
)
st.markdown(
    """
    <meta name="description" content="Interactive demo for modeling galaxy spectra and SEDs. Explore age, metallicity, dust, and redshift effects.">
    <meta name="google-site-verification" content="fgzb16Wxs42rXspXIhZgQPJfBFpSOReLCPksDagSTnQ" />
    """,
    unsafe_allow_html=True
)

st.title("Interactive Galaxy Spectrum Model")

# --- Sidebar: parameters ---
st.sidebar.header("Model Parameters")

## SFH parameters
mass_formed = st.sidebar.slider("Mass formed (log)", 6.0, 14.0, 10.0)
age = st.sidebar.slider("Stellar age (Gyr)", 0.01, 3.5, .1)
metallicity = st.sidebar.selectbox(
    "Metallicity (Z)",
    [0.001, 0.004, 0.02]
)

## Dust parameters
dust_av = st.sidebar.slider("Dust Av (mag)", 0.0, 3.0, 0.5)
dust_delta = st.sidebar.slider("Dust slope delta", -1.2, 0.4, 0.0)

## Nebular parameters
logU = st.sidebar.slider("Ionization parameter logU", -4.0, -1.0, -2.0)

## Redshift
redshift = st.sidebar.slider("Redshift", 2.0, 10.0, 7.0)

sfh = {
    "type": "constant",
    "tstart": cosmo.age(redshift).value-age if (cosmo.age(redshift).value-age)>0 else 0.001,
    "tstop": cosmo.age(redshift).value-0.003,
    "metallicity": metallicity,
    "massformed": mass_formed,
}

dust = {
    "type": "Salim",
    "Av": dust_av,
    "delta": dust_delta,
    "B": 0.0,
}

nebular = {
    "logU": logU,
}

# --- Compute model ---
@st.cache_data
def compute_model(sfh, dust, nebular, redshift):
    return generate_bagpipes_spectrum(sfh, dust, nebular, redshift)

wav, spec = compute_model(
    sfh,
    dust,
    nebular,
    redshift
)
# --- Plot SFH ---
st.subheader("Star Formation History")
fig = plot_sfh(sfh, redshift)
st.pyplot(fig, use_container_width=False)
st.markdown("""
This demo uses [Bagpipes](https://bagpipes.readthedocs.io/en/latest/) to generate galaxy spectra based on user-defined parameters.
""")

# --- Plot spectrum ---
st.subheader("Model Galaxy Spectrum")
st.text(f"Computed spectrum at redshift z={redshift} with {len(wav)} wavelength points.")
st.text(f"Maximum flux: {spec.max():.2e} erg/s/cm²/Å")

is_wav_show = (wav >= 800) & (wav <= 8500)
fig = plot_spectrum_mag(wav[is_wav_show]*(1+redshift), spec[is_wav_show], redshift=redshift)
st.pyplot(fig, use_container_width=False)
st.markdown("""
Adjust the parameters in the sidebar to see how they affect the galaxy spectrum and star formation history.
""")