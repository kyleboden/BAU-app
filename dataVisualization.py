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

    if call_disp_filt:
        title = f'Total {call_disp_filt} Appointments per State'
    else:
        title = 'Total Appointments per State'
    plt.title(title)

    plt.tight_layout()
    st.pyplot(plt)
    plt.close() 


    disp_percent(df_call_filt, state_counts, call_disp_filt, state_filtered_deals)

    
    # Total appointments by Disp bar chart
    disp_counts = df_call_filt['Closer Disposition'].value_counts().reset_index()
    disp_counts.columns = ['Disposition', 'Total Appointments']

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
    if not disp_filt:
        # If no filter is selected, display a simplified dataframe
        simplified_df = counts.copy()
        simplified_df['Total Appts'] = counts['Total Appts'].astype(int)
        totals_row = pd.DataFrame({'State': ['Total'], 'Total Appts': [counts['Total Appts'].sum()]})
        simplified_df = pd.concat([simplified_df, totals_row], ignore_index=True)

        # Display the simplified dataframe
        st.write("Total Appts for each State:")
        st.table(simplified_df.set_index('State'))

        return

    # Merge total and filtered deals dfs
    merged_df = pd.merge(counts, state_filt, on='State', how='left')

    # Calculate percentage of filtered deals and round to nearest whole number
    merged_df['Percent'] = (merged_df['Filtered Deals'] / merged_df['Total Appts'] * 100).fillna(0).astype(int).astype(str) + '%'

    # Add a row for totals
    totals_row = pd.DataFrame({'State': ['Total'], 'Total Appts': [merged_df['Total Appts'].sum()], 'Filtered Deals': [merged_df['Filtered Deals'].sum()]})
    totals_row['Percent'] = (totals_row['Filtered Deals'] / totals_row['Total Appts'] * 100).fillna(0).astype(int).astype(str) + '%'

    # Append totals row to the DataFrame
    merged_df = pd.concat([merged_df, totals_row], ignore_index=True)

    # Display the merged dataframe
    st.write(f"Total and {disp_filt} with Percent for each State:")
    st.table(merged_df.set_index('State'))











#TODO add a tab to see which names are missing the closer form

