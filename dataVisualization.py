import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

import pandas as pd
import numpy as np
from datetime import date

import database
import config

sheet = database.sheet
AMP_Logo_Blue = "images/AMP_Logo_Blue.png"
# Define the time blocks and reindex the data
time_blocks = pd.date_range("08:00", "18:00", freq="60T").time
time_blocks_str = [t.strftime("%H:%M:%S") for t in time_blocks]
time_blocks = [pd.to_datetime(t).time() for t in time_blocks_str]

def generate_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')
    
def data():
    df = pd.DataFrame(sheet.get_all_records())
    df_call_filt = df.copy()  # should be this if no other filters are applied
    df_call_filt = month_year_col(df_call_filt)

    st.sidebar.image(AMP_Logo_Blue, width=100)
    st.sidebar.header("Please Filter Here:")
    data_options = st.sidebar.selectbox('Choose which Dashboard to see', options = ['Team', 'Closer', 'Setter', 'Detailed Data'])
    month_year_filt = st.sidebar.multiselect('Date', options=df_call_filt["Month_Year"].unique())
    if month_year_filt:
        df_call_filt = df_call_filt[df_call_filt['Month_Year'].isin(month_year_filt)]

    #csv_button = st.sidebar.button('Click to generate list of non-recorded appts')
    st.title(f"{data_options} Dashboard{' - ' + ', '.join(month_year_filt) if month_year_filt else ''}")
    st.markdown("---")

    st.sidebar.markdown("---")
    #st.sidebar.markdown("###")

    df_call_filt['Set Time'] = pd.to_datetime(df_call_filt['Set Time']).dt.round('60min').dt.time
    df_call_filt['Close Time'] = pd.to_datetime(df_call_filt['Close Time']).dt.round('60min').dt.time

    if data_options == 'Team':
        t_dashboard(df_call_filt)
    elif data_options == 'Closer':
        c_dashboard(df_call_filt)
    elif data_options == 'Setter':
        s_dashboard(df_call_filt)
    elif data_options == 'Detailed Data':
        d_dashboard(df_call_filt, month_year_filt)

    st.sidebar.markdown("---")



    # Filtering DataFrame for non-recorded appointments
    nonrecord_apts_df = df[df['Closer Disposition'] == '']
    password_from_secrets = st.secrets["general"]["password"]

    
    # Sidebar password input
    password = st.sidebar.text_input("Enter password to generate the list:", type="password")
    
    # Check if the password is correct
    if password == password_from_secrets:
        st.sidebar.download_button(
            "Click to generate list of non-recorded appts",
            generate_csv(nonrecord_apts_df),
            f"unrecorded_appts_{date.today()}.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.sidebar.write("INCORRECT: Enter the correct password to enable the button.")



def t_dashboard(df):




    #KPI's
    total_sets = len(df)
    total_sets_happened = (df['Closer Disposition'] != '').sum()
    total_happened_df = df[df['Closer Disposition'] != '']
    total_nosits = (df['Closer Disposition'] == 'No Sit').sum()
    total_sits = total_sets_happened - total_nosits # maybe - reschedules
    total_close = (df['Closer Disposition'] == 'Closed').sum()


    #st.write(total_close)

    left_col, middle_col, right_col = st.columns(3)

    with left_col:
        st.markdown(f"""
        <div style="background-color: #ECFCFF; border-radius: 15px; padding: 20px; text-align: center;">
            <h3 style="margin: 0; padding: 0;">Total Sets:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_sets}</h1>
            <h3 style="margin: 0; padding: 0; margin-top: 15px;">Recorded Appts:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_sets_happened}</h1>
        </div>
        """, unsafe_allow_html=True)

    with middle_col:
        st.markdown(f"""
        <div style="background-color: #E6F4F1; border-radius: 15px; padding: 20px; text-align: center;">
            <h3 style="margin: 0; padding: 0;">Total Sits:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_sits}</h1>
            <h3 style="margin: 0; padding: 0; margin-top: 15px;">Sit rate:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{((total_sits / total_sets_happened) * 100).astype(int)}%</h1>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown(f"""
        <div style="background-color: #95B0B7; border-radius: 15px; padding: 20px; text-align: center;">
            <h3 style="margin: 0; padding: 0;">Total Closes:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_close}</h1>
            <h3 style="margin: 0; padding: 0; margin-top: 15px;">Close rate:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{((total_close / total_sets_happened) * 100).astype(int)}%</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- BAR CHARTS ---
    closes_df = df[df['Closer Disposition'] == 'Closed']
    noSits_df = df[df['Closer Disposition'] == 'No Sit']

    # Closes by Close Bar
    closes_by_closer = closes_df.groupby('Closer Name').size().sort_values(ascending=False)
    #st.bar_chart(closes_by_closer)

    fig_closes_closer = px.bar(
        closes_by_closer,
        x=closes_by_closer.index,
        y=closes_by_closer.values,
        orientation="v",
        title="<b>Closes by Closer</b>",
        color_discrete_sequence=["#2fddff"] * len(closes_by_closer),
        labels={"y": "Number of Closes"}
    )
    fig_closes_closer.update_layout(
        xaxis_title=None,
        title_x=0.5
    )

    #st.bar_chart(closes_by_closer)
    # Closes by Setter Bar
    closes_by_setter = closes_df.groupby('Setter Name').size().sort_values(ascending=False)
    fig_closes_setter = px.bar(
        closes_by_setter,
        x=closes_by_setter.index,
        y=closes_by_setter.values,
        orientation="v",
        title="<b>Closes by Setter</b>",
        color_discrete_sequence=["#2fddff"] * len(closes_by_setter),
        labels={"y": "Number of Closes"}
    )
    fig_closes_setter.update_layout(
        xaxis_title=None,
        title_x=0.5
    )


    # Closes by Disp Bar
    closes_by_disp = total_happened_df.groupby('Closer Disposition').size().sort_values(ascending=True)
    fig_closes_disp = px.bar(
        closes_by_disp,
        y=closes_by_disp.index,
        x=closes_by_disp.values,
        orientation="h",
        title="<b>Call Disposition</b>",
        color_discrete_sequence=["#2fddff"] * len(closes_by_disp),
        labels={"x": "Number of Appts","y": "Call Disposition"}
    )
    fig_closes_disp.update_layout(
        title_x=0.5
    )

    # Closes by State Bar
    closes_by_state = closes_df.groupby('State').size().sort_values(ascending=True)
    fig_closes_by_state = px.bar(
        closes_by_state,
        y=closes_by_state.index,
        x=closes_by_state.values,
        orientation="h",
        title="<b>Closes by State</b>",
        color_discrete_sequence=["#2fddff"] * len(closes_by_state),
        labels = {"x": "Number of Closes", "y": "State"}

    )
    fig_closes_by_state.update_layout(
        title_x=0.5
    )

    left_col, right_col = st.columns(2)
    left_col.plotly_chart(fig_closes_closer, use_container_width=True)
    right_col.plotly_chart(fig_closes_setter, use_container_width=True)
    left_col.plotly_chart(fig_closes_disp, use_container_width=True)
    right_col.plotly_chart(fig_closes_by_state, use_container_width=True)


    st.markdown("---")
    st.header("Time of Day Charts")
    st.markdown("---")
    left_col, right_col = st.columns(2)

    time_set_s = df.groupby('Set Time').size().reindex(time_blocks, fill_value=0)
    time_close_c = closes_df.groupby('Close Time').size().reindex(time_blocks, fill_value=0)
    #time_set_close = closes_df.groupby('Set Time').size()
    time_noSit_c = noSits_df.groupby('Set Time').size().reindex(time_blocks, fill_value=0)
    time_appts_c = total_happened_df.groupby('Close Time').size().reindex(time_blocks, fill_value=0)


    fig_time_set_s = px.bar(
        x=[t.strftime("%H:%M") for t in time_set_s.index],
        y=time_set_s.values,
        title="<b>Sets by Time of Day</b>",
        color_discrete_sequence=["#2fddff"] * len(time_set_s),
        labels={"y": "Number of Sets", "x": "Time of Day"}
    )
    fig_time_set_s.update_layout(
        xaxis_title=None,
        title_x=0.5
    )

    """
    fig_time_close_c = px.bar(
        x=[t.strftime("%H:%M") for t in time_close_c.index],
        y=time_close_c.values,
        title="<b>Closes by Time of Day</b>",
        color_discrete_sequence=["#2fddff"] * len(time_close_c),
        labels={"y": "Number of Closes", "x": "Time of Day"}
    )
    fig_time_close_c.update_layout(
        xaxis_title=None,
        title_x=0.5
    )
    """

    # Closer time close appts no sit chart
    fig_time_appt_noSit = plot_ns_c_appt(time_appts_c,time_noSit_c,time_close_c)

    fig_time_noSit_c = px.bar(
        time_noSit_c,
        x=[t.strftime("%H:%M") for t in time_noSit_c.index],
        y=time_noSit_c.values,
        orientation="v",
        title="<b>No Sits by Time of Day</b>",
        color_discrete_sequence=["#2fddff"] * len(time_noSit_c),
        labels={"y": "Number of No Sits"}
    )
    fig_time_noSit_c.update_layout(
        xaxis_title=None,
        title_x=0.5
    )

    """
    fig_time_set_close = px.bar(
        time_set_close,
        x=time_set_close.index,
        y=time_set_close.values,
        orientation="v",
        title="<b>Closes by Time Appt Was Set</b>",
        color_discrete_sequence=["#2fddff"] * len(time_set_close),
        labels={"y": "Number of Closes"}
    )
    fig_time_set_close.update_layout(
        xaxis_title=None,
        title_x=0.5
    )
    """

    """
    fig_time_appts_c = px.bar(
        time_appts_c,
        x=[t.strftime("%H:%M") for t in time_appts_c.index],
        y=time_appts_c.values,
        orientation="v",
        title="<b>Time of Closer Appts</b>",
        color_discrete_sequence=["#2fddff"] * len(time_appts_c),
        labels={"y": "Number of Appts"}
    )
    fig_time_appts_c.update_layout(
        xaxis_title=None,
        title_x=0.5
    )
    """


    #left_col.plotly_chart(fig_time_set_s, use_container_width=True)
    st.plotly_chart(fig_time_set_s, use_container_width=True)
    #right_col.plotly_chart(fig_time_noSit_c, use_container_width=True)
    #with left_col:
    st.pyplot(fig_time_appt_noSit)
    #left_col.plotly_chart(fig_time_close_c, use_container_width=True)
    #right_col.plotly_chart(fig_time_close_c, use_container_width=True)
    #right_col.plotly_chart(fig_time_appts_c, use_container_width=True)
    #right_col.plotly_chart(fig_time_set_close, use_container_width=True)



def c_dashboard(df):
    closer_filt = st.sidebar.selectbox('Closer', config.closers)
    closer_name = closer_filt if closer_filt else "Select a Closer"
    if closer_filt:
        df = df[df['Closer Name'].isin([closer_filt])]

    st.markdown(
        f"""
        <h1 style="text-align: center;">{closer_name}</h1>
        <br>
        """,
        unsafe_allow_html=True
    )

    #KPI's
    total_sets = len(df)
    total_sets_happened = (df['Closer Disposition'] != '').sum()
    total_happened_df = df[df['Closer Disposition'] != '']
    total_nosits = (df['Closer Disposition'] == 'No Sit').sum()
    total_sits = total_sets_happened - total_nosits # maybe - reschedules
    total_close = (df['Closer Disposition'] == 'Closed').sum()

    left_col, middle_col, right_col = st.columns(3)

    with left_col:
        st.markdown(f"""
        <div style="background-color: #ECFCFF; border-radius: 15px; padding: 20px; text-align: center;">
            <h3 style="margin: 0; padding: 0;">Total Appointments:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_sets}</h1>
        </div>
        """, unsafe_allow_html=True)

    with middle_col:
        st.markdown(f"""
        <div style="background-color: #E6F4F1; border-radius: 15px; padding: 20px; text-align: center;">
            <h3 style="margin: 0; padding: 0;">Total Sits:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_sits}</h1>
            <h3 style="margin: 0; padding: 0; margin-top: 15px;">Sit rate:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{((total_sits / total_sets_happened) * 100).astype(int)}%</h1>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown(f"""
        <div style="background-color: #95B0B7; border-radius: 15px; padding: 20px; text-align: center;">
            <h3 style="margin: 0; padding: 0;">Total Closes:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_close}</h1>
            <h3 style="margin: 0; padding: 0; margin-top: 15px;">Close rate:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{((total_close / total_sets_happened) * 100).astype(int)}%</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- BAR CHARTS ---
    closes_df = df[df['Closer Disposition'] == 'Closed']
    noSits_df = df[df['Closer Disposition'] == 'No Sit']

    if closes_df.empty:
        st.markdown(
            """
            <h1 style="text-align: center; color: red;">
                🔔 You need at least one Close in the current date range for the charts to show up. 🔔 
            </h1>
            """,
            unsafe_allow_html=True
        )

    # Closes by Setter Bar
    closes_by_setter = closes_df.groupby('Setter Name').size().sort_values(ascending=False)
    fig_closes_setter = px.bar(title="<b>Closes by Setter</b>")
    if not closes_by_setter.empty:
        fig_closes_setter = px.bar(
            closes_by_setter,
            x=closes_by_setter.index,
            y=closes_by_setter.values,
            orientation="v",
            title=f"<b>{closer_name}'s Closes by Closer</b>" if closer_name != 'Select a Closer' else "<b>Closes by Setter</b>",
            color_discrete_sequence=["#2fddff"] * len(closes_by_setter),
            labels={"y": "Number of Closes"}
        )
        fig_closes_setter.update_layout(
            xaxis_title=None,
            title_xanchor='center',  # Anchor the title to its center
            title_x=0.5
        )

    # Closes by Disp Bar
    closes_by_disp = total_happened_df.groupby('Closer Disposition').size().sort_values(ascending=True)
    fig_closes_disp = px.bar(title="<b>Call Disposition</b>")
    if not closes_by_disp.empty:
        fig_closes_disp = px.bar(
            closes_by_disp,
            y=closes_by_disp.index,
            x=closes_by_disp.values,
            orientation="h",
            title=f"<b>{closer_name}'s Call Disposition</b>" if closer_name != 'Select a Closer' else "<b>Call Disposition</b>",
            color_discrete_sequence=["#2fddff"] * len(closes_by_disp),
            labels={"x": "Number of Appts","y": "Call Disposition"}
        )
        fig_closes_disp.update_layout(
            title_xanchor='center',  # Anchor the title to its center
            title_x=0.5
        )

    # Closes by Time Bar
    closes_df.set_index('Close Date', inplace=True)
    closes_by_week = closes_df.resample('W').size()

    fig_closes_by_time = px.bar(title="<b>Closes over Time (Weekly)</b>")
    if not closes_by_week.empty:
        fig_closes_by_time = px.line(
            x=closes_by_week.index,
            y=closes_by_week.values,
            title=f"<b>{closer_name}'s Closes over Time (Weekly)</b>" if closer_name != 'Select a Closer' else "<b>Closes over Time (Weekly)</b>",
            labels={"x": "Date", "y": "Number of Closes"}
        )
        fig_closes_by_time.update_layout(title_xanchor='center',title_x=0.5, xaxis_title=None)
        fig_closes_by_time.update_traces(line=dict(color="#2fddff", width=3))

        # Display the note and the graph
        if len(closes_by_week) < 3:
            fig_closes_by_time.add_annotation(
                x=0.5,
                y=0.5,
                text="🔔 For some reason, the Closes over Time graph requires at least 3 closes to be recorded. 🔔",
                showarrow=False,
                font=dict(size=12, color="red"),
                align="center",
                xref="paper",
                yref="paper"
            )

    # Closes by State Bar
    closes_by_state = closes_df.groupby('State').size().sort_values(ascending=True)
    fig_closes_by_state = px.bar(title="<b>Closes by State</b>")
    if not closes_by_state.empty:
        fig_closes_by_state = px.bar(
            closes_by_state,
            y=closes_by_state.index,
            x=closes_by_state.values,
            orientation="h",
            title=f"<b>{closer_name}'s Closes by State</b>" if closer_name != 'Select a Closer' else "<b>Closes by State</b>",
            color_discrete_sequence=["#2fddff"] * len(closes_by_state),
            labels = {"x": "Number of Closes", "y": "State"}

        )
        fig_closes_by_state.update_layout(
            title_xanchor='center',  # Anchor the title to its center
            title_x=0.5
        )

    left_col, right_col = st.columns(2)
    left_col.plotly_chart(fig_closes_setter, use_container_width=True)
    left_col.plotly_chart(fig_closes_disp, use_container_width=True)
    right_col.plotly_chart(fig_closes_by_time, use_container_width=True)
    right_col.plotly_chart(fig_closes_by_state, use_container_width=True)

    #--- Time of day ---
    st.markdown("---")
    st.header(f"Time of Day Charts for {closer_name}" if closer_name != "Select a Closer" else "Time of Day Charts rfor Closers")
    st.markdown("---")
    left_col, right_col = st.columns(2)


    time_set_s = df.groupby('Set Time').size().reindex(time_blocks, fill_value=0)
    time_close_c = closes_df.groupby('Close Time').size().reindex(time_blocks, fill_value=0)
    #time_set_close = closes_df.groupby('Set Time').size()
    time_noSit_c = noSits_df.groupby('Close Time').size().reindex(time_blocks, fill_value=0)
    time_appts_c = total_happened_df.groupby('Close Time').size().reindex(time_blocks, fill_value=0)


    # Closer time close appts no sit chart
    fig_time_appt_noSit = plot_ns_c_appt(time_appts_c,time_noSit_c,time_close_c)

    """
    fig_time_set_s = px.bar(title="<b>Appts by Time of Day</b>")
    if not time_set_s.empty:
        fig_time_set_s = px.bar(
            time_set_s,
            x=time_set_s.index,
            y=time_set_s.values,
            orientation="v",
            title="<b>Appts by Time of Day</b>",
            color_discrete_sequence=["#2fddff"] * len(time_set_s),
            labels={"y": "Number of Sets"}
        )
        fig_time_set_s.update_layout(
            xaxis_title=None,
            title_x=0.5
        )
    """

    """
    fig_time_close_c = px.bar(title="<b>Closes by Time of Day</b>")
    if not time_close_c.empty:
        fig_time_close_c = px.bar(
            time_close_c,
            x=time_close_c.index,
            y=time_close_c.values,
            orientation="v",
            title="<b>Closes by Time of Day</b>",
            color_discrete_sequence=["#2fddff"] * len(time_close_c),
            labels={"y": "Number of Closes"}
        )
        fig_time_close_c.update_layout(
            xaxis_title=None,
            title_x=0.5
        )
    """


    """
    fig_time_noSit_c = px.bar(title="<b>No Sits by Time of Day</b>")
    if not time_noSit_c.empty:
        fig_time_noSit_c = px.bar(
            time_noSit_c,
            x=time_noSit_c.index,
            y=time_noSit_c.values,
            orientation="v",
            title="<b>No Sits by Time of Day</b>",
            color_discrete_sequence=["#2fddff"] * len(time_noSit_c),
            labels={"y": "Number of No Sits"}
        )
        fig_time_noSit_c.update_layout(
            xaxis_title=None,
            title_x=0.5
        )
    """

    st.pyplot(fig_time_appt_noSit)
    #left_col.plotly_chart(fig_time_set_s, use_container_width=True)
    #right_col.plotly_chart(fig_time_noSit_c, use_container_width=True)
    #left_col.plotly_chart(fig_time_close_c, use_container_width=True)
    #right_col.plotly_chart(fig_time_appts_c, use_container_width=True)
    #right_col.plotly_chart(fig_time_set_close, use_container_width=True)

def s_dashboard(df):
    setter_filt = st.sidebar.selectbox('Setter', config.setters)
    setter_name = setter_filt if setter_filt else "Select a Setter"
    if setter_filt:
        df = df[df['Setter Name'].isin([setter_filt])]

    st.markdown(
        f"""
        <h1 style="text-align: center;">{setter_name}</h1>
        <br>
        """,
        unsafe_allow_html=True
    )


    #KPI's
    total_sets = len(df)
    total_sets_happened = (df['Closer Disposition'] != '').sum()
    total_happened_df = df[df['Closer Disposition'] != '']
    total_nosits = (df['Closer Disposition'] == 'No Sit').sum()
    total_sits = total_sets_happened - total_nosits # maybe - reschedules
    total_close = (df['Closer Disposition'] == 'Closed').sum()

    left_col, middle_col, right_col = st.columns(3)

    with left_col:
        st.markdown(f"""
        <div style="background-color: #ECFCFF; border-radius: 15px; padding: 20px; text-align: center;">
            <h3 style="margin: 0; padding: 0;">Total Sets:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_sets}</h1>
            <h3 style="margin: 0; padding: 0; margin-top: 15px;">Recorded Appts:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_sets_happened}</h1>
        </div>
        """, unsafe_allow_html=True)

    with middle_col:
        st.markdown(f"""
        <div style="background-color: #E6F4F1; border-radius: 15px; padding: 20px; text-align: center;">
            <h3 style="margin: 0; padding: 0;">Total Sits:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_sits}</h1>
            <h3 style="margin: 0; padding: 0; margin-top: 15px;">Sit rate:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{((total_sits / total_sets_happened) * 100).astype(int)}%</h1>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown(f"""
        <div style="background-color: #95B0B7; border-radius: 15px; padding: 20px; text-align: center;">
            <h3 style="margin: 0; padding: 0;">Total Closes:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{total_close}</h1>
            <h3 style="margin: 0; padding: 0; margin-top: 15px;">Close rate:</h3>
            <h1 style="font-size: 3em; margin: 0; padding: 0;">{((total_close / total_sets_happened) * 100).astype(int)}%</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- BAR CHARTS ---
    closes_df = df[df['Closer Disposition'] == 'Closed']
    noSits_df = df[df['Closer Disposition'] == 'No Sit']

    if closes_df.empty:
        st.markdown(
            """
            <h1 style="text-align: center; color: red;">
                🔔 You need at least one Close in the current date range for the charts to show up. 🔔 
            </h1>
            """,
            unsafe_allow_html=True
        )



    # Closes by Close Bar
    closes_by_closer = closes_df.groupby('Closer Name').size().sort_values(ascending=False)
    fig_closes_closer = px.bar(title="<b>Closes by Closer</b>")
    if not closes_by_closer.empty:
        fig_closes_closer = px.bar(
            closes_by_closer,
            x=closes_by_closer.index,
            y=closes_by_closer.values,
            orientation="v",
            title=f"<b>{setter_name}'s Closes by Closer</b>" if setter_name != 'Select a Setter' else "<b>Closes by Closer</b>",
            color_discrete_sequence=["#2fddff"] * len(closes_by_closer),
            labels={"y": "Number of Closes"}
        )
        fig_closes_closer.update_layout(
            xaxis_title=None,
            title_xanchor='center',  # Anchor the title to its center
            title_x=0.5
        )

    # Closes by Disp Bar
    closes_by_disp = total_happened_df.groupby('Closer Disposition').size().sort_values(ascending=True)
    fig_closes_disp = px.bar(title="<b>Call Disposition</b>")
    if not closes_by_disp.empty:
        fig_closes_disp = px.bar(
            closes_by_disp,
            y=closes_by_disp.index,
            x=closes_by_disp.values,
            orientation="h",
            title=f"<b>{setter_name}'s Call Disposition</b>" if setter_name != 'Select a Setter' else "<b>Call Disposition</b>",
            color_discrete_sequence=["#2fddff"] * len(closes_by_disp),
            labels={"x": "Number of Appts","y": "Call Disposition"}
        )
        fig_closes_disp.update_layout(
            title_xanchor='center',  # Anchor the title to its center
            title_x=0.5
        )

    # Closes by Time Bar
    closes_df.set_index('Close Date', inplace=True)
    closes_by_week = closes_df.resample('W').size()

    fig_closes_by_time = px.bar(title="<b>Closes over Time (Weekly)</b>")
    if not closes_by_week.empty:
        fig_closes_by_time = px.line(
            x=closes_by_week.index,
            y=closes_by_week.values,
            title=f"<b>{setter_name}'s Closes over Time (Weekly)</b>" if setter_name != 'Select a Setter' else "<b>Closes over Time (Weekly)</b>",
            labels={"x": "Date", "y": "Number of Closes"}
        )
        fig_closes_by_time.update_layout(title_xanchor='center', title_x=0.5, xaxis_title=None)
        fig_closes_by_time.update_traces(line=dict(color="#2fddff", width=3))

        # Display the note and the graph
        if len(closes_by_week) < 3:
            fig_closes_by_time.add_annotation(
                x=0.5,
                y=0.5,
                text="🔔 For some reason, the Closes over Time graph requires at least 3 closes to be recorded. 🔔",
                showarrow=False,
                font=dict(size=12, color="red"),
                align="center",
                xref="paper",
                yref="paper"
            )

    # Closes by State Bar
    closes_by_state = closes_df.groupby('State').size().sort_values(ascending=True)
    fig_closes_by_state = px.bar(title="<b>Closes by State</b>")
    if not closes_by_state.empty:
        fig_closes_by_state = px.bar(
            closes_by_state,
            y=closes_by_state.index,
            x=closes_by_state.values,
            orientation="h",
            title=f"<b>{setter_name}'s Closes by State</b>" if setter_name != 'Select a Setter' else "<b>Closes by State</b>",
            color_discrete_sequence=["#2fddff"] * len(closes_by_state),
            labels = {"x": "Number of Closes", "y": "State"}

        )
        fig_closes_by_state.update_layout(
            title_xanchor='center',  # Anchor the title to its center
            title_x=0.5
        )

    left_col, right_col = st.columns(2)
    left_col.plotly_chart(fig_closes_closer, use_container_width=True)
    left_col.plotly_chart(fig_closes_disp, use_container_width=True)
    right_col.plotly_chart(fig_closes_by_time, use_container_width=True)
    right_col.plotly_chart(fig_closes_by_state, use_container_width=True)


    st.markdown("---")
    st.header(f"Time of Day Charts for {setter_name}" if setter_name != "Select a Setter" else "Time of Day Charts for Setters")
    st.markdown("---")
    left_col, right_col = st.columns(2)


    time_set_s = df.groupby('Set Time').size().reindex(time_blocks, fill_value=0)
    time_close_c = closes_df.groupby('Close Time').size().reindex(time_blocks, fill_value=0)
    #time_set_close = closes_df.groupby('Set Time').size()
    time_noSit_c = noSits_df.groupby('Close Time').size().reindex(time_blocks, fill_value=0)
    time_appts_c = total_happened_df.groupby('Close Time').size().reindex(time_blocks, fill_value=0)

    fig_time_set_s = px.bar(
        x=[t.strftime("%H:%M") for t in time_set_s.index],
        y=time_set_s.values,
        title=f"<b>{setter_name}'s Sets by Time of Day</b>" if setter_name != 'Select a Setter' else "<b>Sets by Time of Day</b>",
        color_discrete_sequence=["#2fddff"] * len(time_set_s),
        labels={"y": "Number of Sets", "x": "Time of Day"}
    )
    fig_time_set_s.update_layout(
        xaxis_title=None,
        title_xanchor='center',  # Anchor the title to its center
        title_x=0.5
    )

    """
    fig_time_close_c = px.bar(
        x=[t.strftime("%H:%M") for t in time_close_c.index],
        y=time_close_c.values,
        title="<b>Closes by Time of Day</b>",
        color_discrete_sequence=["#2fddff"] * len(time_close_c),
        labels={"y": "Number of Closes", "x": "Time of Day"}
    )
    fig_time_close_c.update_layout(
        xaxis_title=None,
        title_x=0.5
    )
    """

    # Closer time close appts no sit chart
    fig_time_appt_noSit = plot_ns_c_appt(time_appts_c, time_noSit_c, time_close_c)

    fig_time_noSit_c = px.bar(
        time_noSit_c,
        x=[t.strftime("%H:%M") for t in time_noSit_c.index],
        y=time_noSit_c.values,
        orientation="v",
        title="<b>No Sits by Time of Day</b>",
        color_discrete_sequence=["#2fddff"] * len(time_noSit_c),
        labels={"y": "Number of No Sits"}
    )
    fig_time_noSit_c.update_layout(
        xaxis_title=None,
        title_xanchor='center',  # Anchor the title to its center
        title_x=0.5
    )

    """
    fig_time_set_close = px.bar(
        time_set_close,
        x=time_set_close.index,
        y=time_set_close.values,
        orientation="v",
        title="<b>Closes by Time Appt Was Set</b>",
        color_discrete_sequence=["#2fddff"] * len(time_set_close),
        labels={"y": "Number of Closes"}
    )
    fig_time_set_close.update_layout(
        xaxis_title=None,
        title_x=0.5
    )
    """

    """
    fig_time_appts_c = px.bar(
        time_appts_c,
        x=[t.strftime("%H:%M") for t in time_appts_c.index],
        y=time_appts_c.values,
        orientation="v",
        title="<b>Time of Closer Appts</b>",
        color_discrete_sequence=["#2fddff"] * len(time_appts_c),
        labels={"y": "Number of Appts"}
    )
    fig_time_appts_c.update_layout(
        xaxis_title=None,
        title_x=0.5
    )
    """

    # left_col.plotly_chart(fig_time_set_s, use_container_width=True)
    st.plotly_chart(fig_time_set_s, use_container_width=True)
    # right_col.plotly_chart(fig_time_noSit_c, use_container_width=True)
    # with left_col:
    st.pyplot(fig_time_appt_noSit)
    # left_col.plotly_chart(fig_time_close_c, use_container_width=True)
    # right_col.plotly_chart(fig_time_close_c, use_container_width=True)
    # right_col.plotly_chart(fig_time_appts_c, use_container_width=True)
    # right_col.plotly_chart(fig_time_set_close, use_container_width=True)

def d_dashboard(df, month_year_filt):
    #df = pd.DataFrame(sheet.get_all_records())
    df_call_filt = df.copy()  # should be this if no other filters are applied

    df_call_filt = month_year_col(df_call_filt)

    # --- SIDEBAR ---
    st.sidebar.header("Please Filter Here:")
    #month_year_filt = st.sidebar.multiselect('Date', options=df_call_filt["Month_Year"].unique())
    call_disp_filt = st.sidebar.multiselect('Call Dispositions', config.dispositions)
    states_filt = st.sidebar.multiselect('States', config.states)
    setter_filt = st.sidebar.multiselect('Setter', config.setters)
    closer_filt = st.sidebar.multiselect('Closer', config.closers)

    # Connecting filters to data

    state_counts_og = df.groupby('State').size().sort_values(ascending=False)
    if month_year_filt:
        df_call_filt = df_call_filt[df_call_filt['Month_Year'].isin(month_year_filt)]
        state_counts_og = df_call_filt.groupby('State').size().sort_values(ascending=False)
    if setter_filt:
        df_call_filt = df_call_filt[df_call_filt['Setter Name'].isin(setter_filt)]
        state_counts_og = df_call_filt.groupby('State').size().sort_values(ascending=False)
    if closer_filt:
        df_call_filt = df_call_filt[df_call_filt['Closer Name'].isin(closer_filt)]
        state_counts_og = df_call_filt.groupby('State').size().sort_values(ascending=False)
    if states_filt:
        df_call_filt = df_call_filt[df_call_filt['State'].isin(states_filt)]
        state_counts_og = df_call_filt.groupby('State').size().sort_values(ascending=False)
    if call_disp_filt:
        df_call_filt = df_call_filt[df_call_filt['Closer Disposition'].isin(call_disp_filt)]

    # --- Total appointments per state ---
    state_counts_filt = df_call_filt.groupby('State').size().sort_values(ascending=False)
    # Bar chart to show appointments per state
    y_pos = np.arange(len(state_counts_filt))
    plt.figure(figsize=(12, 10))
    plt.bar(y_pos, state_counts_filt.values, color='#00a7e1')
    plt.xticks(y_pos, state_counts_filt.index, rotation=45, fontsize=12)  # Set x-ticks
    plt.xlabel('State', fontsize=14)
    plt.ylabel('Total Appointments', fontsize=14)

    if call_disp_filt:
        title = f'Total {call_disp_filt} Appointments per State'
    else:
        title = 'Total Appointments per State'
    plt.title(title)

    plt.tight_layout()
    st.pyplot(plt)
    plt.close()  # Close the figure to prevent overlapping

    disp_percent(state_counts_og, state_counts_filt, call_disp_filt)

    #  --- Bar chart to show different disps ---
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
    plt.close()  # Close the figure to prevent overlapping

    #  --- Setter bar chart ---
    if not call_disp_filt:
        st.subheader("Total Appointments by Setter")
    else:
        st.subheader(f"Total Appointments and {call_disp_filt} by Setter")
    setter_counts = df_call_filt['Setter Name'].value_counts().reset_index()
    setter_counts.columns = ['Setter Name', 'Total Appointments']
    y_pos = np.arange(len(setter_counts))
    plt.figure(figsize=(12, 8))
    plt.bar(y_pos, setter_counts['Total Appointments'], color='#00a7e1')
    plt.xticks(y_pos, setter_counts['Setter Name'], rotation=45, fontsize=12)  # Set x-ticks to setters
    plt.xlabel('Setter Name', fontsize=14)
    plt.ylabel('Total Appointments', fontsize=14)
    plt.title('Total Appointments by Setter', fontsize=16)
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()

    #  --- Closer Bar chart ---
    if not call_disp_filt:
        st.subheader("Total Appointments by Closer")
    else:
        st.subheader(f"Total Appointments and {call_disp_filt} by Closer")
    closer_counts = df_call_filt['Closer Name'].value_counts().reset_index()
    closer_counts.columns = ['Closer Name', 'Total Appointments']
    y_pos = np.arange(len(closer_counts))
    plt.figure(figsize=(12, 8))
    plt.bar(y_pos, closer_counts['Total Appointments'], color='#00a7e1')
    plt.xticks(y_pos, closer_counts['Closer Name'], rotation=45, fontsize=12)  # Set x-ticks to setters
    plt.xlabel('Closer Name', fontsize=14)
    plt.ylabel('Total Appointments', fontsize=14)
    plt.title('Total Appointments by Closer', fontsize=16)
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()

def plot_ns_c_appt(time_appts_c,time_noSit_c,time_close_c):
    # Combined Appts and no sit chart
    percentage_no_sit = (time_noSit_c / time_appts_c) * 100
    percentage_no_sit = percentage_no_sit.fillna(0)  # Handle division by zero

    percentage_closed = (time_close_c / time_appts_c) * 100
    percentage_closed = percentage_closed.fillna(0)  # Handle division by zero

    fig_time_appt_noSit, ax1 = plt.subplots(figsize=(16, 8))
    fig_time_appt_noSit.patch.set_alpha(0.0)
    ax1.set_facecolor('none')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    # Bar chart for number of appointments
    ax1.bar(
        [t.strftime("%H:%M") for t in time_appts_c.index],
        time_appts_c.values,
        color="#2fddff",
        label="Number of Appts"
    )
    ax1.set_ylabel("Number of Appts", fontsize = 16)
    ax1.tick_params(axis='x', labelsize=14)  # Set font size for x-axis labels

    # Secondary y-axis for percentage of no sits
    ax2 = ax1.twinx()
    ax2.plot(
        [t.strftime("%H:%M") for t in percentage_no_sit.index],
        percentage_no_sit.values,
        color="#ff6347",
        marker='o',
        label="Percentage of No Sits"
    )
    ax2.set_ylabel("Percentage of No Sits", fontsize = 16)
    ax2.set_ylim(0, 100)  # Set limits for percentage

    ax2.plot(
        [t.strftime("%H:%M") for t in percentage_closed.index],
        percentage_closed.values,
        color="#4682b4",
        marker='s',
        linestyle='--',
        label="Percentage of Closed"
    )
    ax2.set_ylabel("Percentage", fontsize=16)
    ax2.set_ylim(0, 100)  # Set limits for percentage

    plt.title("Time of Closer Appts with Percentage of No Sits and Closed", fontsize=18, weight='bold', pad=50)
    fig_time_appt_noSit.tight_layout()
    #plt.show()
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    return  fig_time_appt_noSit
def generate_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def disp_percent(counts_og, counts_filt, disp_filt):
    df = pd.DataFrame()
    df['Appointments'] = counts_og
    total_appointments = counts_og.sum()

    if disp_filt:
        st.subheader(f'Total {disp_filt} for each State')
        df[f'{disp_filt} Deals'] = counts_filt
        percent = (counts_filt / counts_og * 100).fillna(0).astype(int).astype(str) + '%'
        df['Percent'] = percent
        #Total Row
        total_filtered_deals = counts_filt.sum()
        total_percent = (total_filtered_deals / total_appointments * 100).astype(int).astype(str) + '%'
        total_row = {
            'Appointments': total_appointments,
            f'{disp_filt} Deals': total_filtered_deals,
            'Percent': total_percent
        }
    else:
        st.subheader(f'Total Appts for each State')
        total_row = {
            'Appointments': total_appointments,
        }

    df = df.append(pd.DataFrame(total_row, index=['Total']))
    st.write(df)
def month_year_col(df):
    # Convert the 'Set Date' and 'Close Date' columns to datetime
    df['Set Date'] = pd.to_datetime(df['Set Date'], errors='coerce')
    df['Close Date'] = pd.to_datetime(df['Close Date'], errors='coerce')

    # Create a new column 'Actual Date' that uses 'Close Date' or 'Set Date' as a fallback
    df['Actual Date'] = df['Close Date'].combine_first(df['Set Date'])

    # Drop rows with NaT in 'Actual Date'
    df = df.dropna(subset=['Actual Date'])

    # Extract month and year for filtering and formatting
    df['Month_Year'] = df['Actual Date'].dt.strftime('%B %Y')

    return df
