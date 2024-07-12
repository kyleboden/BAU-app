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

    # Calculate total appointments per state
    state_counts = df.groupby('State').size().reset_index(name='Total Appts')

    # Calculate filtered appointments per state based on filters
    if call_disp_filt != '':
        df_call_filt = df[df['Closer Disposition'] == call_disp_filt]
    else:
        df_call_filt = df.copy()  # Use entire dataset if no call disposition filter applied

    if states_filt:
        df_call_filt = df_call_filt[df_call_filt['State'].isin(states_filt)]

    state_filtered_deals = df_call_filt.groupby('State').size().reset_index(name=call_disp_filt)


    # Donut chart for filtered appointments per state
    if call_disp_filt == '':
        donut_data = state_counts #objects
        donut_theta = 'Total Appts'
    else:
        donut_data = state_filtered_deals #objects
        donut_theta = call_disp_filt
    plost.donut_chart(
        data=donut_data,
        theta=donut_theta,
        color='State',
        use_container_width=True
    )

    #bar chart to show appointments per state
    y_pos = np.arange(len(donut_data))
    plt.figure(figsize=(10, 6))
    plt.bar(y_pos, donut_data[donut_theta], color='00a7e1')
    #plt.xticks(y_pos, donut_data['State'], rotation=45)
    plt.xlabel('State')
    plt.ylabel('Total Appointments')
    plt.title('Total Appointments per State')
    plt.tight_layout()
    st.pyplot(plt)
    
    #bar chart to show different disps
    

    #if call_disp_filt:
    disp_percent(df_call_filt, state_counts, call_disp_filt, state_filtered_deals)



def disp_percent(df, counts, disp_filt, state_filt):
    if disp_filt == '':
        # If no filter is selected, display a simplified dataframe
        simplified_df = counts.copy()
        simplified_df['Total Appts'] = counts['Total Appts'].astype(int)
        totals_row = pd.DataFrame({'State': 'Total', 'Total Appts': counts['Total Appts'].sum()}, index=[0])
        simplified_df = pd.concat([simplified_df, totals_row], ignore_index=True)

        # Display the simplified dataframe
        st.write("Total Appts for each State:")
        st.table(simplified_df.set_index('State'))

        return

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

