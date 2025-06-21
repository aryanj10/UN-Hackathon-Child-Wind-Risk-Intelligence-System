import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
from pathlib import Path
import json
import logging

class ERA5WindHandler:
    def __init__(self, u_file: Path, v_file: Path, aoi_path: Path, logger: logging.Logger = None):
        self.u_file = Path(u_file)
        self.v_file = Path(v_file)
        self.aoi_path = Path(aoi_path)
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.logger.info(f"Loading AOI from {self.aoi_path}")
        self.aoi = gpd.read_file(self.aoi_path).to_crs("EPSG:4326")
        self.aoi_geom = [json.loads(self.aoi.to_json())['features'][0]['geometry']]

    def _load_and_clip(self, tif_path):
        with rasterio.open(tif_path) as src:
            clipped, transform = mask(src, self.aoi_geom, crop=True)
            data = np.where(clipped[0] == src.nodata, np.nan, clipped[0])
        return data, transform, src.crs

    def compute_total_wind(self):
        u_arr, transform, crs = self._load_and_clip(self.u_file)
        v_arr, _, _ = self._load_and_clip(self.v_file)
        wind_speed = np.sqrt(u_arr ** 2 + v_arr ** 2)
        return wind_speed, transform, crs
