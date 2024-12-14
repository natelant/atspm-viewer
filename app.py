# This file hosts the main application using streamlit.

import streamlit as st
from datetime import datetime, timedelta
from api_tmc import fetch_tmc_data
from api_splitmonitor import fetch_splitmonitor_data
from api_splitfail import fetch_splitfail_data



# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Signal Operations',
    page_icon='vertical_traffic_light',  # Direct emoji
    # or
    # page_icon='sport_utility_vehicle',  # Shortcode without colons
)

# Add title and logo
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <img src="https://avenueconsultants.com/wp-content/themes/avenuecustom/webflow/images/a-blue.png" 
             style="width: 100px; margin-left: 20px;">
        <div>
            <h1>ATSPM SigOps Dashboard</h1>
            <p>Interfacing with ATSPM APIs to visualize signal operations data.</p>
        </div>
        
    </div>
    """, 
    unsafe_allow_html=True
)

# Add some vertical space
st.markdown("<br>", unsafe_allow_html=True)

st.header("Instructions")
st.write(
    '''
    1. Input the signal ID(s) you want to visualize.
    2. Input the date range you want to visualize.
    3. Click the button to fetch the data.
    4. View the data in the table and charts.
    '''
)

st.header("Inputs")
# Signal ID input as list separated by commas
signal_ids = st.text_input("Signal IDs (order is important)", "7115, 7116")

# input date range in columns
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=7))
with col2:
    end_date = st.date_input("End Date", value=datetime.now())



# cache data
@st.cache_data
def get_tmc_data(signal_ids, start_date, end_date):
    return fetch_tmc_data(signal_ids, start_date, end_date)

@st.cache_data
def get_splitmonitor_data(signal_ids, start_date, end_date):
    return fetch_splitmonitor_data(signal_ids, start_date, end_date)

@st.cache_data
def get_splitfail_data(signal_ids, start_date, end_date):
    return fetch_splitfail_data(signal_ids, start_date, end_date)

# fetch data
if st.button("Fetch Data"):
    # Convert the comma-separated string to a list of strings
    signal_id_list = [id.strip() for id in signal_ids.split(',')]
    
    if not signal_id_list:
        st.error("Please input signal IDs")
    elif not start_date or not end_date:
        st.error("Please input a start and end date")
    else:
        try:
            st.info("Fetching Turning Movement Counts...")
            st.session_state.tmc_data = get_tmc_data(signal_id_list, start_date, end_date)
            st.info("Fetching Split Monitor...")
            st.session_state.splitmonitor_data = get_splitmonitor_data(signal_id_list, start_date, end_date)
            st.info("Fetching Split Failures...")
            st.session_state.splitfail_data = get_splitfail_data(signal_id_list, start_date, end_date)
            st.success("Data fetched successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# if st.button("Analyze Data"):
#     try:
#         st.subheader("Turning Movement Counts")
#          # generate the bar chart
