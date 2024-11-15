# This file hosts the main application using streamlit.

import streamlit as st

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



