import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.warp import reproject, Resampling
import tempfile

def compute_child_exposure(wind_speed, transform, crs, child_tif, aoi_geom):
    if crs is None:
        crs = rasterio.crs.CRS.from_epsg(4326)
    elif not isinstance(crs, rasterio.crs.CRS):
        crs = rasterio.crs.CRS.from_user_input(crs)

    with rasterio.open(child_tif) as child_src:
        clipped, child_transform = mask(child_src, aoi_geom, crop=True)
        child_data = clipped[0]
        child_data = np.where(child_data == child_src.nodata, np.nan, child_data)

        dst_height, dst_width = wind_speed.shape
        dst_transform = transform

        reprojected_child = np.empty((dst_height, dst_width), dtype=np.float32)

        reproject(
            source=child_data,
            destination=reprojected_child,
            src_transform=child_transform,
            src_crs=child_src.crs,
            dst_transform=dst_transform,
            dst_crs=crs,
            resampling=Resampling.nearest
        )

    valid_mask = (~np.isnan(wind_speed)) & (~np.isnan(reprojected_child))
    exposure = np.where(valid_mask, wind_speed * reprojected_child, np.nan)

    tmp_file = tempfile.NamedTemporaryFile(suffix=".tif", delete=False).name
    with rasterio.open(
        tmp_file, 'w', driver='GTiff',
        height=exposure.shape[0], width=exposure.shape[1],
        count=1, dtype='float32', crs=crs, transform=transform,
        nodata=np.nan
    ) as dst:
        dst.write(exposure, 1)

    return tmp_file