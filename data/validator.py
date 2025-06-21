import os

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "assets/aoi_bangladesh.geojson",
        "assets/adm3.geojson", 
        "assets/bgd_pop_2025_CN_100m_R2024B_v1.tif"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def check_cds_config():
    """Check if CDS API is properly configured for the new CDS system"""
    cdsapirc_path = os.path.expanduser("~/.cdsapirc")
    if not os.path.exists(cdsapirc_path):
        return False, "CDS API configuration file (.cdsapirc) not found in home directory"
    
    try:
        with open(cdsapirc_path, 'r') as f:
            content = f.read()
            if "url:" not in content or "key:" not in content:
                return False, "CDS API configuration file is missing url or key"
            
            # Check for correct new CDS URL
            if "cds.climate.copernicus.eu/api" not in content:
                if "cds-beta.climate.copernicus.eu" in content:
                    return False, "You're using the old CDS-beta URL. Please update to: https://cds.climate.copernicus.eu/api"
                else:
                    return False, "CDS API URL appears to be incorrect in configuration file"
                    
        return True, "CDS API configuration appears to be correct"
    except Exception as e:
        return False, f"Error reading CDS API configuration: {str(e)}"