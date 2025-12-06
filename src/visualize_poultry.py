"""
Create visualizations of poultry susceptibility by zip code.

This script creates maps showing:
1. Poultry susceptibility by zip code
2. Risk scores with poultry data
3. Comparison visualizations
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_poultry_susceptibility_map(
    data_file: str = 'data/processed/nyc_zip_codes_with_poultry.geojson',
    output_path: str = 'data/processed/poultry_susceptibility_map.png'
):
    """
    Create a map showing poultry susceptibility by zip code.
    """
    print("Creating poultry susceptibility map...")
    
    if not Path(data_file).exists():
        print(f"ERROR: {data_file} not found")
        return
    
    # Load data
    gdf = gpd.read_file(data_file)
    
    # Ensure CRS is appropriate for NYC
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Plot poultry susceptibility
    gdf.plot(
        column='poultry_susceptibility',
        cmap='Reds',
        legend=True,
        ax=ax,
        edgecolor='black',
        linewidth=0.3,
        legend_kwds={
            'label': 'Poultry Susceptibility Score',
            'shrink': 0.8,
            'orientation': 'horizontal',
            'pad': 0.02
        },
        missing_kwds={
            'color': 'lightgray',
            'label': 'No data'
        }
    )
    
    ax.set_title(
        'Poultry Susceptibility to Avian Influenza\nNYC Zip Codes',
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.set_axis_off()
    
    # Add text annotation
    stats_text = (
        f"Zip codes with data: {(gdf['poultry_susceptibility'] > 0).sum()}/{len(gdf)}\n"
        f"Range: {gdf['poultry_susceptibility'].min():.0f} - {gdf['poultry_susceptibility'].max():.0f}\n"
        f"Mean: {gdf['poultry_susceptibility'].mean():.0f}"
    )
    ax.text(
        0.02, 0.98, stats_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved to {output_path}")
    plt.close()


def create_risk_comparison_map(
    risk_file: str = 'data/processed/nyc_zip_codes_with_poultry.geojson',
    output_path: str = 'data/processed/risk_comparison_map.png'
):
    """
    Create a comparison map showing risk scores vs poultry susceptibility.
    """
    print("Creating risk comparison map...")
    
    # This would require risk scores to be calculated first
    # For now, just create a note
    print("  Note: Run risk calculations first to create comparison map")


def create_interactive_poultry_map(
    data_file: str = 'data/processed/nyc_zip_codes_with_poultry.geojson',
    output_path: str = 'data/processed/poultry_susceptibility_map.html'
):
    """
    Create an interactive Folium map of poultry susceptibility.
    """
    try:
        import folium
    except ImportError:
        print("  folium not available, skipping interactive map")
        return
    
    print("Creating interactive poultry susceptibility map...")
    
    if not Path(data_file).exists():
        print(f"ERROR: {data_file} not found")
        return
    
    # Load data
    gdf = gpd.read_file(data_file)
    gdf = gdf.to_crs('EPSG:4326')
    
    # Calculate center
    bounds = gdf.total_bounds
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2
    
    # Create map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add choropleth
    folium.Choropleth(
        geo_data=gdf,
        data=gdf,
        columns=['zip_code', 'poultry_susceptibility'],
        key_on='feature.properties.zip_code',
        fill_color='Reds',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Poultry Susceptibility Score',
        highlight=True
    ).add_to(m)
    
    # Add popups
    for idx, row in gdf.iterrows():
        popup_text = (
            f"<b>Zip Code:</b> {row['zip_code']}<br>"
            f"<b>Poultry Susceptibility:</b> {row['poultry_susceptibility']:.0f}<br>"
            f"<b>Population:</b> {row.get('population', 'N/A'):,.0f}"
        )
        
        folium.GeoJson(
            row.geometry,
            style_function=lambda feature: {
                'fillColor': 'transparent',
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0
            },
            tooltip=folium.Tooltip(popup_text, sticky=True)
        ).add_to(m)
    
    # Save
    m.save(output_path)
    print(f"✓ Saved to {output_path}")


def main():
    """Main visualization function."""
    print("=" * 60)
    print("Poultry Susceptibility Visualization")
    print("=" * 60)
    
    # Create static map
    create_poultry_susceptibility_map()
    
    # Create interactive map
    create_interactive_poultry_map()
    
    print("\n" + "=" * 60)
    print("Visualizations complete!")
    print("=" * 60)
    print("\nFiles created:")
    print("  - data/processed/poultry_susceptibility_map.png")
    print("  - data/processed/poultry_susceptibility_map.html")
    print("\nOpen the HTML file in a browser to explore the interactive map!")


if __name__ == '__main__':
    main()

