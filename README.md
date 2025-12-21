# Galaxy Spectrum Modeling Demo

🔗 Live demo: https://galaxy-spectrum-demo.streamlit.app

This Streamlit app provides an interactive visualization of a galaxy
spectrum model, allowing users to explore the effects of physical
parameters such as stellar age, metallicity, dust attenuation, and redshift.

Keywords:
galaxy spectrum, SED modeling, astrophysics, Streamlit, astronomy



## To Deploy on Your Local Machine

1. Clone the repository:
   ```bash
   git clone https://github.com/bcj1n/galaxy-spectrum-demo.git
   ```


2. Activate your virtual environment (if you have one) and install the required packages (and most important, Streamlit):
   ```bash
   conda activate your_env_name  # if using conda
   pip install -r requirements.txt
   pip install streamlit
   ```


3. Before running the app, ensure you have proper configuration for `bagpipes_dev`:

    In `bagpipes_dev/utils.py`, set the `install_dir` variable to point to the local directory where `bagpipes` (not `bagpipes_dev`) is located. For example, replace line 73-76 with:
    ```
    install_dir = "/path/to/your/bagpipes/"
    ```


4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
   This will open a tab in your default web browser where you can interact with the app.