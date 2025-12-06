"""
Process water body data to calculate water proximity for NYC zip codes.

This script:
1. Loads water body data (from NYC Open Data or USGS NHD)
2. Calculates proximity to water for each zip code
3. Updates the risk mapping dataset
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_utils import calculate_water_proximity


def load_nyc_water_data(file_path: str) -> gpd.GeoDataFrame:
    """
    Load water body data from various formats.
    
    Supports:
    - GeoJSON
    - Shapefile
    - File Geodatabase (GDB)
    """
    print(f"Loading water data from {file_path}...")
    
    if file_path.endswith('.geojson'):
        gdf = gpd.read_file(file_path)
    elif file_path.endswith('.shp'):
        gdf = gpd.read_file(file_path)
    elif file_path.endswith('.gdb'):
        # For GDB, need to specify layer name
        # Common layer names: 'NHDFlowline', 'NHDWaterbody', 'NHDArea'
        try:
            gdf = gpd.read_file(file_path, layer='NHDWaterbody')
        except:
            # Try other common layer names
            try:
                gdf = gpd.read_file(file_path, layer='NHDArea')
            except:
                print("  Available layers:")
                import fiona
                print(fiona.listlayers(file_path))
                raise ValueError("Please specify the correct layer name")
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    
    print(f"✓ Loaded {len(gdf)} water features")
    print(f"  CRS: {gdf.crs}")
    print(f"  Columns: {list(gdf.columns)[:10]}")
    
    return gdf


def process_water_proximity(
    zip_gdf: gpd.GeoDataFrame,
    water_gdf: gpd.GeoDataFrame,
    method: str = 'distance'
) -> pd.Series:
    """
    Calculate water proximity for each zip code.
    
    Parameters
    ----------
    zip_gdf : gpd.GeoDataFrame
        Zip code boundaries
    water_gdf : gpd.GeoDataFrame
        Water body geometries
    method : str
        'distance' or 'overlap'
    
    Returns
    -------
    pd.Series
        Water proximity scores (0-1 scale)
    """
    print(f"\nCalculating water proximity using '{method}' method...")
    
    # Use the utility function
    proximity = calculate_water_proximity(zip_gdf, water_gdf, method=method)
    
    return proximity


def main():
    """Main processing function."""
    print("=" * 60)
    print("Water Proximity Data Processing")
    print("=" * 60)
    
    # Check for water data files
    water_data_dir = Path('data/raw')
    shape_dir = water_data_dir / 'Shape'
    
    # Check for NHD shapefiles (preferred)
    nhd_waterbody = shape_dir / 'NHDWaterbody.shp'
    nhd_flowline = shape_dir / 'NHDFlowline.shp'
    nhd_area = shape_dir / 'NHDArea.shp'
    
    # Check for other formats
    possible_files = [
        'nyc_water_bodies.geojson',
        'nyc_hydrography.geojson',
        'Hydrography.geojson',
        'NHD_H_NewYork_State.gdb'
    ]
    
    water_files = []
    
    # Check for NHD shapefiles
    if nhd_waterbody.exists():
        water_files.append(('NHDWaterbody', str(nhd_waterbody)))
    if nhd_flowline.exists():
        water_files.append(('NHDFlowline', str(nhd_flowline)))
    if nhd_area.exists():
        water_files.append(('NHDArea', str(nhd_area)))
    
    # Check for other formats
    for filename in possible_files:
        filepath = water_data_dir / filename
        if filepath.exists():
            water_files.append(('Other', str(filepath)))
            break
    
    if not water_files:
        print("\nNo water data file found!")
        print("\nPlease download water data:")
        print("  1. NYC Open Data (EASIEST):")
        print("     https://data.cityofnewyork.us/Environment/Hydrography/9ar3-6nj9")
        print("     Export as GeoJSON → Save to: data/raw/nyc_water_bodies.geojson")
        print("\n  2. Or USGS NHD for New York State:")
        print("     https://www.usgs.gov/national-hydrography/access-national-hydrography-products")
        print("     Download NHD by State → New York")
        return
    
    print(f"\nFound {len(water_files)} water data source(s):")
    for name, path in water_files:
        print(f"  - {name}: {path}")
    
    # Load zip codes
    zip_file = 'data/processed/nyc_zip_codes_with_poultry.geojson'
    if not Path(zip_file).exists():
        print(f"\nERROR: {zip_file} not found")
        print("  Please run: python src/process_poultry_raster.py first")
        return
    
    print(f"\nLoading zip codes from {zip_file}...")
    zip_gdf = gpd.read_file(zip_file)
    print(f"✓ Loaded {len(zip_gdf)} zip codes")
    
    # Load and combine water data from multiple sources
    print("\nLoading water data...")
    water_geoms = []
    
    # Load NHD water bodies (lakes, ponds, reservoirs)
    if nhd_waterbody.exists():
        print("  Loading NHDWaterbody (lakes, ponds, reservoirs)...")
        waterbody = gpd.read_file(str(nhd_waterbody))
        # Filter to NYC area for efficiency
        nyc_bounds = zip_gdf.total_bounds
        waterbody = waterbody.cx[
            nyc_bounds[0]-0.1:nyc_bounds[2]+0.1,
            nyc_bounds[1]-0.1:nyc_bounds[3]+0.1
        ]
        water_geoms.append(waterbody)
        print(f"    Loaded {len(waterbody)} water bodies in NYC area")
    
    # Load NHD flowlines (rivers, streams)
    if nhd_flowline.exists():
        print("  Loading NHDFlowline (rivers, streams)...")
        flowline = gpd.read_file(str(nhd_flowline))
        # Filter to NYC area
        nyc_bounds = zip_gdf.total_bounds
        flowline = flowline.cx[
            nyc_bounds[0]-0.1:nyc_bounds[2]+0.1,
            nyc_bounds[1]-0.1:nyc_bounds[3]+0.1
        ]
        water_geoms.append(flowline)
        print(f"    Loaded {len(flowline)} rivers/streams in NYC area")
    
    # Load NHD areas (water areas)
    if nhd_area.exists():
        print("  Loading NHDArea (water areas)...")
        nhd_area_gdf = gpd.read_file(str(nhd_area))
        # Filter to NYC area
        nyc_bounds = zip_gdf.total_bounds
        nhd_area_gdf = nhd_area_gdf.cx[
            nyc_bounds[0]-0.1:nyc_bounds[2]+0.1,
            nyc_bounds[1]-0.1:nyc_bounds[3]+0.1
        ]
        water_geoms.append(nhd_area_gdf)
        print(f"    Loaded {len(nhd_area_gdf)} water areas in NYC area")
    
    # Combine all water features
    if water_geoms:
        # Ensure all have same CRS
        for i, gdf in enumerate(water_geoms):
            if gdf.crs != zip_gdf.crs:
                water_geoms[i] = gdf.to_crs(zip_gdf.crs)
        
        # Combine into single GeoDataFrame
        water_gdf = gpd.GeoDataFrame(
            pd.concat([gdf[['geometry']] for gdf in water_geoms], ignore_index=True),
            crs=zip_gdf.crs
        )
        print(f"\n✓ Combined {len(water_gdf)} total water features")
    else:
        # Fallback to other formats
        water_file = water_files[0][1]
        water_gdf = load_nyc_water_data(water_file)
        if zip_gdf.crs != water_gdf.crs:
            print(f"\nReprojecting water data from {water_gdf.crs} to {zip_gdf.crs}...")
            water_gdf = water_gdf.to_crs(zip_gdf.crs)
    
    # Calculate proximity
    water_proximity = process_water_proximity(zip_gdf, water_gdf, method='distance')
    
    # Add to zip code data
    print("\nAdding water proximity to zip code data...")
    zip_gdf['water_proximity'] = water_proximity
    
    # Save updated data
    output_dir = Path('data/processed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / 'nyc_zip_codes_with_water.geojson'
    zip_gdf.to_file(output_file, driver='GeoJSON')
    print(f"✓ Saved to {output_file}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Water proximity range: {water_proximity.min():.3f} - {water_proximity.max():.3f}")
    print(f"Mean proximity: {water_proximity.mean():.3f}")
    print(f"Zip codes with high proximity (>0.7): {(water_proximity > 0.7).sum()}")
    
    print("\nTop 10 Zip Codes by Water Proximity:")
    top_water = zip_gdf.nlargest(10, 'water_proximity')[
        ['zip_code', 'water_proximity', 'population']
    ]
    print(top_water.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Update risk calculations with water proximity data")
    print("2. Run: python src/example_risk_map_real_data.py")
    print("=" * 60)


if __name__ == '__main__':
    main()

