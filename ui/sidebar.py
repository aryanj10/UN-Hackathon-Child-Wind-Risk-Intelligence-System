import streamlit as st

def render_sidebar():
    st.header("About")
    st.write("""
    **CW-RIS** (Child-Centric Wind Risk Intelligence System) combines:
    - ERA5 reanalysis wind data from Copernicus
    - Child population vulnerability data
    - Administrative boundaries for risk assessment
    
    **Data Sources:**
    - Wind: ERA5 10m wind components
    - Population: Child population density
    - Geography: Administrative level 3 boundaries
    """)
    
    st.header("Requirements")
    st.write("""
    - Valid CDS API account and configuration
    - Required data files in project directory
    - Internet connection for data download
    """)
