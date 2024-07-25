import datetime  # Core Python Module
import pytz
import streamlit as st  # pip install streamlit

import database as db
import settings as s
import config

def update_visibility():
    if st.session_state.closer_disp == 'Closed':
        st.session_state.visible = True
    else:
        st.session_state.visible = False

def reset_form():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
    
    
def close_form():
    if 'visible' not in st.session_state:
        st.session_state.visible = False
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'close_date' not in st.session_state:
        st.session_state.close_date = datetime.date.today()
    if 'close_time' not in st.session_state:
        st.session_state.close_time = congifg.get_nearest_15_minute_time()
    if 'on_time' not in st.session_state:
        st.session_state.on_time = 'Yes'
    if 'cx_email' not in st.session_state:
        st.session_state.cx_email = ''
    if 'closer_name' not in st.session_state:
        st.session_state.closer_name = config.closers[0]
    if 'closer_disp' not in st.session_state:
        st.session_state.closer_disp = config.dispositions[0]
    if 'lender' not in st.session_state:
        st.session_state.lender = config.lenders[0]
    if 'syst_size' not in st.session_state:
        st.session_state.syst_size = 0
    if 'purch_pref' not in st.session_state:
        st.session_state.purch_pref = config.purch_prefs[0]
    if 'sold_ppw' not in st.session_state:
        st.session_state.sold_ppw = 0
    if 'loan_amount' not in st.session_state:
        st.session_state.loan_amount = 0
    if 'percent_offset' not in st.session_state:
        st.session_state.percent_offset = 100
    if 'lock_close' not in st.session_state:
        st.session_state.lock_close = False
    if 'vid_call' not in st.session_state:
        st.session_state.vid_call = False
    if 'both_spouses' not in st.session_state:
        st.session_state.both_spouses = False
    if 'had_UB' not in st.session_state:
        st.session_state.had_UB = False

    st.header("This form is to be filled out after every appointment that you have, whether they answered or not.")
    
    close_col1, close_col2 = st.columns([2, 3])
    
    with close_col1:
        s.questionCSS("Date you called")
        config.close_date = st.date_input("", value=st.session_state.close_date).isoformat()
    
    with close_col2:
        close_sub_col1, close_sub_col2 = st.columns(2)
        
        with close_sub_col1:
            s.questionCSS("Time you called")
            config.close_time = st.time_input("", value=st.session_state.close_time).isoformat()
        
        with close_sub_col2:
            s.questionCSS("Did you call on time?")
            config.on_time = st.radio("", ['Yes', 'No'], index=['Yes', 'No'].index(st.session_state.on_time))
            placeholder = st.empty()
    s.questionCSS("Customer's email")
    config.cx_email = st.text_area(
        label="",
        height=100,
        placeholder="Write here",
        value=st.session_state.cx_email
    )
    close_col3, close_col4 = st.columns(2)
    
    with close_col3:
        s.questionCSS("Closer Name")
        config.closer_name = st.selectbox(
            '',
            config.closers,
            index=config.closers.index(st.session_state.closer_name)
        )
    
    with close_col4:
        s.questionCSS("Call Disposition")
        config.closer_disp = st.selectbox(
            '',
            config.dispositions,
            index=config.dispositions.index(st.session_state.closer_disp),
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
            config.lender = st.selectbox(
                '',
                config.lenders,
                index=config.lenders.index(st.session_state.lender),
                key='lender',
            )
            
            s.questionCSS("System Size")
            config.syst_size = st.number_input(
                '',
                value=st.session_state.syst_size,
                key='syst_size'
            )
        
        with close_col6:
            s.questionCSS("Loan/CASH/PPA")
            config.purch_pref = st.selectbox(
                '',
                config.purch_prefs,
                index=config.purch_prefs.index(st.session_state.purch_pref),
                key='purch_pref'
            )
            
            s.questionCSS("Sold PPW")
            config.sold_ppw = st.number_input(
                '',
                value=st.session_state.sold_ppw,
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
        config.loan_amount = st.number_input('', value=st.session_state.loan_amount)
        
        st.markdown(
            """
            <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: -100px;">
                <label style='font-size: 17px; font-family: Arial, sans-serif;'>Percent Offset %</label>
            </div>
            """,
            unsafe_allow_html=True
        )
        config.percent_offset = st.slider("", value=st.session_state.percent_offset, min_value=50, max_value=150)
        
    close_col7, close_col8 = st.columns(2)
    
    with close_col7:
        st.markdown(
            "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Lock Close?</p>",
            unsafe_allow_html=True)
        config.lock_close = st.checkbox('', value=st.session_state.lock_close, key='lock_close')
        
        st.markdown(
            "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Video Call?</p>",
            unsafe_allow_html=True)
        config.vid_call = st.checkbox('', value=st.session_state.vid_call, key='vid_call')
    
    with close_col8:
        st.markdown(
            "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>All decision makers?</p>",
            unsafe_allow_html=True)
        config.both_spouses = st.checkbox('', value=st.session_state.both_spouses, key='both_spouses')
        
        st.markdown(
            "<p style='font-size: 17px; font-family: Arial, sans-serif; margin-bottom: 0px;'>Had UB?</p>",
            unsafe_allow_html=True)
        config.had_UB = st.checkbox('', value=st.session_state.had_UB, key='had_UB')
        
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
                reset_form()
        elif config.closer_disp == "We didn't call":
            new_data = [
                config.set_date, config.set_time, config.setter_name, config.cx_state, config.cx_name,
                config.cx_email, config.set_comment, config.unpaid_lead, config.close_date, '', '',
                config.closer_name, config.closer_disp, config.lender, config.syst_size, config.purch_pref,
                config.close_comment, '', '', '', '', '', '', ''
            ]
            db.upsert_email(config.cx_email, new_data)
            st.success("Customer information saved!")
            reset_form()
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
                reset_form()
