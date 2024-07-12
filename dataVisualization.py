import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter

import database
import config

import plost
import pandas as pd
import numpy as np

sheet = database.sheet

def data():
    #--- SIDEBAR ---

    
    call_disp_filt = st.sidebar.multiselect('Call Dispositions', config.dispositions)
    states_filt = st.sidebar.multiselect('States', config.states)
    setter_filt = st.sidebar.multiselect('Setter', config.setters)
    closer_filt = st.sidebar.multiselect('Closer', config.closers)
    df = pd.DataFrame(sheet.get_all_records())

    st.title("My Streamlit Dashboard")

    # Connecting filters to data
      
    # Calculate filtered appointments per state based on filters
    df_call_filt = df.copy()
    if states_filt:
        df_call_filt = df[df['State'].isin(states_filt)]
    if call_disp_filt:
        df_call_filt = df_call_filt[df_call_filt['Closer Disposition'].isin(call_disp_filt)]
    if setter_filt:
        df_call_filt = df_call_filt[df_call_filt['Setter Name'].isin(setter_filt)]
    if closer_filt:
        df_call_filt = df_call_filt[df_call_filt['Closer Name'].isin(closer_filt)]
        
    # Calculate total appointments per state
    state_counts = df_call_filt.groupby('State').size().reset_index(name='Total Appts')
    state_filtered_deals = df_call_filt.groupby('State').size().reset_index(name=call_disp_filt)


    if not call_disp_filt and not states_filt and not setter_filt and not closer_filt:
        data = state_counts #objects
        theta = 'Total Appts'
    else:
        data = state_filtered_deals #objects
        theta = call_disp_filt

    data = data.sort_values(by=theta, ascending=False)


    # Bar chart to show appointments per state
    y_pos = np.arange(len(data))
    plt.figure(figsize=(12, 10))
    plt.bar(y_pos, data[theta], color='#00a7e1')
    plt.xticks(y_pos, data['State'], rotation=45, fontsize = 12)  # Set x-ticks
    plt.xlabel('State', fontsize = 14)
    plt.ylabel('Total Appointments', fontsize = 14)

    test_disp_filt = call_disp_filt
    if call_disp_filt:
        title = f'Total {call_disp_filt} Appointments per State'
    else:
        title = 'Total Appointments per State'
        test_disp_filt = config.dispositions
    plt.title(title)

    plt.tight_layout()
    st.pyplot(plt)
    
    test_state_filt = states_filt
    if not states_filt:
        test_state_filt = config.states


    disp_percent(df_call_filt, state_counts, test_disp_filt, state_filtered_deals)
    
    #bar chart to show different disps
    disp_counts = df_call_filt['Closer Disposition'].value_counts().reset_index()
    disp_counts.columns = ['Disposition', 'Total Appointments']

    # Create a bar chart
    y_pos = np.arange(len(disp_counts))
    plt.figure(figsize=(10, 6))
    plt.bar(y_pos, disp_counts['Total Appointments'], color='#00a7e1')
    plt.xticks(y_pos, disp_counts['Disposition'], rotation=45)  # Set x-ticks to dispositions
    plt.xlabel('Dispositions')
    plt.ylabel('Total Appointments')
    plt.title('Total Appointments by Disposition')
    plt.tight_layout()
    st.pyplot(plt)

    #create 2 bar charts with closer and setter names and call disps

    
    #if closer_filt:
    



def disp_percent(df, counts, disp_filt, state_filt):

    merged_df = pd.merge(counts, state_filt, on='State', how='left')  # Merge total and filtered deals dfs

    # Calculate percentage of filtered deals and round to nearest whole number
    percent = (merged_df[disp_filt] / merged_df['Total Appts']) * 100
    percent_rounded = percent.round()

    # Handle NaN or infinite values
    percent_rounded = percent_rounded.replace([np.nan, np.inf, -np.inf], 0)

    # Add '%' sign to each percentage value
    merged_df['Percent'] = percent_rounded.astype(int).astype(str) + '%'

    # Add a row for totals
    totals_row = pd.DataFrame(merged_df.sum(numeric_only=True)).T
    totals_row['State'] = 'Total'

    # Calculate percentage for totals row
    totals_row_percent = (totals_row[disp_filt] / totals_row['Total Appts']) * 100
    totals_row_percent_rounded = round(totals_row_percent)
    totals_row['Percent'] = str(totals_row_percent_rounded.iloc[0]) + '%'

    # Ensure all columns are integers and handle NaN/infinite values
    merged_df['Total Appts'] = merged_df['Total Appts'].replace([np.nan, np.inf, -np.inf], 0).astype(int)
    merged_df[disp_filt] = merged_df[disp_filt].replace([np.nan, np.inf, -np.inf], 0).astype(int)
    totals_row['Total Appts'] = totals_row['Total Appts'].replace([np.nan, np.inf, -np.inf], 0).astype(int)
    totals_row[disp_filt] = totals_row[disp_filt].replace([np.nan, np.inf, -np.inf], 0).astype(int)

    # Append totals row to the DataFrame
    merged_df = pd.concat([merged_df, totals_row], ignore_index=True)

    # Display the merged dataframe
    st.write(f"Total and {disp_filt} with Percent for each State:")
    st.table(merged_df.set_index('State'))  # Hide the index column












#TODO add a tab to see which names are missing the closer form

