import osmnx as ox
import geopandas as gpd
import os

def download_osm_layers(place_name="Bangladesh", tags=None):
    if tags is None:
        tags = {
            'amenity': ['hospital', 'school'],
            'highway': True  # True gets all roads
        }

    gdf = ox.geometries_from_place(place_name, tags)

    # Filter layers
    hospitals = gdf[gdf["amenity"] == "hospital"]
    schools = gdf[gdf["amenity"] == "school"]
    roads = gdf[gdf["highway"].notnull()]

    return hospitals, schools, roads

def save_layers_to_assets(hospitals, schools, roads, output_dir="assets"):
    os.makedirs(output_dir, exist_ok=True)
    hospitals.to_file(f"{output_dir}/hospitals.geojson", driver="GeoJSON")
    schools.to_file(f"{output_dir}/schools.geojson", driver="GeoJSON")
    roads.to_file(f"{output_dir}/roads.geojson", driver="GeoJSON")

# Example usage:
hospitals, schools, roads = download_osm_layers("Bangladesh")
save_layers_to_assets(hospitals, schools, roads)
