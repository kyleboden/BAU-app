import datetime  # Core Python Module
import streamlit as st  # pip install streamlit

import database as db
import settings as s
import config

def update_visibility():
    if st.session_state.closer_disp == 'Closed':
        st.session_state.visible = True
    else:
        st.session_state.visible = False

def close_form():
    if 'visible' not in st.session_state:
        st.session_state.visible = False
    
    st.header("This form is to be filled out after every appointment that you have, whether they answered or not.")
    
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
        config.closer_disp = st.selectbox(
            '',
            config.dispositions,
            key='closer_disp',
            on_change=update_visibility
        )
    s.questionCSS("Customer's email")
        config.cx_email = st.text_area(
            label="",
            height=100,
            placeholder="Write here"
        )
    if st.session_state.visible:
        placeholder = st.empty()

        
        "---"
        
        st.markdown(
            """
            <div style="text-align: center; font-size: 24px; font-weight: bold; padding-bottom: 20px;">
                System Details
            </div>
            """,
            unsafe_allow_html=True
        )
        
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
        
        st.markdown(
            """
            <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: -100px;">
                <label style='font-size: 17px; font-family: Arial, sans-serif;'>Loan amount $</label>
            </div>
            """,
            unsafe_allow_html=True
        )
        config.loan_amount = st.number_input('')
        
        st.markdown(
            """
            <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: -100px;">
                <label style='font-size: 17px; font-family: Arial, sans-serif;'>Percent Offset %</label>
            </div>
            """,
            unsafe_allow_html=True
        )
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
    
    with st.form("entry_form", clear_on_submit=True):
        st.session_state.submitted = st.form_submit_button("Submit")
        
    if st.session_state.submitted:
        if config.closer_disp == "Closed":
            required_fields = [
                config.close_date, config.close_time, config.on_time, config.closer_name,
                config.closer_disp, config.cx_email, config.lender, config.syst_size,
                config.purch_pref, config.sold_ppw, config.loan_amount, config.percent_offset
            ]
            if not all(required_fields):
                st.error("Please fill in all fields before submitting.")
            else:
                new_data = [
                    config.set_date, config.set_time, config.setter_name, config.cx_state, config.cx_name,
                    config.cx_email, config.set_comment, config.unpaid_lead, config.close_date, config.close_time,
                    config.on_time, config.closer_name, config.closer_disp, config.lender, config.syst_size,
                    config.purch_pref, config.close_comment, config.sold_ppw, config.loan_amount, config.percent_offset,
                    config.lock_close, config.vid_call, config.both_spouses, config.had_UB
                ]
                db.upsert_email(config.cx_email, new_data)
                st.success("Customer information saved!")
                st.experimental_rerun()
        elif config.closer_disp == "We didn't call":
            new_data = [
                config.set_date, config.set_time, config.setter_name, config.cx_state, config.cx_name,
                config.cx_email, config.set_comment, config.unpaid_lead, config.close_date, '', '',
                config.closer_name, config.closer_disp, config.lender, config.syst_size, config.purch_pref,
                config.close_comment, '', '', '', '', '', '', ''
            ]
            db.upsert_email(config.cx_email, new_data)
            st.success("Customer information saved!")
            st.experimental_rerun()
        else:
            required_fields = [
                config.close_date, config.close_time, config.on_time, config.closer_name,
                config.closer_disp, config.cx_email
            ]
            if not all(required_fields):
                st.error("Please fill in all fields before submitting.")
            else:
                new_data = [
                    config.set_date, config.set_time, config.setter_name, config.cx_state, config.cx_name,
                    config.cx_email, config.set_comment, config.unpaid_lead, config.close_date, config.close_time,
                    config.on_time, config.closer_name, config.closer_disp, config.lender, config.purch_pref,
                    config.close_comment, config.sold_ppw, config.loan_amount, config.percent_offset, config.lock_close,
                    config.vid_call, config.both_spouses, config.had_UB
                ]
                db.upsert_email(config.cx_email, new_data)
                st.success("Customer information saved!")
                st.experimental_rerun()
