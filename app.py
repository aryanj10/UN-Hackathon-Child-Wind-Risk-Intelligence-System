# app.py

import streamlit as st
import geopandas as gpd
import numpy as np
from rasterstats import zonal_stats

from config.settings import AOI_PATH, ADMIN_PATH, CHILD_TIF, U_TIF, V_TIF
from data.downloader import download_latest_forecast
from data.validator import check_required_files, check_cds_config
from logic.wind_handler import ERA5WindHandler
from logic.exposure import compute_child_exposure
from ui.map_display import render_risk_map
from ui.sidebar import render_sidebar
from utils.cleanup import cleanup_files

# --- Streamlit Page Setup --- #
st.set_page_config(page_title="CW-RIS: Child Wind Risk Viewer", layout="wide")
st.title("Child-Centric Wind Risk Intelligence System")
st.markdown("""
This tool fetches recent ERA5 wind data from Copernicus Climate Data Store and overlays it with child vulnerability data to assess wind exposure risks.
""")

# --- Check System Status --- #
st.subheader("System Status")

missing = check_required_files()

if missing:
    st.error(f"Missing required files: {', '.join(missing)}")
    st.info("Please place the required files in the project assets directory.")
else:
    st.success("✅ All required data files are present.")

cds_ok, cds_msg = check_cds_config()
if cds_ok:
    st.success(f"✅ {cds_msg}")
else:
    st.error(f"❌ {cds_msg}")

# --- Main Analysis Button --- #
st.subheader("Wind Risk Analysis")

if st.button("Get Latest Wind + Vulnerability Data", disabled=(not cds_ok or bool(missing))):
    with st.spinner("Downloading ERA5 wind data and computing child exposure risk..."):
        success, msg = download_latest_forecast(U_TIF, V_TIF)

        if not success:
            st.error(msg)
        else:
            st.success(msg)

            try:
                # Load boundaries
                admin_gdf = gpd.read_file(ADMIN_PATH).to_crs("EPSG:4326")

                # Process wind and compute exposure
                handler = ERA5WindHandler(U_TIF, V_TIF, AOI_PATH)
                wind_speed, transform, crs = handler.compute_total_wind()
                exposure_tif = compute_child_exposure(wind_speed, transform, crs, CHILD_TIF, handler.aoi_geom)

                # Zonal stats
                zs = zonal_stats(admin_gdf, exposure_tif, stats=["sum"], geojson_out=True, nodata=np.nan)
                risk_gdf = gpd.GeoDataFrame.from_features(zs).rename(columns={"sum": "Child Wind Risk"})

                # Render map
                st.subheader("🗺️ Child Wind Risk Map")
                m, max_risk = render_risk_map(risk_gdf)
                m.to_streamlit(height=600)

                # Stats
                st.subheader("📊 Risk Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Areas Analyzed", len(risk_gdf))
                with col2:
                    st.metric("Maximum Risk Score", f"{max_risk:.2f}" if not np.isnan(max_risk) else "N/A")
                with col3:
                    mean_risk = risk_gdf["Child Wind Risk"].mean()
                    st.metric("Average Risk Score", f"{mean_risk:.2f}" if not np.isnan(mean_risk) else "N/A")

                # Cleanup
                cleanup_files([U_TIF, V_TIF, exposure_tif])

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
else:
    if not cds_ok:
        st.warning("Please fix CDS configuration.")
    elif missing:
        st.warning("Missing required data files.")
    else:
        st.info("Click the button to begin analysis.")

# --- Sidebar --- #
with st.sidebar:
    render_sidebar()
