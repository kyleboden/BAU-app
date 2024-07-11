import datetime  # Core Python Module
import streamlit as st  # pip install streamlit

import database as db
import settings as s
import config

#TODO add check box for AMP Lead
def set_form():
    st.header("This form is to be filled out after every appointment that is set.")
    with st.form("entry_form", clear_on_submit=True):
        set_col1, set_col2 = st.columns(2)
        with set_col1:
            s.questionCSS("Date you called")
            config.set_date = st.date_input("", value=datetime.date.today()).isoformat()
        with set_col2:
            s.questionCSS("Time you called")
            config.set_time = st.time_input("", value=datetime.time(14, 00)).isoformat()
        # ub file uploader
        s.questionCSS("Upload Utility Bill here")
        ub_file = st.file_uploader(label='')

        st.markdown(
            "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Unpaid Lead?</p>",
            unsafe_allow_html=True)
        config.unpaid_lead = st.checkbox('', key='unpaid_lead')

        "---"

        set_col3, set_col4 = st.columns(2)
        with set_col3:
            s.questionCSS("Setter Name")
            config.setter_name = st.selectbox(
                '',
                config.setters
            )
        with set_col4:
            s.questionCSS("Customer\'s State")
            config.cx_state = st.selectbox(
                '',
                config.states
            )

        set_col5, set_col6 = st.columns(2)
        with set_col5:
            s.questionCSS("Customer's Full Name")
            config.cx_name = st.text_area(
                label="",
                height=100,
                max_chars=50,
                placeholder="Write here"
            )
        with set_col6:
            s.questionCSS("Customer's email")
            config.cx_email = st.text_area(
                label="",
                height=100,
                placeholder="Write here"
            )

        config.set_comment = st.text_area("", placeholder="Leave any additional notes for the closer here ...")

        submitted = st.form_submit_button("Submit")
        if submitted:
            if not (config.set_date and config.set_time and config.setter_name and config.cx_state and config.cx_name
                    and config.cx_email):
                st.error("Please fill in all fields before submitting.")
            else:
                new_data = [config.set_date, config.set_time,  config.setter_name, config.cx_state, config.cx_name,
                            config.cx_email, config.set_comment, config.unpaid_lead,]
                db.upsert_email(config.cx_email, new_data)
                config.cx_email = ''
                st.success("Customer information saved!")
                st.rerun()
