import config
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import streamlit as st

import dataVisualization
import setForm
import closeForm



# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Setter Form", "Closer Form" ,"Data Visualization"],
    icons=["pencil-fill", "bi-brightness-high-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

if selected == "Setter Form":
    setForm.set_form()

if selected == "Closer Form":
    closeForm.close_form()

if selected == "Data Visualization":
    dataVisualization.data()







