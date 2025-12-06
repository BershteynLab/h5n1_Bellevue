"""
Example script demonstrating how to use the RiskMap module.

This script shows how to:
1. Load zip code data
2. Calculate risk scores
3. Visualize risk maps
4. Export results
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from risk_map import RiskMap, create_sample_data
import pandas as pd


def main():
    """
    Main example function demonstrating RiskMap usage.
    """
    print("=" * 60)
    print("H5N1 Risk Map Example")
    print("=" * 60)
    
    # Option 1: Use sample data (for testing)
    print("\n1. Creating sample data...")
    sample_data = create_sample_data(n_zips=50)
    print(f"   Created {len(sample_data)} sample zip codes")
    
    # Option 2: Load real data from file
    # risk_map = RiskMap()
    # gdf = risk_map.load_zip_code_data('data/raw/nyc_zip_codes.geojson')
    
    # Initialize RiskMap with custom risk weights (optional)
    print("\n2. Initializing RiskMap...")
    custom_weights = {
        'population_density': 0.25,
        'bird_density': 0.45,  # Higher weight for bird density (H5N1 is avian)
        'water_proximity': 0.20,
        'healthcare_capacity': 0.05,
        'vulnerability_index': 0.05
    }
    
    risk_map = RiskMap(
        zip_code_data=sample_data,
        risk_weights=custom_weights
    )
    print("   Risk weights:", risk_map.risk_weights)
    
    # Calculate risk scores
    print("\n3. Calculating risk scores...")
    risk_scores = risk_map.calculate_risk_scores()
    print(f"   Calculated risk scores for {len(risk_scores)} zip codes")
    
    # Display summary statistics
    print("\n4. Risk Score Statistics:")
    print(risk_scores['risk_score'].describe())
    
    # Display risk category distribution
    print("\n5. Risk Category Distribution:")
    print(risk_scores['risk_category'].value_counts().sort_index())
    
    # Get high-risk zip codes
    print("\n6. Top 10 High-Risk Zip Codes:")
    high_risk = risk_map.get_high_risk_zips(top_n=10)
    print(high_risk[['risk_score', 'risk_category']].to_string())
    
    # Export results
    print("\n7. Exporting results...")
    risk_map.export_risk_data('data/processed/risk_scores.csv', format='csv')
    print("   Exported to data/processed/risk_scores.csv")
    
    # Note: Visualization requires geometry data
    # For real data with geometry:
    # risk_map.visualize_risk_map(output_path='data/processed/risk_map.png')
    # risk_map.create_interactive_map(output_path='data/processed/risk_map.html')
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()

