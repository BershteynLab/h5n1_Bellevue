"""
Process NYC zip code data for H5N1 risk mapping.

This script processes:
1. Modified ZCTA boundaries with geometry and population estimates
2. 2020 Census Decennial data for official population counts
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from risk_map import RiskMap
from data_utils import prepare_risk_data


def load_modzcta_data(file_path: str) -> gpd.GeoDataFrame:
    """
    Load NYC Modified ZCTA data with geometry and population.
    
    Parameters
    ----------
    file_path : str
        Path to MODZCTA CSV file
    
    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame with zip codes, population, and geometry
    """
    print(f"Loading MODZCTA data from {file_path}...")
    
    # Read CSV
    df = pd.read_csv(file_path)
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower()
    
    # Standardize zip code column
    if 'modzcta' in df.columns:
        df['zip_code'] = df['modzcta'].astype(str).str.zfill(5)
    elif 'zcta' in df.columns:
        df['zip_code'] = df['zcta'].astype(str).str.zfill(5)
    
    # Clean population data (remove commas)
    if 'pop_est' in df.columns:
        df['population'] = df['pop_est'].astype(str).str.replace(',', '').astype(float)
    elif 'population' in df.columns:
        df['population'] = df['population'].astype(str).str.replace(',', '').astype(float)
    
    # Convert geometry from WKT string to GeoSeries
    if 'the_geom' in df.columns:
        geometry_col = 'the_geom'
    elif 'geometry' in df.columns:
        geometry_col = 'geometry'
    else:
        raise ValueError("No geometry column found. Expected 'the_geom' or 'geometry'")
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.GeoSeries.from_wkt(df[geometry_col], crs='EPSG:4326')
    )
    
    # Calculate area in km²
    gdf_projected = gdf.to_crs('EPSG:3857')  # Web Mercator for area calculation
    gdf['area_km2'] = gdf_projected.geometry.area / 1e6
    
    print(f"✓ Loaded {len(gdf)} zip codes")
    print(f"  Population range: {gdf['population'].min():.0f} - {gdf['population'].max():.0f}")
    print(f"  Area range: {gdf['area_km2'].min():.3f} - {gdf['area_km2'].max():.3f} km²")
    
    return gdf


def load_census_data(file_path: str) -> pd.DataFrame:
    """
    Load 2020 Census Decennial data.
    
    Parameters
    ----------
    file_path : str
        Path to Census CSV file
    
    Returns
    -------
    pd.DataFrame
        DataFrame with zip codes and population
    """
    print(f"\nLoading Census data from {file_path}...")
    
    # Read CSV - first row has column names, second row is metadata, data starts at row 3
    df = pd.read_csv(file_path, header=0)
    
    # Drop the metadata row (second row)
    df = df.iloc[1:].reset_index(drop=True)
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Extract zip code from GEO_ID or NAME
    if 'GEO_ID' in df.columns:
        # Format: "860Z200US10001" -> extract "10001"
        df['zip_code'] = df['GEO_ID'].astype(str).str.extract(r'US(\d{5})')[0]
    elif 'NAME' in df.columns:
        # Format: "ZCTA5 10001" -> extract "10001"
        df['zip_code'] = df['NAME'].astype(str).str.extract(r'(\d{5})')[0]
    else:
        print("  WARNING: Could not extract zip codes")
        print(f"  Available columns: {list(df.columns)}")
        return pd.DataFrame()  # Return empty DataFrame
    
    # Get population column (usually P1_001N or similar)
    pop_cols = [col for col in df.columns if 'P1_001' in col or 'Total' in col or 'population' in col.lower()]
    if pop_cols:
        df['population_census'] = pd.to_numeric(df[pop_cols[0]], errors='coerce')
        print(f"  Using population column: {pop_cols[0]}")
    else:
        print("  WARNING: No population column found")
        df['population_census'] = 0
    
    # Select relevant columns (check if zip_code was created)
    if 'zip_code' not in df.columns:
        print("  ERROR: Could not extract zip codes")
        return pd.DataFrame()
    
    result = df[['zip_code', 'population_census']].copy()
    result = result.dropna(subset=['zip_code'])
    result['zip_code'] = result['zip_code'].astype(str).str.zfill(5)
    
    print(f"✓ Loaded {len(result)} zip codes from Census")
    print(f"  Population range: {result['population_census'].min():.0f} - {result['population_census'].max():.0f}")
    
    return result


def merge_census_population(gdf: gpd.GeoDataFrame, census_df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Merge Census population data with MODZCTA boundaries.
    
    Prefers Census data (more official) but keeps MODZCTA estimates as fallback.
    """
    print("\nMerging Census population data...")
    
    # Merge
    gdf = gdf.merge(
        census_df[['zip_code', 'population_census']],
        on='zip_code',
        how='left'
    )
    
    # Use Census data if available, otherwise use MODZCTA estimate
    gdf['population'] = gdf['population_census'].fillna(gdf['population'])
    
    # Count how many got updated
    updated = gdf['population_census'].notna().sum()
    print(f"✓ Updated {updated} zip codes with Census data")
    print(f"  {len(gdf) - updated} zip codes using MODZCTA estimates")
    
    return gdf


def main():
    """Main processing function."""
    print("=" * 60)
    print("NYC H5N1 Risk Mapping - Data Processing")
    print("=" * 60)
    
    # File paths
    modzcta_file = 'data/raw/Modified_Zip_Code_Tabulation_Areas_(MODZCTA)_20251205.csv'
    census_file = 'data/raw/DECENNIALDHC2020.P1-Data.csv'
    
    # Check if files exist
    if not Path(modzcta_file).exists():
        print(f"ERROR: {modzcta_file} not found")
        return
    
    # Load MODZCTA data (has geometry + population)
    gdf = load_modzcta_data(modzcta_file)
    
    # Load Census data if available
    if Path(census_file).exists():
        census_df = load_census_data(census_file)
        gdf = merge_census_population(gdf, census_df)
    else:
        print(f"\nNOTE: {census_file} not found, using MODZCTA population estimates only")
    
    # Save processed data
    output_dir = Path('data/processed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as GeoJSON
    output_geojson = output_dir / 'nyc_zip_codes.geojson'
    gdf.to_file(output_geojson, driver='GeoJSON')
    print(f"\n✓ Saved GeoJSON to {output_geojson}")
    
    # Save as CSV (without geometry)
    output_csv = output_dir / 'nyc_zip_codes.csv'
    gdf_drop_geom = pd.DataFrame(gdf.drop(columns=['geometry']))
    gdf_drop_geom.to_csv(output_csv, index=False)
    print(f"✓ Saved CSV to {output_csv}")
    
    # Create summary
    print("\n" + "=" * 60)
    print("Data Summary")
    print("=" * 60)
    print(f"Total zip codes: {len(gdf)}")
    print(f"Total population: {gdf['population'].sum():,.0f}")
    print(f"Average population per zip: {gdf['population'].mean():,.0f}")
    print(f"Average area: {gdf['area_km2'].mean():.3f} km²")
    print(f"Average density: {(gdf['population'] / gdf['area_km2']).mean():,.0f} people/km²")
    
    # Show sample
    print("\nSample zip codes:")
    sample = gdf[['zip_code', 'population', 'area_km2']].head(10)
    print(sample.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Add bird/poultry facility data")
    print("2. Add water bodies data")
    print("3. Add healthcare capacity data")
    print("4. Run risk calculations: python src/example_risk_map.py")
    print("=" * 60)


if __name__ == '__main__':
    main()

