#!/usr/bin/env python3
"""
Process CDC Social Vulnerability Index (SVI) data for NYC zip codes.
Extracts vulnerability scores and healthcare access indicators.
"""

import os
import sys
import pandas as pd
import geopandas as gpd
from pathlib import Path

def load_svi_data(file_path: str) -> pd.DataFrame:
    """Load and process SVI data from CSV."""
    print(f"Loading SVI data from {file_path}...")
    
    df = pd.read_csv(file_path)
    print(f"  Loaded {len(df)} ZCTAs")
    
    # Extract zip code from FIPS (FIPS is 5-digit ZCTA code)
    df['zip_code'] = df['FIPS'].astype(str).str.zfill(5)
    
    # Filter to NYC zip codes (10001-11697)
    nyc_mask = (
        (df['zip_code'].str.match(r'^10[0-9]{3}')) |
        (df['zip_code'].str.match(r'^11[0-6][0-9]{2}'))
    )
    df_nyc = df[nyc_mask].copy()
    print(f"  Found {len(df_nyc)} NYC zip codes")
    
    return df_nyc

def extract_vulnerability_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Extract vulnerability metrics from SVI data."""
    print("\nExtracting vulnerability metrics...")
    
    result = df[['zip_code']].copy()
    
    # Overall SVI rank (0-1, higher = more vulnerable)
    if 'RPL_THEMES' in df.columns:
        result['vulnerability_index'] = df['RPL_THEMES'] / 100.0  # Normalize to 0-1
        print(f"  ✓ Added vulnerability_index (RPL_THEMES)")
    elif 'SPL_THEMES' in df.columns:
        # Use sum of theme percentiles if RPL not available
        result['vulnerability_index'] = df['SPL_THEMES'] / 400.0  # Normalize
        print(f"  ✓ Added vulnerability_index (SPL_THEMES)")
    else:
        print("  ⚠️  No overall vulnerability index found")
        result['vulnerability_index'] = 0.5  # Default
    
    # Theme-specific scores (optional, for detailed analysis)
    theme_cols = {
        'RPL_THEME1': 'vulnerability_theme1_socioeconomic',
        'RPL_THEME2': 'vulnerability_theme2_household',
        'RPL_THEME3': 'vulnerability_theme3_minority',
        'RPL_THEME4': 'vulnerability_theme4_housing'
    }
    
    for col, new_col in theme_cols.items():
        if col in df.columns:
            result[new_col] = df[col] / 100.0
            print(f"  ✓ Added {new_col}")
    
    return result

def extract_healthcare_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Extract healthcare-related indicators from SVI data."""
    print("\nExtracting healthcare indicators...")
    
    result = pd.DataFrame()
    
    # Healthcare access indicators in SVI
    # EP_UNINSUR: Percentage uninsured (higher = worse access)
    # EP_NOINT: Percentage without internet (proxy for telehealth access)
    
    if 'EP_UNINSUR' in df.columns:
        # Invert: lower uninsured = higher capacity
        # Normalize to 0-1 where 1 = best access (lowest uninsured rate)
        # EP_UNINSUR is already a percentage (0-100), but may have outliers
        uninsured_pct = (df['EP_UNINSUR'] / 100.0).clip(0, 1)  # Clip to 0-1 range
        result['healthcare_access_score'] = 1.0 - uninsured_pct
        # Ensure final score is also in 0-1 range
        result['healthcare_access_score'] = result['healthcare_access_score'].clip(0, 1)
        print(f"  ✓ Added healthcare_access_score (from EP_UNINSUR)")
        print(f"    Range: {result['healthcare_access_score'].min():.3f} - {result['healthcare_access_score'].max():.3f}")
    else:
        print("  ⚠️  EP_UNINSUR not found, cannot calculate healthcare access")
    
    if 'EP_NOINT' in df.columns:
        # Internet access as proxy for telehealth capacity
        no_internet_pct = df['EP_NOINT'] / 100.0
        result['telehealth_access_score'] = 1.0 - no_internet_pct
        print(f"  ✓ Added telehealth_access_score (from EP_NOINT)")
    
    return result

def merge_with_existing_data(svi_df: pd.DataFrame, processed_file: str) -> gpd.GeoDataFrame:
    """Merge SVI data with existing processed NYC zip code data."""
    print(f"\nMerging with existing data: {processed_file}...")
    
    if not os.path.exists(processed_file):
        print(f"  ⚠️  File not found: {processed_file}")
        print("  Creating new file with SVI data only...")
        return None
    
    # Load existing processed data
    gdf = gpd.read_file(processed_file)
    print(f"  Loaded {len(gdf)} zip codes from existing data")
    
    # Ensure zip_code is string in both
    gdf['zip_code'] = gdf['zip_code'].astype(str).str.zfill(5)
    svi_df['zip_code'] = svi_df['zip_code'].astype(str).str.zfill(5)
    
    # Merge
    gdf_merged = gdf.merge(svi_df, on='zip_code', how='left', suffixes=('', '_svi'))
    
    # Check merge success
    merged_count = gdf_merged['vulnerability_index'].notna().sum() if 'vulnerability_index' in gdf_merged.columns else 0
    print(f"  ✓ Successfully merged SVI data for {merged_count} zip codes")
    
    if merged_count < len(gdf) * 0.8:
        print(f"  ⚠️  Warning: Only {merged_count}/{len(gdf)} zip codes matched")
    
    return gdf_merged

def main():
    """Main processing function."""
    print("=" * 70)
    print("Processing CDC Social Vulnerability Index (SVI) Data")
    print("=" * 70)
    print()
    
    # Input file
    svi_file = 'data/raw/NewYork_ZCTA.csv'
    if not os.path.exists(svi_file):
        print(f"ERROR: {svi_file} not found")
        print("  Please download SVI data from:")
        print("  https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html")
        return
    
    # Load SVI data
    svi_df = load_svi_data(svi_file)
    
    # Extract vulnerability metrics
    vulnerability_df = extract_vulnerability_metrics(svi_df)
    
    # Extract healthcare indicators
    healthcare_df = extract_healthcare_indicators(svi_df)
    
    # Combine all metrics
    metrics_df = vulnerability_df.copy()
    if not healthcare_df.empty:
        metrics_df = pd.concat([metrics_df, healthcare_df], axis=1)
    
    # Save standalone SVI metrics
    output_csv = 'data/processed/nyc_svi_metrics.csv'
    metrics_df.to_csv(output_csv, index=False)
    print(f"\n✓ Saved SVI metrics to {output_csv}")
    
    # Merge with existing processed data (prefer water data as it's most complete)
    processed_files = [
        'data/processed/nyc_zip_codes_with_water.geojson',
        'data/processed/nyc_zip_codes_with_poultry.geojson',
        'data/processed/nyc_zip_codes.geojson'
    ]
    
    merged_gdf = None
    for processed_file in processed_files:
        if os.path.exists(processed_file):
            merged_gdf = merge_with_existing_data(metrics_df, processed_file)
            if merged_gdf is not None:
                # Save merged data
                output_file = processed_file.replace('.geojson', '_with_svi.geojson')
                merged_gdf.to_file(output_file, driver='GeoJSON')
                print(f"✓ Saved merged data to {output_file}")
                break
    
    if merged_gdf is None:
        print("\n⚠️  Could not merge with existing data")
        print("  SVI metrics saved separately to:", output_csv)
        print("  You can manually merge this data later")
    
    print()
    print("=" * 70)
    print("SVI Data Processing Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Update risk mapping script to use vulnerability_index from SVI")
    if 'healthcare_access_score' in metrics_df.columns:
        print("  2. Consider using healthcare_access_score for healthcare capacity")
    print("  3. Run: python src/example_risk_map_real_data.py")

if __name__ == '__main__':
    main()

