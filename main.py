from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import streamlit as st
page_title = "BAU"
page_icon = '☀️'

#st.set_page_config(page_title=page_title, page_icon=page_icon)
#st.title(page_title + " " + page_icon)
st.set_page_config(page_title="BAU", page_icon='☀️')
#st.title(page_title + " " + page_icon)

import config
import dataVisualization
import setForm
import closeForm

#st.set_page_config(page_title="BAU", page_icon='☀️')
#st.title(config.page_title + " " + config.page_icon)


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







