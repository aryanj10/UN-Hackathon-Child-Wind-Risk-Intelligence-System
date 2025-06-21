import geopandas as gpd
from shapely.ops import nearest_points

def compute_hospital_access(admin_gdf, hospital_geojson_path):
    hospitals = gpd.read_file(hospital_geojson_path).to_crs("EPSG:4326")
    hospital_points = hospitals.geometry.unary_union

    admin_gdf["Centroid"] = admin_gdf.geometry.centroid
    admin_gdf["Hospital_Dist"] = admin_gdf["Centroid"].apply(
        lambda pt: pt.distance(nearest_points(pt, hospital_points)[1])
    )

    max_dist = admin_gdf["Hospital_Dist"].max()
    admin_gdf["Hospital_Access_Factor"] = 1 - (admin_gdf["Hospital_Dist"] / max_dist)
    return admin_gdf
