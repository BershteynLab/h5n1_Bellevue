"""
Helper script to download and prepare data for H5N1 risk mapping.

This script provides functions to download data from common sources.
Note: Some downloads may require manual steps or API keys.
"""

import os
import requests
import pandas as pd
import geopandas as gpd
from pathlib import Path
from typing import Optional


def setup_data_directories():
    """Create data directory structure."""
    dirs = ['data/raw', 'data/processed']
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print("✓ Data directories created")


def download_nyc_zip_boundaries(output_path: str = 'data/raw/nyc_zip_codes.geojson'):
    """
    Download NYC zip code boundaries from NYC Open Data.
    
    Note: This downloads from the NYC Open Data API.
    You may need to manually download from:
    https://data.cityofnewyork.us/Business/Zip-Code-Boundaries/i8iw-xf4u
    """
    url = "https://data.cityofnewyork.us/api/geospatial/i8iw-xf4u?method=export&format=GeoJSON"
    
    print(f"Downloading NYC zip code boundaries...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        # Verify it's valid GeoJSON
        gdf = gpd.read_file(output_path)
        print(f"✓ Downloaded {len(gdf)} zip codes to {output_path}")
        print(f"  Columns: {list(gdf.columns)}")
        
        # Standardize zip code column name
        zip_cols = [col for col in gdf.columns if 'zip' in col.lower() or 'postal' in col.lower()]
        if zip_cols and zip_cols[0] != 'zip_code':
            gdf = gdf.rename(columns={zip_cols[0]: 'zip_code'})
            gdf.to_file(output_path, driver='GeoJSON')
            print(f"  Renamed column to 'zip_code'")
        
        return gdf
    except Exception as e:
        print(f"✗ Error downloading: {e}")
        print(f"  Please manually download from:")
        print(f"  https://data.cityofnewyork.us/Business/Zip-Code-Boundaries/i8iw-xf4u")
        return None


def download_nyc_water_bodies(output_path: str = 'data/raw/nyc_water_bodies.geojson'):
    """
    Download NYC water bodies from NYC Open Data.
    
    Note: You may need to manually download from:
    https://data.cityofnewyork.us/Environment/Hydrography/9ar3-6nj9
    """
    url = "https://data.cityofnewyork.us/api/geospatial/9ar3-6nj9?method=export&format=GeoJSON"
    
    print(f"Downloading NYC water bodies...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        gdf = gpd.read_file(output_path)
        print(f"✓ Downloaded water bodies to {output_path}")
        print(f"  Features: {len(gdf)}")
        return gdf
    except Exception as e:
        print(f"✗ Error downloading: {e}")
        print(f"  Please manually download from:")
        print(f"  https://data.cityofnewyork.us/Environment/Hydrography/9ar3-6nj9")
        return None


def create_sample_population_data(zip_codes: list, output_path: str = 'data/raw/nyc_population_by_zip.csv'):
    """
    Create a template for population data.
    
    This creates a CSV template that you can fill in with real Census data.
    """
    import numpy as np
    
    df = pd.DataFrame({
        'zip_code': zip_codes,
        'population': np.nan  # Fill with real data
    })
    
    df.to_csv(output_path, index=False)
    print(f"✓ Created population template at {output_path}")
    print(f"  Please fill in 'population' column with Census data")
    return df


def validate_zip_code_data(gdf: gpd.GeoDataFrame) -> dict:
    """
    Validate zip code GeoDataFrame.
    
    Returns a dictionary with validation results.
    """
    results = {
        'valid': True,
        'issues': []
    }
    
    # Check for zip_code column
    if 'zip_code' not in gdf.columns:
        zip_cols = [col for col in gdf.columns if 'zip' in col.lower()]
        if zip_cols:
            results['issues'].append(f"Found zip column: {zip_cols[0]} (should rename to 'zip_code')")
        else:
            results['valid'] = False
            results['issues'].append("No zip_code column found")
    
    # Check for geometry
    if not hasattr(gdf, 'geometry') or gdf.geometry.isna().all():
        results['valid'] = False
        results['issues'].append("No valid geometry found")
    
    # Check zip code format
    if 'zip_code' in gdf.columns:
        zip_codes = gdf['zip_code'].astype(str)
        if not zip_codes.str.match(r'^\d{5}$').all():
            results['issues'].append("Some zip codes are not 5-digit format")
    
    # Check for duplicates
    if 'zip_code' in gdf.columns:
        duplicates = gdf['zip_code'].duplicated().sum()
        if duplicates > 0:
            results['issues'].append(f"Found {duplicates} duplicate zip codes")
    
    return results


def main():
    """Main function to set up data directories and download initial data."""
    print("=" * 60)
    print("H5N1 Risk Mapping - Data Download Helper")
    print("=" * 60)
    
    # Setup directories
    setup_data_directories()
    
    # Download zip code boundaries
    print("\n1. Downloading zip code boundaries...")
    zip_gdf = download_nyc_zip_boundaries()
    
    if zip_gdf is not None:
        # Validate
        print("\n2. Validating zip code data...")
        validation = validate_zip_code_data(zip_gdf)
        if validation['valid']:
            print("✓ Zip code data is valid")
        else:
            print("✗ Issues found:")
            for issue in validation['issues']:
                print(f"  - {issue}")
        
        # Create population template
        print("\n3. Creating population data template...")
        zip_codes = zip_gdf['zip_code'].astype(str).tolist() if 'zip_code' in zip_gdf.columns else []
        if zip_codes:
            create_sample_population_data(zip_codes)
    
    # Download water bodies
    print("\n4. Downloading water bodies...")
    download_nyc_water_bodies()
    
    print("\n" + "=" * 60)
    print("Data download complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Fill in population data from Census Bureau")
    print("2. Gather poultry facility data")
    print("3. Add hospital/healthcare data")
    print("4. Run risk calculations with: python src/example_risk_map.py")


if __name__ == '__main__':
    main()

