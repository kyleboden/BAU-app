import datetime  # Core Python Module
import streamlit as st  # pip install streamlit

import database as db
import settings as s
import config

def close_form():
    st.header("This form is to be filled out after every appointment that you have, whether they answered or not.")
    
    # Define the form
    with st.form("entry_form", clear_on_submit=True):
        close_col1, close_col2 = st.columns([2, 3])
        with close_col1:
            s.questionCSS("Date you called")
            config.close_date = st.date_input("", value=datetime.date.today()).isoformat()
        with close_col2:
            close_sub_col1, close_sub_col2 = st.columns(2)
            with close_sub_col1:
                s.questionCSS("Time you called")
                config.close_time = st.time_input("", value=datetime.time(14, 00)).isoformat()
            with close_sub_col2:
                s.questionCSS("Did you call on time?")
                config.on_time = st.radio("", ['Yes', 'No'])

        close_col3, close_col4 = st.columns(2)
        with close_col3:
            s.questionCSS("Closer Name")
            config.closer_name = st.selectbox(
                '',
                config.closers
            )
        with close_col4:
            s.questionCSS("Call Disposition")
            disposition_options = config.dispositions
            config.closer_disp = st.selectbox(
                '',
                disposition_options,
                key='disposition_select',
                on_change=lambda: st.experimental_rerun()  # Re-run on change
            )

        s.questionCSS("Customer's email")
        config.cx_email = st.text_area(
            label="",
            height=100,
            placeholder="Write here"
        )
        "---"

        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; font-weight: bold; padding-bottom: 20px;">
                System Details
            </div>
            """,
            unsafe_allow_html=True
        )

        # Display additional fields if "Closed" is selected
        if st.session_state.get('disposition_select') == "Closed":
            close_col5, close_col6 = st.columns(2)
            with close_col5:
                s.questionCSS("Lender")
                config.lender = st.selectbox(
                    '',
                    config.lenders,
                    key='lender',
                )
                s.questionCSS("System Size")
                config.syst_size = st.number_input(
                    '',
                    key='syst_size'
                )
            with close_col6:
                s.questionCSS("Loan/CASH/PPA")
                config.purch_pref = st.selectbox(
                    '',
                    config.purch_prefs,
                    key='purch_pref'
                )
                s.questionCSS("Sold PPW")
                config.sold_ppw = st.number_input(
                    '',
                    key='sold_ppw'
                )

            # Centering the 'Loan amount $' label
            loan_amount_html = """
            <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: -100px;">
                <label style='font-size: 17px; font-family: Arial, sans-serif;'>Loan amount $</label>
            </div>
            """
            st.markdown(loan_amount_html, unsafe_allow_html=True)
            config.loan_amount = st.number_input('')

            percent_offset_html = """
            <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: -100px;">
                <label style='font-size: 17px; font-family: Arial, sans-serif;'>Percent Offset %</label>
            </div>
            """
            st.markdown(percent_offset_html, unsafe_allow_html=True)
            config.percent_offset = st.slider("", value=100, min_value=50, max_value=150)

            close_col7, close_col8 = st.columns(2)
            with close_col7:
                st.markdown(
                    "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Lock Close?</p>",
                    unsafe_allow_html=True)
                config.lock_close = st.checkbox('', key='lock_close')
                st.markdown(
                    "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Video Call?</p>",
                    unsafe_allow_html=True)
                config.vid_call = st.checkbox('', key='vid_call')

            with close_col8:
                st.markdown(
                    "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>All decision makers?</p>",
                    unsafe_allow_html=True)
                config.both_spouses = st.checkbox('', key='both_spouses')

                st.markdown(
                    "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Had UB?</p>",
                    unsafe_allow_html=True)
                config.had_UB = st.checkbox('', key='had_UB')

            "---"

        # Add the common field for additional notes
        config.close_comment = st.text_area("", placeholder="Leave any additional notes here ...")

        submitted = st.form_submit_button("Submit")
        if submitted:
            if config.closer_disp == "Closed":
                if not (config.close_date and config.close_time and config.on_time and config.closer_name and
                        config.closer_disp and config.cx_email and config.lender and config.syst_size and config.purch_pref
                        and config.sold_ppw and config.loan_amount and config.percent_offset):
                    st.error("Please fill in all fields before submitting.")
                else:
                    new_data = [config.set_date, config.set_time, config.setter_name, config.cx_state, config.cx_name,
                                config.cx_email, config.set_comment, config.unpaid_lead, config.close_date, config.close_time, config.on_time,
                                config.closer_name, config.closer_disp, config.lender, config.syst_size, config.purch_pref,
                                config.close_comment, config.sold_ppw, config.loan_amount, config.percent_offset, config.lock_close,
                                config.vid_call, config.both_spouses, config.had_UB]
                    db.upsert_email(config.cx_email, new_data)
                    st.success("Customer information saved!")
                    st.rerun()
            elif config.closer_disp == "We didn't call":
                new_data = [config.set_date, config.set_time, config.setter_name, config.cx_state, config.cx_name,
                                config.cx_email, config.set_comment, config.unpaid_lead, config.close_date, '', '',
                                config.closer_name, config.closer_disp, config.lender, config.syst_size, config.purch_pref,
                                config.close_comment, '', '', '', '',
                                '', '', '']
                db.upsert_email(config.cx_email, new_data)
                st.success("Customer information saved!")
                st.rerun()
            else:
                if not (config.close_date and config.close_time and config.on_time and config.closer_name and
                        config.closer_disp and config.cx_email):
                    st.error("Please fill in all fields before submitting.")
                else:
                    new_data = [config.set_date, config.set_time, config.setter_name, config.cx_state, config.cx_name,
                                config.cx_email, config.set_comment, config.unpaid_lead, config.close_date, config.close_time, config.on_time,
                                config.closer_name, config.closer_disp, config.lender, config.purch_pref,
                                config.close_comment, config.sold_ppw, config.loan_amount, config.percent_offset, config.lock_close,
                                config.vid_call, config.both_spouses, config.had_UB]
                    db.upsert_email(config.cx_email, new_data)
                    st.success("Customer information saved!")
                    st.rerun()
