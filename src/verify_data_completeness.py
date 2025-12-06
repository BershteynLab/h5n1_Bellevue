#!/usr/bin/env python3
"""
Verify data completeness for H5N1 risk mapping.
Checks all required data files and reports status.
"""

import os
import sys
import pandas as pd
import geopandas as gpd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_file_exists(filepath, description):
    """Check if a file exists and return status."""
    exists = os.path.exists(filepath)
    size = os.path.getsize(filepath) if exists else 0
    return {
        'exists': exists,
        'size_mb': round(size / (1024 * 1024), 2) if exists else 0,
        'description': description
    }

def check_svi_data():
    """Check SVI (Social Vulnerability Index) data."""
    results = {}
    
    # Check NewYork_ZCTA.csv (NY-specific SVI)
    ny_file = 'data/raw/NewYork_ZCTA.csv'
    if os.path.exists(ny_file):
        try:
            df = pd.read_csv(ny_file, nrows=1)
            results['ny_svi'] = {
                'exists': True,
                'has_rpl_themes': 'RPL_THEMES' in df.columns,
                'has_fips': 'FIPS' in df.columns,
                'has_rpl_theme1': 'RPL_THEME1' in df.columns,
                'columns': list(df.columns)[:10],
                'total_rows': len(pd.read_csv(ny_file))
            }
        except Exception as e:
            results['ny_svi'] = {'exists': True, 'error': str(e)}
    else:
        results['ny_svi'] = {'exists': False}
    
    # Check national SVI file
    nat_file = 'data/raw/svi_interactive_map.csv'
    if os.path.exists(nat_file):
        try:
            df = pd.read_csv(nat_file, nrows=1)
            results['national_svi'] = {
                'exists': True,
                'has_rpl_themes': 'RPL_THEMES' in df.columns,
                'has_fips': 'FIPS' in df.columns
            }
        except Exception as e:
            results['national_svi'] = {'exists': True, 'error': str(e)}
    else:
        results['national_svi'] = {'exists': False}
    
    return results

def check_healthcare_data():
    """Check for healthcare capacity data."""
    results = {}
    
    # Check for hospital files
    hospital_files = [
        ('data/raw/nyc_hospitals.geojson', 'GeoJSON'),
        ('data/raw/nyc_hospitals.csv', 'CSV'),
        ('data/raw/nyc_hospitals.shp', 'Shapefile')
    ]
    
    found = False
    for filepath, filetype in hospital_files:
        if os.path.exists(filepath):
            results['hospitals'] = {
                'exists': True,
                'filetype': filetype,
                'filepath': filepath
            }
            found = True
            break
    
    if not found:
        results['hospitals'] = {'exists': False}
    
    return results

def check_all_data():
    """Comprehensive data check."""
    print("=" * 70)
    print("H5N1 Risk Mapping - Data Completeness Check")
    print("=" * 70)
    print()
    
    # Priority 1: Essential
    print("📋 PRIORITY 1: Essential Data")
    print("-" * 70)
    
    # Zip code boundaries
    zip_files = [
        ('data/raw/Modified_Zip_Code_Tabulation_Areas_(MODZCTA)_20251205.csv', 'MODZCTA CSV'),
        ('data/processed/nyc_zip_codes.geojson', 'Processed GeoJSON')
    ]
    zip_found = False
    for filepath, desc in zip_files:
        status = check_file_exists(filepath, desc)
        if status['exists']:
            print(f"  ✅ {desc}: {filepath} ({status['size_mb']} MB)")
            zip_found = True
    if not zip_found:
        print("  ❌ Zip code boundaries: NOT FOUND")
    
    # Population data
    pop_files = [
        ('data/raw/DECENNIALDHC2020.P1-Data.csv', 'Census 2020'),
        ('data/processed/nyc_zip_codes.geojson', 'Processed (includes population)')
    ]
    pop_found = False
    for filepath, desc in pop_files:
        status = check_file_exists(filepath, desc)
        if status['exists']:
            print(f"  ✅ {desc}: {filepath} ({status['size_mb']} MB)")
            pop_found = True
    if not pop_found:
        print("  ❌ Population data: NOT FOUND")
    
    print()
    
    # Priority 2: Critical for H5N1
    print("📋 PRIORITY 2: Critical for H5N1")
    print("-" * 70)
    
    # Poultry data
    poultry_files = [
        ('data/raw/Poultry.tif', 'USGS Poultry Raster'),
        ('data/processed/nyc_zip_codes_with_poultry.geojson', 'Processed with poultry')
    ]
    poultry_found = False
    for filepath, desc in poultry_files:
        status = check_file_exists(filepath, desc)
        if status['exists']:
            print(f"  ✅ {desc}: {filepath} ({status['size_mb']} MB)")
            poultry_found = True
    if not poultry_found:
        print("  ❌ Poultry/bird data: NOT FOUND")
    
    # Water data
    water_files = [
        ('data/raw/Shape/NHDWaterbody.shp', 'NHD Waterbody'),
        ('data/raw/Shape/NHDFlowline.shp', 'NHD Flowline'),
        ('data/processed/nyc_zip_codes_with_water.geojson', 'Processed with water')
    ]
    water_found = False
    for filepath, desc in water_files:
        status = check_file_exists(filepath, desc)
        if status['exists']:
            print(f"  ✅ {desc}: {filepath} ({status['size_mb']} MB)")
            water_found = True
    if not water_found:
        print("  ❌ Water body data: NOT FOUND")
    
    print()
    
    # Priority 3: Important for Risk Assessment
    print("📋 PRIORITY 3: Important for Risk Assessment")
    print("-" * 70)
    
    # Healthcare data
    hc_results = check_healthcare_data()
    if hc_results.get('hospitals', {}).get('exists'):
        print(f"  ✅ Healthcare data: {hc_results['hospitals']['filepath']}")
    else:
        print("  ⚠️  Healthcare data: NOT FOUND (using defaults)")
    
    # Vulnerability data (SVI)
    svi_results = check_svi_data()
    if svi_results.get('ny_svi', {}).get('exists'):
        ny_svi = svi_results['ny_svi']
        print(f"  ✅ SVI data (NY): data/raw/NewYork_ZCTA.csv")
        if ny_svi.get('has_rpl_themes'):
            print(f"     - Has RPL_THEMES (overall vulnerability): ✅")
        if ny_svi.get('has_fips'):
            print(f"     - Has FIPS (zip codes): ✅")
            if 'total_rows' in ny_svi:
                print(f"     - Total ZCTAs: {ny_svi['total_rows']}")
    else:
        print("  ⚠️  SVI data: NOT FOUND (using defaults)")
    
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    essential_complete = zip_found and pop_found
    critical_complete = poultry_found and water_found
    important_complete = hc_results.get('hospitals', {}).get('exists') and svi_results.get('ny_svi', {}).get('exists')
    
    print(f"Essential Data:        {'✅ COMPLETE' if essential_complete else '❌ INCOMPLETE'}")
    print(f"Critical H5N1 Data:    {'✅ COMPLETE' if critical_complete else '⚠️  PARTIAL'}")
    print(f"Risk Assessment Data:  {'✅ COMPLETE' if important_complete else '⚠️  PARTIAL'}")
    
    print()
    
    # Current risk score breakdown
    print("Current Risk Score Coverage:")
    print("  Population Density:     25% - " + ("✅ Real data" if pop_found else "❌ Missing"))
    print("  Poultry Density:         45% - " + ("✅ Real data" if poultry_found else "❌ Missing"))
    print("  Water Proximity:         15% - " + ("✅ Real data" if water_found else "❌ Missing"))
    print("  Healthcare Capacity:     10% - " + ("✅ Real data" if hc_results.get('hospitals', {}).get('exists') else "⚠️  Using default"))
    print("  Vulnerability Index:      5% - " + ("✅ Real data" if svi_results.get('ny_svi', {}).get('exists') else "⚠️  Using default"))
    
    total_with_real = sum([
        0.25 if pop_found else 0,
        0.45 if poultry_found else 0,
        0.15 if water_found else 0,
        0.10 if hc_results.get('hospitals', {}).get('exists') else 0,
        0.05 if svi_results.get('ny_svi', {}).get('exists') else 0
    ])
    
    print()
    print(f"Total with real data: {total_with_real*100:.0f}%")
    print(f"Total with defaults:  {(1-total_with_real)*100:.0f}%")
    
    print()
    print("=" * 70)
    
    # Recommendations
    if not important_complete:
        print("\n📝 RECOMMENDATIONS:")
        if not hc_results.get('hospitals', {}).get('exists'):
            print("  • Download healthcare data from CMS Hospital Compare or NYC Open Data")
        if not svi_results.get('ny_svi', {}).get('exists'):
            print("  • Process SVI data: NewYork_ZCTA.csv appears to be available")
            print("    Run: python src/process_svi_data.py (if script exists)")
    
    return {
        'essential': essential_complete,
        'critical': critical_complete,
        'important': important_complete,
        'total_coverage': total_with_real
    }

if __name__ == '__main__':
    check_all_data()

