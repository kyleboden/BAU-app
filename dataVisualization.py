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

    call_disp_filt = st.sidebar.selectbox('Call Dispositions', config.dispositions)
    states_filt = st.sidebar.multiselect('States', config.states)
    df = pd.DataFrame(sheet.get_all_records())

    st.title("My Streamlit Dashboard")

    # Connecting filters to data
    st.subheader("Pie Chart")

    

    # Calculate filtered appointments per state based on filters
    if states_filt:
        df_call_filt = df[df['State'].isin(states_filt)]
    else:
        df_call_filt = df.copy()
    if call_disp_filt != '':
        df_call_filt = df_call_filt[df_call_filt['Closer Disposition'] == call_disp_filt]
        
    # Calculate total appointments per state
    state_counts = df_call_filt.groupby('State').size().reset_index(name='Total Appts')


    state_filtered_deals = df_call_filt.groupby('State').size().reset_index(name=call_disp_filt)


    # Donut chart for filtered appointments per state
    if call_disp_filt == '' and not states_filt:
        donut_data = state_counts #objects
        donut_theta = 'Total Appts'
    else:
        donut_data = state_filtered_deals #objects
        donut_theta = call_disp_filt

    donut_data = donut_data.sort_values(by=donut_theta, ascending=False)
    plost.donut_chart(
        data=donut_data,
        theta=donut_theta,
        color='State',
        use_container_width=True
    )
    set_col11, set_col12 = st.columns(2)

    with set_col11:
        # Bar chart to show appointments per state
        y_pos = np.arange(len(donut_data))
        plt.figure(figsize=(12, 10))
        plt.bar(y_pos, donut_data[donut_theta], color='#00a7e1')
        plt.xticks(y_pos, donut_data['State'], rotation=45, fontsize = 12)  # Set x-ticks
        plt.xlabel('State', fontsize = 14)
        plt.ylabel('Total Appointments', fontsize = 14)

        if call_disp_filt:
            title = f'Total {call_disp_filt} Appointments per State'
        else:
            title = 'Total Appointments per State'
        plt.title(title)

        plt.tight_layout()
        st.pyplot(plt)

    with set_col12:
        #if call_disp_filt:
        disp_percent(df_call_filt, state_counts, call_disp_filt, state_filtered_deals)
    
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

