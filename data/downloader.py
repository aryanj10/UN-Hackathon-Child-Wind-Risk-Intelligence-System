import cdsapi
import xarray as xr
import os
from datetime import datetime, timedelta

def download_latest_forecast(u_file, v_file, bbox=[26, 88, 20, 92]):
    try:
        safe_date = (datetime.utcnow() - timedelta(days=6)).strftime('%Y-%m-%d')
        year, month, day = safe_date.split('-')
        temp_file = "data/latest_forecast.nc"
        if os.path.exists(temp_file):
            os.remove(temp_file)

        c = cdsapi.Client()
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': ['10m_u_component_of_wind', '10m_v_component_of_wind'],
                'year': year,
                'month': month,
                'day': day,
                'time': '12:00',
                'area': bbox,
                'grid': [0.25, 0.25]
            },
            temp_file
        )

        ds = xr.open_dataset(temp_file)
        ds['u10'].rio.write_crs("EPSG:4326", inplace=True)
        ds['v10'].rio.write_crs("EPSG:4326", inplace=True)
        ds['u10'].rio.to_raster(u_file)
        ds['v10'].rio.to_raster(v_file)
        ds.close()
        os.remove(temp_file)

        return True, f"Successfully downloaded wind data for {safe_date}"

    except Exception as e:
        return False, f"Failed to download ERA5 data: {str(e)}"
