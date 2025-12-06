"""
Process USGS Poultry Susceptibility Raster for H5N1 Risk Mapping.

This script extracts poultry susceptibility values from the raster
and aggregates them to NYC zip code level.
"""

import rasterio
from rasterio.mask import mask
import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def extract_poultry_values_by_zip(
    raster_path: str,
    zip_gdf: gpd.GeoDataFrame,
    method: str = 'mean'
) -> pd.Series:
    """
    Extract poultry susceptibility values from raster for each zip code.
    
    Parameters
    ----------
    raster_path : str
        Path to the poultry raster file
    zip_gdf : gpd.GeoDataFrame
        GeoDataFrame with zip code boundaries
    method : str
        Aggregation method: 'mean', 'max', 'sum', or 'median'
    
    Returns
    -------
    pd.Series
        Poultry susceptibility values indexed by zip code
    """
    print(f"Loading raster from {raster_path}...")
    
    # Open raster
    with rasterio.open(raster_path) as src:
        print(f"  Raster info:")
        print(f"    Shape: {src.shape}")
        print(f"    CRS: {src.crs}")
        print(f"    Bounds: {src.bounds}")
        print(f"    NoData: {src.nodata}")
        
        # Ensure zip codes are in same CRS as raster
        if zip_gdf.crs != src.crs:
            print(f"  Reprojecting zip codes from {zip_gdf.crs} to {src.crs}...")
            zip_gdf_proj = zip_gdf.to_crs(src.crs)
        else:
            zip_gdf_proj = zip_gdf.copy()
        
        # Extract values for each zip code
        print(f"\nExtracting values for {len(zip_gdf_proj)} zip codes...")
        poultry_values = []
        zip_codes = []
        
        for idx, row in zip_gdf_proj.iterrows():
            zip_code = row['zip_code']
            geometry = row.geometry
            
            try:
                # Mask raster to zip code boundary
                out_image, out_transform = mask(
                    src,
                    [geometry],
                    crop=True,
                    nodata=src.nodata
                )
                
                # Extract valid values (exclude nodata)
                values = out_image[0]
                if src.nodata is not None:
                    valid_values = values[values != src.nodata]
                else:
                    valid_values = values[~np.isnan(values)]
                
                # Aggregate values
                if len(valid_values) > 0:
                    if method == 'mean':
                        value = float(np.mean(valid_values))
                    elif method == 'max':
                        value = float(np.max(valid_values))
                    elif method == 'sum':
                        value = float(np.sum(valid_values))
                    elif method == 'median':
                        value = float(np.median(valid_values))
                    else:
                        value = float(np.mean(valid_values))
                else:
                    value = 0.0  # No data in this zip code
                
                poultry_values.append(value)
                zip_codes.append(zip_code)
                
            except Exception as e:
                print(f"  Warning: Error processing zip {zip_code}: {e}")
                poultry_values.append(0.0)
                zip_codes.append(zip_code)
        
        # Create result series
        result = pd.Series(poultry_values, index=zip_codes, name='poultry_susceptibility')
        
        print(f"\n✓ Extracted values for {len(result)} zip codes")
        print(f"  Value range: {result.min():.2f} - {result.max():.2f}")
        print(f"  Mean: {result.mean():.2f}")
        print(f"  Zip codes with data: {(result > 0).sum()}")
        
        return result


def main():
    """Main processing function."""
    print("=" * 60)
    print("Poultry Susceptibility Raster Processing")
    print("=" * 60)
    
    # File paths
    raster_path = 'data/raw/Poultry.tif'
    zip_geojson = 'data/processed/nyc_zip_codes.geojson'
    
    # Check if files exist
    if not Path(raster_path).exists():
        print(f"ERROR: {raster_path} not found")
        return
    
    if not Path(zip_geojson).exists():
        print(f"ERROR: {zip_geojson} not found")
        print("  Please run: python src/process_nyc_data.py first")
        return
    
    # Load zip code boundaries
    print(f"\nLoading zip codes from {zip_geojson}...")
    zip_gdf = gpd.read_file(zip_geojson)
    print(f"✓ Loaded {len(zip_gdf)} zip codes")
    
    # Extract poultry values
    poultry_values = extract_poultry_values_by_zip(
        raster_path,
        zip_gdf,
        method='mean'  # Use mean to get average susceptibility per zip
    )
    
    # Merge with zip code data
    print("\nMerging poultry data with zip codes...")
    zip_gdf['poultry_susceptibility'] = zip_gdf['zip_code'].map(poultry_values).fillna(0)
    
    # Save updated data
    output_dir = Path('data/processed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as GeoJSON
    output_geojson = output_dir / 'nyc_zip_codes_with_poultry.geojson'
    zip_gdf.to_file(output_geojson, driver='GeoJSON')
    print(f"\n✓ Saved to {output_geojson}")
    
    # Save as CSV
    output_csv = output_dir / 'nyc_zip_codes_with_poultry.csv'
    zip_gdf_drop_geom = pd.DataFrame(zip_gdf.drop(columns=['geometry']))
    zip_gdf_drop_geom.to_csv(output_csv, index=False)
    print(f"✓ Saved to {output_csv}")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    print(f"Total zip codes: {len(zip_gdf)}")
    print(f"Zip codes with poultry data: {(zip_gdf['poultry_susceptibility'] > 0).sum()}")
    print(f"\nPoultry Susceptibility:")
    print(f"  Min: {zip_gdf['poultry_susceptibility'].min():.2f}")
    print(f"  Max: {zip_gdf['poultry_susceptibility'].max():.2f}")
    print(f"  Mean: {zip_gdf['poultry_susceptibility'].mean():.2f}")
    print(f"  Median: {zip_gdf['poultry_susceptibility'].median():.2f}")
    
    # Top zip codes by poultry susceptibility
    print("\nTop 10 Zip Codes by Poultry Susceptibility:")
    top_poultry = zip_gdf.nlargest(10, 'poultry_susceptibility')[
        ['zip_code', 'population', 'poultry_susceptibility']
    ]
    print(top_poultry.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Use this data in risk calculations")
    print("2. Add water bodies data for wild bird proximity")
    print("3. Run risk mapping: python src/example_risk_map.py")
    print("=" * 60)


if __name__ == '__main__':
    main()

