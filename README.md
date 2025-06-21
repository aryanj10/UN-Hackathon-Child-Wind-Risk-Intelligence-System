# 🌪️ CW-RIS: Child Wind Risk Intelligence System

**CW-RIS** is a child-centered wind risk analysis app that overlays real-time ECMWF ERA5 wind forecast data with child population exposure (e.g., from WorldPop) to compute and visualize risk zones. This Streamlit app enables faster, data-driven decisions for humanitarian response and preparedness.

---

## 🚀 What This App Does

- ✅ Downloads live 10m wind forecast data (U & V components) from ECMWF ERA5 via CDS API
- ✅ Computes wind speed magnitude from U and V components
- ✅ Clips and reprojects child population raster to match wind data
- ✅ Multiplies wind × population to produce a child wind risk raster
- ✅ Aggregates exposure using zonal statistics (by admin boundaries)
- ✅ Displays an interactive map with high-risk areas highlighted

---

## 🛠️ Features

- 📡 **Live ERA5 Wind Data** via Copernicus CDS API
- 💨 **Wind Magnitude Calculation**: `sqrt(U^2 + V^2)`
- 👶 **Child Exposure Mapping** using population rasters
- 🗺️ **Zonal Risk Statistics** per admin region
- 🖱️ **Interactive Map** with hover tooltips (Leafmap/Folium)
- 🔍 **Auto-Zoom to Highest Risk Zones**

---

## 📁 Project Structure

```protobuf
cw-ris/
├── app.py                         # 🔵 Main Streamlit entrypoint
├── requirements.txt               # 📦 Python dependencies
├── README.md                      # 📘 Project overview

├── config/
│   └── settings.py                # ⚙️ File paths and constants

├── data/
│   ├── downloader.py              # 🌐 ERA5 wind downloader via CDS API
│   └── validator.py              # ✅ File presence & CDS API checks

├── logic/
│   ├── wind_handler.py            # 💨 Wind speed calculation from U/V
│   └── exposure.py                # 👶 Population × wind risk computation

├── ui/
│   ├── map_display.py             # 🗺️ Map rendering with OSM layers
│   └── sidebar.py                 # 📚 Sidebar with instructions

├── utils/
│   └── cleanup.py                 # 🧹 Temp file cleanup utility

├── assets/                        # 🗂️ Static geospatial inputs
│   ├── aoi_bangladesh.geojson     # 🟡 AOI polygon
│   ├── adm3.geojson               # 🟢 Admin boundaries for stats
│   ├── bgd_pop_2025_CN_100m.tif   # 👶 Child population raster

```

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

### 🔑 Setup: CDS API Key

1.  Register at https://cds.climate.copernicus.eu

2.  Go to your CDS API page

3. Save your credentials in a .cdsapirc file or add directly to script:

```python
c = cdsapi.Client(
    url="https://cds.climate.copernicus.eu/api",
    key="your_uid:your_api_key"
)
```

### 📂 Input Files Required

| File                       | Description                        |
| -------------------------- | ---------------------------------- |
| `aoi_bangladesh.geojson`   | Area of interest polygon           |
| `adm3.geojson`             | Admin boundaries for zonal stats   |
| `bgd_pop_2025_CN_100m.tif` | Child population raster (WorldPop) |
---

## ▶️ Run the App

```bash
streamlit run app.py
```
Open in browser at: http://localhost:8501

## 🔄 How It Works

Fetch latest wind forecast (last 5 days)

Compute total wind speed using U and V components

Clip and reproject child population raster to wind CRS

Multiply wind speed × child population to get exposure

Aggregate risk per administrative zone using zonal_stats

Display results on an interactive map

---
## 📊 Example Outputs

- Table ranking admin regions by total child wind risk

- Interactive map:

    - Color-coded risk zones

    - Highlighted highest-risk areas

    - Hover for risk value tooltips

---
## Notes
CRS assumed to be EPSG:4326 across all layers

Ensure netCDF4 or h5netcdf is installed to read ERA5 .nc files

Reprojection and alignment handled via rasterio.reproject()

---

## Future Plans

Add flood and landslide risk layers

Integrate with CCRI-DRM dashboards via Cloud-Optimized GeoTIFF

Add school and health facility access overlays

Modularize handlers for global use (GIGA-compatible)

---