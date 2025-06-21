import geopandas as gpd

def compute_school_density(admin_gdf, school_geojson_path):
    schools = gpd.read_file(school_geojson_path).to_crs("EPSG:4326")
    joined = gpd.sjoin(schools, admin_gdf, predicate='within')
    school_counts = joined.groupby("index_right").size().rename("School_Count")
    admin_gdf["School_Count"] = admin_gdf.index.map(school_counts).fillna(0)
    return admin_gdf
