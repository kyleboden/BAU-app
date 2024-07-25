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

def clear_form():
    st.session_state.close_date = datetime.date.today()
    st.session_state.close_time = datetime.time(14, 00)
    st.session_state.on_time = 'Yes'
    st.session_state.cx_email = ''
    st.session_state.closer_name = config.closers[0] if config.closers else ''
    st.session_state.closer_disp = config.dispositions[0] if config.dispositions else ''
    st.session_state.lender = config.lenders[0] if config.lenders else ''
    st.session_state.syst_size = 0
    st.session_state.purch_pref = config.purch_prefs[0] if config.purch_prefs else ''
    st.session_state.sold_ppw = 0
    st.session_state.loan_amount = 0
    st.session_state.percent_offset = 100
    st.session_state.lock_close = False
    st.session_state.vid_call = False
    st.session_state.both_spouses = False
    st.session_state.had_UB = False

def close_form():
    if 'visible' not in st.session_state:
        st.session_state.visible = False
    
    st.header("This form is to be filled out after every appointment that you have, whether they answered or not.")
    
    close_col1, close_col2 = st.columns([2, 3])
    
    with close_col1:
        s.questionCSS("Date you called")
        st.session_state.close_date = st.date_input("", value=datetime.date.today())
    
    with close_col2:
        close_sub_col1, close_sub_col2 = st.columns(2)
        
        with close_sub_col1:
            s.questionCSS("Time you called")
            st.session_state.close_time = st.time_input("", value=datetime.time(14, 00))
        
        with close_sub_col2:
            s.questionCSS("Did you call on time?")
            st.session_state.on_time = st.radio("", ['Yes', 'No'])
            placeholder = st.empty()
    
    s.questionCSS("Customer's email")
    st.session_state.cx_email = st.text_area(
        label="",
        height=100,
        placeholder="Write here"
    )
    
    close_col3, close_col4 = st.columns(2)
    
    with close_col3:
        s.questionCSS("Closer Name")
        st.session_state.closer_name = st.selectbox(
            '',
            config.closers
        )
    
    with close_col4:
        s.questionCSS("Call Disposition")
        st.session_state.closer_disp = st.selectbox(
            '',
            config.dispositions,
            key='closer_disp',
            on_change=update_visibility
        )
    
    if st.session_state.visible:
        
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
            st.session_state.lender = st.selectbox(
                '',
                config.lenders,
                key='lender',
            )
            
            s.questionCSS("System Size")
            st.session_state.syst_size = st.number_input(
                '',
                key='syst_size'
            )
        
        with close_col6:
            s.questionCSS("Loan/CASH/PPA")
            st.session_state.purch_pref = st.selectbox(
                '',
                config.purch_prefs,
                key='purch_pref'
            )
            
            s.questionCSS("Sold PPW")
            st.session_state.sold_ppw = st.number_input(
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
        st.session_state.loan_amount = st.number_input('')
        
        st.markdown(
            """
            <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: -100px;">
                <label style='font-size: 17px; font-family: Arial, sans-serif;'>Percent Offset %</label>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.session_state.percent_offset = st.slider("", value=100, min_value=50, max_value=150)
        
    close_col7, close_col8 = st.columns(2)
    
    with close_col7:
        st.markdown(
            "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Lock Close?</p>",
            unsafe_allow_html=True)
        st.session_state.lock_close = st.checkbox('', key='lock_close')
        
        st.markdown(
            "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Video Call?</p>",
            unsafe_allow_html=True)
        st.session_state.vid_call = st.checkbox('', key='vid_call')
    
    with close_col8:
        st.markdown(
            "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>All decision makers?</p>",
            unsafe_allow_html=True)
        st.session_state.both_spouses = st.checkbox('', key='both_spouses')
        
        st.markdown(
            "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Had UB?</p>",
            unsafe_allow_html=True)
        st.session_state.had_UB = st.checkbox('', key='had_UB')
        
        "---"
    
    with st.form("entry_form", clear_on_submit=True):
        submitted = st.form_submit_button("Submit")
        
    if submitted:
        if config.closer_disp == "Closed":
            required_fields = [
                st.session_state.close_date, st.session_state.close_time, st.session_state.on_time, st.session_state.closer_name,
                st.session_state.closer_disp, st.session_state.cx_email, st.session_state.lender, st.session_state.syst_size,
                st.session_state.purch_pref, st.session_state.sold_ppw, st.session_state.loan_amount, st.session_state.percent_offset
            ]
            if not all(required_fields):
                st.error("Please fill in all fields before submitting.")
            else:
                new_data = [
                    config.set_date, config.set_time, config.setter_name, config.cx_state, config.cx_name,
                    st.session_state.cx_email, config.set_comment, config.unpaid_lead, st.session_state.close_date, st.session_state.close_time,
                    st.session_state.on_time, st.session_state.closer_name, st.session_state.closer_disp, st.session_state.lender, st.session_state.syst_size,
                    st.session_state.purch_pref, config.close_comment, st.session_state.sold_ppw, st.session_state.loan_amount, st.session_state.percent_offset,
                    st.session_state.lock_close, st.session_state.vid_call, st.session_state.both_spouses, st.session_state.had_UB
                ]
                db.upsert_email(st.session_state.cx_email, new_data)
                st.success("Customer information saved!")
                clear_form()  # Clear form fields
                st.experimental_rerun()
        elif config.closer_disp == "We didn't call":
            new_data = [
                config.set_date, config.set_time, config.setter_name, config.cx_state, config.cx_name,
                st.session_state.cx_email, config.set_comment, config.unpaid_lead, st.session_state.close_date, '', '',
                st.session_state.closer_name, st.session_state.closer_disp, st.session_state.lender, st.session_state.syst_size, st.session_state.purch_pref,
                config.close_comment, '', '', '', '', '', '', ''
            ]
            db.upsert_email(st.session_state.cx_email, new_data)
            st.success("Customer information saved!")
            clear_form()  # Clear form fields
            st.experimental_rerun()
        else:
            required_fields = [
                st.session_state.close_date, st.session_state.close_time, st.session_state.on_time, st.session_state.closer_name,
                st.session_state.closer_disp, st.session_state.cx_email
            ]
            if not all(required_fields):
                st.error("Please fill in all fields before submitting.")
            else:
                new_data = [
                    config.set_date, config
