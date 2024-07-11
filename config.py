import calendar  # Core Python Module
import streamlit as st  # pip install streamlit

page_title = "AMP Smart BAU Form"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
setters = ['','Hunter Bolen', 'Jake Bolen', 'Danny Timmreck', 'Joshua Killpack', 'Closer Self-Gen']
closers = ['','Kyle Boden', 'Spencer Jackson', 'Michael Oliveira']
states = ['', 'CA', 'CT',  'FL', 'IA', 'IL', 'GA', 'KY', 'MA', 'ME', 'MO', 'NH', 'NJ', 'OH', 'RI', 'TX', 'UT', 'VT']
dispositions = ['', 'Closed', 'No Sit', 'Not Interested', 'Reschedule', 'Pitched, need to Follow Up', 'DNQ', 'We didn\'t call']
system_details = ['', 'System Size in kW', 'Sold PPW', 'Loan Amount']
lenders = ['', 'Enfin', 'Dividend', 'Goodleap', 'Sunlight', 'Mosaic', 'Enium', 'Skylight', 'Palmetto', 'Sunnova', 'Thrive', 'Sungage', 'Cash']
purch_prefs = ['', 'Loan', 'Cash', 'PPA']
set_date = ''
set_time = ''
setter_name = ''
cx_state = ''
cx_name = ''
cx_email = ''
set_comment = ''
close_date = ''
close_time = ''
closer_name = ''
closer_disp = ''
lender = ''
purch_pref = ''
close_comment = ''
syst_size = ''
sold_ppw = ''
loan_amount = ''
#check boxes
lock_close = False
vid_call = False
both_spouses = False
had_UB = False
unpaid_lead = False
on_time = ''
percent_offset = ''
#did lock close
#video call
#both spouses
#hadUB
#percent offset

# --------------------------------------
#st.set_page_config(page_title="BAU", page_icon='☀️')
#st.title(page_title + " " + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
#years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
