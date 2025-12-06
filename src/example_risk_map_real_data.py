"""
Example script using REAL NYC data for H5N1 risk mapping.

This script demonstrates how to:
1. Load real NYC zip code data with population and poultry data
2. Calculate risk scores using actual data
3. Visualize risk maps
4. Export results
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from risk_map import RiskMap
import geopandas as gpd
import pandas as pd


def main():
    """
    Main example function using real NYC data.
    """
    print("=" * 60)
    print("H5N1 Risk Map - NYC Real Data")
    print("=" * 60)
    
    # Load processed NYC data with poultry, water, and SVI
    print("\n1. Loading NYC zip code data...")
    # Try to load data with SVI (most complete), fallback to water, then poultry-only
    data_file = 'data/processed/nyc_zip_codes_with_water_with_svi.geojson'
    if not os.path.exists(data_file):
        data_file = 'data/processed/nyc_zip_codes_with_water.geojson'
        print("  Note: Using data without SVI (vulnerability and healthcare will use defaults)")
    if not os.path.exists(data_file):
        data_file = 'data/processed/nyc_zip_codes_with_poultry.geojson'
        print("  Note: Using data without water proximity (using defaults)")
    
    if not os.path.exists(data_file):
        print(f"ERROR: {data_file} not found")
        print("  Please run: python src/process_svi_data.py first")
        return
    
    gdf = gpd.read_file(data_file)
    print(f"   Loaded {len(gdf)} zip codes")
    
    # Prepare data for RiskMap
    # The poultry_susceptibility column will be used as bird_density
    data = pd.DataFrame(gdf.drop(columns=['geometry']))
    
    # Rename poultry_susceptibility to bird_density for the risk map
    if 'poultry_susceptibility' in data.columns:
        data['bird_density'] = data['poultry_susceptibility']
    
    # Use SVI data if available
    if 'vulnerability_index' in data.columns:
        print("   ✓ Using SVI vulnerability_index")
    else:
        print("   ⚠️  No vulnerability_index found (using defaults)")
    
    if 'healthcare_access_score' in data.columns:
        # Invert healthcare_access_score for healthcare_capacity
        # Lower access = higher risk, so we need to invert
        # healthcare_access_score: 1 = best access, 0 = worst access
        # healthcare_capacity: should be higher = better capacity = lower risk
        # So: healthcare_capacity = healthcare_access_score (already correct direction)
        data['healthcare_capacity'] = data['healthcare_access_score']
        print("   ✓ Using SVI healthcare_access_score as healthcare_capacity")
    else:
        print("   ⚠️  No healthcare_access_score found (using defaults)")
    
    # Ensure we have required columns
    required_cols = ['zip_code', 'population', 'area_km2']
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        print(f"   WARNING: Missing columns: {missing_cols}")
        print(f"   Available columns: {list(data.columns)}")
        return
    
    # Initialize RiskMap with custom risk weights for H5N1
    print("\n2. Initializing RiskMap with H5N1-specific weights...")
    h5n1_weights = {
        'population_density': 0.25,   # Human contact risk
        'bird_density': 0.45,         # Higher weight for avian flu (poultry susceptibility)
        'water_proximity': 0.15,      # Wild bird habitats
        'healthcare_capacity': 0.10,  # Response capability
        'vulnerability_index': 0.05   # Socioeconomic factors
    }
    
    risk_map = RiskMap(
        zip_code_data=data,
        risk_weights=h5n1_weights
    )
    print("   Risk weights:", risk_map.risk_weights)
    
    # Calculate risk scores
    print("\n3. Calculating risk scores...")
    # Use SVI columns if available, otherwise use defaults
    risk_params = {
        'population_col': 'population',
        'area_col': 'area_km2',
        'bird_density_col': 'bird_density'  # Uses poultry_susceptibility
    }
    
    # Add SVI columns if available
    if 'vulnerability_index' in data.columns:
        risk_params['vulnerability_col'] = 'vulnerability_index'
        print("   ✓ Using SVI vulnerability_index")
    
    if 'healthcare_capacity' in data.columns:
        risk_params['healthcare_col'] = 'healthcare_capacity'
        print("   ✓ Using SVI healthcare_access_score as healthcare_capacity")
    
    risk_scores = risk_map.calculate_risk_scores(**risk_params)
    print(f"   Calculated risk scores for {len(risk_scores)} zip codes")
    
    # Display summary statistics
    print("\n4. Risk Score Statistics:")
    print(risk_scores['risk_score'].describe())
    
    # Display risk category distribution
    print("\n5. Risk Category Distribution:")
    print(risk_scores['risk_category'].value_counts().sort_index())
    
    # Get high-risk zip codes
    print("\n6. Top 15 High-Risk Zip Codes:")
    high_risk = risk_map.get_high_risk_zips(top_n=15)
    display_cols = ['risk_score', 'risk_category', 'population', 'bird_density']
    display_cols = [col for col in display_cols if col in high_risk.columns]
    print(high_risk[display_cols].to_string())
    
    # Create GeoDataFrame with risk scores for visualization
    print("\n7. Preparing data for visualization...")
    risk_map.risk_map_gdf = gpd.GeoDataFrame(
        pd.concat([gdf[['zip_code', 'geometry']], risk_scores], axis=1)
    )
    
    # Export results
    print("\n8. Exporting results...")
    risk_map.export_risk_data('data/processed/nyc_risk_scores.csv', format='csv')
    print("   Exported to data/processed/nyc_risk_scores.csv")
    
    # Create visualizations
    print("\n9. Creating visualizations...")
    try:
        # Static map
        risk_map.visualize_risk_map(
            output_path='data/processed/nyc_risk_map.png',
            risk_col='risk_score',
            cmap='YlOrRd',
            figsize=(14, 10),
            title='H5N1 Risk Map - NYC by Zip Code'
        )
        print("   ✓ Created static map: data/processed/nyc_risk_map.png")
        
        # Interactive map
        risk_map.create_interactive_map(
            output_path='data/processed/nyc_risk_map.html',
            risk_col='risk_score',
            popup_cols=['zip_code', 'risk_score', 'risk_category', 'population', 'bird_density']
        )
        print("   ✓ Created interactive map: data/processed/nyc_risk_map.html")
        
    except Exception as e:
        print(f"   Warning: Could not create visualizations: {e}")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
    print("\nFiles created:")
    print("  - data/processed/nyc_risk_scores.csv")
    print("  - data/processed/nyc_risk_map.png (if matplotlib available)")
    print("  - data/processed/nyc_risk_map.html (if folium available)")
    print("\nNext steps:")
    print("  - Review high-risk zip codes")
    print("  - Add water bodies data for better wild bird proximity estimates")
    print("  - Add healthcare capacity data for more accurate risk assessment")


if __name__ == '__main__':
    main()

