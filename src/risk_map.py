"""
Spatial Risk Map Module for H5N1 Outbreak Preparedness

This module provides functionality to create risk maps by zip code for H5N1 outbreaks.
It incorporates multiple risk factors including population density, bird/poultry density,
and other relevant epidemiological factors.

Author: H5N1 Bellevue Project
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from typing import Dict, List, Optional, Tuple, Union
import warnings
warnings.filterwarnings('ignore')


class RiskMap:
    """
    A class to create and visualize spatial risk maps for H5N1 outbreaks by zip code.
    
    Risk factors considered:
    - Population density
    - Bird/poultry density
    - Proximity to water bodies (wild bird habitats)
    - Healthcare capacity
    - Socioeconomic vulnerability
    """
    
    def __init__(
        self,
        zip_code_data: Optional[Union[pd.DataFrame, gpd.GeoDataFrame]] = None,
        risk_weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize the RiskMap object.
        
        Parameters
        ----------
        zip_code_data : pd.DataFrame or gpd.GeoDataFrame, optional
            DataFrame containing zip code data with columns:
            - zip_code: zip code identifier
            - population: population count
            - area_km2: area in square kilometers (for density calculation)
            - bird_density: density of birds/poultry (optional)
            - water_proximity: proximity to water bodies score (optional)
            - healthcare_capacity: healthcare capacity index (optional)
            - vulnerability_index: socioeconomic vulnerability index (optional)
            - geometry: GeoSeries geometry (if GeoDataFrame)
        
        risk_weights : dict, optional
            Dictionary of risk factor weights. Default weights:
            {
                'population_density': 0.3,
                'bird_density': 0.4,
                'water_proximity': 0.15,
                'healthcare_capacity': 0.1,
                'vulnerability_index': 0.05
            }
            Weights should sum to approximately 1.0
        """
        self.zip_code_data = zip_code_data
        self.risk_scores = None
        self.risk_map_gdf = None
        
        # Default risk weights
        default_weights = {
            'population_density': 0.3,
            'bird_density': 0.4,
            'water_proximity': 0.15,
            'healthcare_capacity': 0.1,
            'vulnerability_index': 0.05
        }
        
        self.risk_weights = risk_weights if risk_weights else default_weights
        
        # Normalize weights to sum to 1.0
        total_weight = sum(self.risk_weights.values())
        if total_weight > 0:
            self.risk_weights = {k: v/total_weight for k, v in self.risk_weights.items()}
    
    def load_zip_code_data(
        self,
        file_path: str,
        zip_code_col: str = 'zip_code',
        geometry_col: Optional[str] = None
    ) -> gpd.GeoDataFrame:
        """
        Load zip code data from a file (CSV, GeoJSON, Shapefile, etc.).
        
        Parameters
        ----------
        file_path : str
            Path to the data file
        zip_code_col : str
            Name of the zip code column
        geometry_col : str, optional
            Name of the geometry column (if loading from CSV)
        
        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame with zip code data
        """
        if file_path.endswith('.geojson') or file_path.endswith('.shp'):
            gdf = gpd.read_file(file_path)
        else:
            df = pd.read_csv(file_path)
            if geometry_col and geometry_col in df.columns:
                gdf = gpd.GeoDataFrame(
                    df,
                    geometry=gpd.GeoSeries.from_wkt(df[geometry_col])
                )
            else:
                gdf = gpd.GeoDataFrame(df)
        
        self.zip_code_data = gdf
        return gdf
    
    def calculate_population_density(
        self,
        population_col: str = 'population',
        area_col: str = 'area_km2'
    ) -> pd.Series:
        """
        Calculate population density for each zip code.
        
        Parameters
        ----------
        population_col : str
            Name of the population column
        area_col : str
            Name of the area column (in km²)
        
        Returns
        -------
        pd.Series
            Population density (people per km²)
        """
        if self.zip_code_data is None:
            raise ValueError("No zip code data loaded. Use load_zip_code_data() first.")
        
        if area_col not in self.zip_code_data.columns:
            # Try to calculate area from geometry if available
            if hasattr(self.zip_code_data, 'geometry') and self.zip_code_data.geometry is not None:
                # Convert to appropriate CRS for area calculation (e.g., UTM)
                gdf = self.zip_code_data.to_crs('EPSG:3857')  # Web Mercator
                self.zip_code_data[area_col] = gdf.geometry.area / 1e6  # Convert m² to km²
            else:
                raise ValueError(f"Area column '{area_col}' not found and cannot calculate from geometry.")
        
        density = self.zip_code_data[population_col] / self.zip_code_data[area_col]
        # Replace inf and NaN with 0
        density = density.replace([np.inf, -np.inf], 0).fillna(0)
        
        return density
    
    def normalize_risk_factor(self, series: pd.Series, method: str = 'min_max') -> pd.Series:
        """
        Normalize a risk factor to 0-1 scale.
        
        Parameters
        ----------
        series : pd.Series
            Series to normalize
        method : str
            Normalization method: 'min_max' or 'z_score'
        
        Returns
        -------
        pd.Series
            Normalized series (0-1 scale)
        """
        if method == 'min_max':
            min_val = series.min()
            max_val = series.max()
            if max_val - min_val > 0:
                normalized = (series - min_val) / (max_val - min_val)
            else:
                normalized = pd.Series(0, index=series.index)
        elif method == 'z_score':
            mean_val = series.mean()
            std_val = series.std()
            if std_val > 0:
                normalized = (series - mean_val) / std_val
                # Convert z-scores to 0-1 scale using sigmoid
                normalized = 1 / (1 + np.exp(-normalized))
            else:
                normalized = pd.Series(0.5, index=series.index)
        else:
            raise ValueError(f"Unknown normalization method: {method}")
        
        return normalized.fillna(0)
    
    def calculate_risk_scores(
        self,
        population_col: str = 'population',
        area_col: str = 'area_km2',
        bird_density_col: Optional[str] = 'bird_density',
        water_proximity_col: Optional[str] = 'water_proximity',
        healthcare_col: Optional[str] = 'healthcare_capacity',
        vulnerability_col: Optional[str] = 'vulnerability_index'
    ) -> pd.DataFrame:
        """
        Calculate composite risk scores for each zip code.
        
        Parameters
        ----------
        population_col : str
            Name of the population column
        area_col : str
            Name of the area column
        bird_density_col : str, optional
            Name of the bird density column
        water_proximity_col : str, optional
            Name of the water proximity column
        healthcare_col : str, optional
            Name of the healthcare capacity column
        vulnerability_col : str, optional
            Name of the vulnerability index column
        
        Returns
        -------
        pd.DataFrame
            DataFrame with risk scores and individual risk factors
        """
        if self.zip_code_data is None:
            raise ValueError("No zip code data loaded. Use load_zip_code_data() first.")
        
        results = pd.DataFrame(index=self.zip_code_data.index)
        
        # Calculate population density
        pop_density = self.calculate_population_density(population_col, area_col)
        results['population_density'] = pop_density
        results['population_density_norm'] = self.normalize_risk_factor(pop_density)
        
        # Bird density (if available)
        if bird_density_col and bird_density_col in self.zip_code_data.columns:
            bird_density = self.zip_code_data[bird_density_col].fillna(0)
            results['bird_density'] = bird_density
            results['bird_density_norm'] = self.normalize_risk_factor(bird_density)
        else:
            results['bird_density_norm'] = 0
        
        # Water proximity (if available)
        if water_proximity_col and water_proximity_col in self.zip_code_data.columns:
            water_prox = self.zip_code_data[water_proximity_col].fillna(0)
            results['water_proximity'] = water_prox
            results['water_proximity_norm'] = self.normalize_risk_factor(water_prox)
        else:
            results['water_proximity_norm'] = 0
        
        # Healthcare capacity (if available) - lower capacity = higher risk
        if healthcare_col and healthcare_col in self.zip_code_data.columns:
            healthcare = self.zip_code_data[healthcare_col].fillna(0)
            results['healthcare_capacity'] = healthcare
            # Invert: lower capacity = higher risk
            healthcare_norm = self.normalize_risk_factor(healthcare)
            results['healthcare_capacity_norm'] = 1 - healthcare_norm
        else:
            results['healthcare_capacity_norm'] = 0
        
        # Vulnerability index (if available)
        if vulnerability_col and vulnerability_col in self.zip_code_data.columns:
            vulnerability = self.zip_code_data[vulnerability_col].fillna(0)
            results['vulnerability_index'] = vulnerability
            results['vulnerability_index_norm'] = self.normalize_risk_factor(vulnerability)
        else:
            results['vulnerability_index_norm'] = 0
        
        # Calculate composite risk score
        risk_score = (
            results['population_density_norm'] * self.risk_weights.get('population_density', 0) +
            results['bird_density_norm'] * self.risk_weights.get('bird_density', 0) +
            results['water_proximity_norm'] * self.risk_weights.get('water_proximity', 0) +
            results['healthcare_capacity_norm'] * self.risk_weights.get('healthcare_capacity', 0) +
            results['vulnerability_index_norm'] * self.risk_weights.get('vulnerability_index', 0)
        )
        
        results['risk_score'] = risk_score
        results['risk_category'] = pd.cut(
            risk_score,
            bins=[0, 0.25, 0.5, 0.75, 1.0],
            labels=['Low', 'Medium', 'High', 'Very High']
        )
        
        self.risk_scores = results
        
        # Create GeoDataFrame with risk scores
        if isinstance(self.zip_code_data, gpd.GeoDataFrame):
            self.risk_map_gdf = gpd.GeoDataFrame(
                pd.concat([self.zip_code_data, results], axis=1)
            )
        else:
            self.risk_map_gdf = pd.concat([self.zip_code_data, results], axis=1)
        
        return results
    
    def visualize_risk_map(
        self,
        output_path: Optional[str] = None,
        risk_col: str = 'risk_score',
        cmap: str = 'YlOrRd',
        figsize: Tuple[int, int] = (12, 8),
        title: str = 'H5N1 Risk Map by Zip Code'
    ):
        """
        Create a visualization of the risk map.
        
        Parameters
        ----------
        output_path : str, optional
            Path to save the figure (e.g., 'risk_map.png')
        risk_col : str
            Column name to use for coloring
        cmap : str
            Colormap name (e.g., 'YlOrRd', 'Reds', 'viridis')
        figsize : tuple
            Figure size (width, height)
        title : str
            Plot title
        
        Returns
        -------
        matplotlib.figure.Figure
            The figure object
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("matplotlib is required for visualization. Install with: pip install matplotlib")
        
        if self.risk_map_gdf is None:
            raise ValueError("Risk scores not calculated. Use calculate_risk_scores() first.")
        
        if not isinstance(self.risk_map_gdf, gpd.GeoDataFrame):
            raise ValueError("GeoDataFrame required for visualization. Ensure geometry data is loaded.")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot the risk map
        self.risk_map_gdf.plot(
            column=risk_col,
            cmap=cmap,
            legend=True,
            ax=ax,
            edgecolor='black',
            linewidth=0.5,
            legend_kwds={'label': 'Risk Score', 'shrink': 0.8}
        )
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_axis_off()
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Risk map saved to {output_path}")
        
        return fig
    
    def create_interactive_map(
        self,
        output_path: str = 'risk_map.html',
        risk_col: str = 'risk_score',
        popup_cols: Optional[List[str]] = None
    ):
        """
        Create an interactive folium map of the risk scores.
        
        Parameters
        ----------
        output_path : str
            Path to save the HTML file
        risk_col : str
            Column name to use for coloring
        popup_cols : list, optional
            List of column names to show in popups
        
        Returns
        -------
        folium.Map
            The folium map object
        """
        try:
            import folium
            from folium import plugins
        except ImportError:
            raise ImportError("folium is required for interactive maps. Install with: pip install folium")
        
        if self.risk_map_gdf is None:
            raise ValueError("Risk scores not calculated. Use calculate_risk_scores() first.")
        
        if not isinstance(self.risk_map_gdf, gpd.GeoDataFrame):
            raise ValueError("GeoDataFrame required for interactive map. Ensure geometry data is loaded.")
        
        # Ensure CRS is WGS84 for folium
        gdf = self.risk_map_gdf.to_crs('EPSG:4326')
        
        # Calculate center of the map
        bounds = gdf.total_bounds
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        
        # Default popup columns
        if popup_cols is None:
            popup_cols = ['zip_code', 'risk_score', 'risk_category', 'population']
            popup_cols = [col for col in popup_cols if col in gdf.columns]
        
        # Add choropleth layer
        folium.Choropleth(
            geo_data=gdf,
            data=gdf,
            columns=['zip_code', risk_col],
            key_on='feature.properties.zip_code',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='H5N1 Risk Score',
            highlight=True
        ).add_to(m)
        
        # Add popup information
        for idx, row in gdf.iterrows():
            popup_text = '<br>'.join([f'<b>{col}:</b> {row[col]}' for col in popup_cols if col in row])
            
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
        
        # Save map
        m.save(output_path)
        print(f"Interactive map saved to {output_path}")
        
        return m
    
    def export_risk_data(
        self,
        output_path: str,
        format: str = 'csv'
    ):
        """
        Export risk scores and data to a file.
        
        Parameters
        ----------
        output_path : str
            Path to save the file
        format : str
            Export format: 'csv', 'geojson', or 'shp'
        """
        if self.risk_map_gdf is None:
            raise ValueError("Risk scores not calculated. Use calculate_risk_scores() first.")
        
        if format == 'csv':
            # Export without geometry for CSV
            if isinstance(self.risk_map_gdf, gpd.GeoDataFrame) and 'geometry' in self.risk_map_gdf.columns:
                df = pd.DataFrame(self.risk_map_gdf.drop(columns=['geometry']))
            else:
                df = pd.DataFrame(self.risk_map_gdf)
            df.to_csv(output_path, index=False)
        elif format == 'geojson':
            if isinstance(self.risk_map_gdf, gpd.GeoDataFrame):
                self.risk_map_gdf.to_file(output_path, driver='GeoJSON')
            else:
                raise ValueError("GeoDataFrame required for GeoJSON export.")
        elif format == 'shp':
            if isinstance(self.risk_map_gdf, gpd.GeoDataFrame):
                self.risk_map_gdf.to_file(output_path, driver='ESRI Shapefile')
            else:
                raise ValueError("GeoDataFrame required for Shapefile export.")
        else:
            raise ValueError(f"Unknown format: {format}. Use 'csv', 'geojson', or 'shp'.")
        
        print(f"Risk data exported to {output_path}")
    
    def get_high_risk_zips(
        self,
        threshold: float = 0.7,
        top_n: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Get zip codes with highest risk scores.
        
        Parameters
        ----------
        threshold : float
            Minimum risk score threshold (0-1)
        top_n : int, optional
            Return top N zip codes by risk score
        
        Returns
        -------
        pd.DataFrame
            DataFrame with high-risk zip codes
        """
        if self.risk_scores is None:
            raise ValueError("Risk scores not calculated. Use calculate_risk_scores() first.")
        
        high_risk = self.risk_scores[self.risk_scores['risk_score'] >= threshold]
        
        if top_n:
            high_risk = self.risk_scores.nlargest(top_n, 'risk_score')
        
        return high_risk.sort_values('risk_score', ascending=False)


def create_sample_data(n_zips: int = 50) -> pd.DataFrame:
    """
    Create sample zip code data for testing.
    
    Parameters
    ----------
    n_zips : int
        Number of zip codes to generate
    
    Returns
    -------
    pd.DataFrame
        Sample DataFrame with zip code data
    """
    np.random.seed(42)
    
    data = {
        'zip_code': [f'1000{i:02d}' for i in range(n_zips)],
        'population': np.random.randint(1000, 50000, n_zips),
        'area_km2': np.random.uniform(0.5, 10.0, n_zips),
        'bird_density': np.random.uniform(0, 100, n_zips),
        'water_proximity': np.random.uniform(0, 1, n_zips),
        'healthcare_capacity': np.random.uniform(0, 1, n_zips),
        'vulnerability_index': np.random.uniform(0, 1, n_zips)
    }
    
    return pd.DataFrame(data)


if __name__ == '__main__':
    # Example usage
    print("Creating sample risk map...")
    
    # Create sample data
    sample_data = create_sample_data(n_zips=50)
    
    # Initialize RiskMap
    risk_map = RiskMap(zip_code_data=sample_data)
    
    # Calculate risk scores
    risk_scores = risk_map.calculate_risk_scores()
    
    # Display summary
    print("\nRisk Score Summary:")
    print(risk_scores[['risk_score', 'risk_category']].describe())
    
    # Get high-risk zip codes
    print("\nTop 10 High-Risk Zip Codes:")
    high_risk = risk_map.get_high_risk_zips(top_n=10)
    print(high_risk[['risk_score', 'risk_category']].head(10))
    
    print("\nRisk map module ready for use!")

