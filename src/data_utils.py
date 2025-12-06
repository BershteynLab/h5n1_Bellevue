"""
Utility functions for preparing and processing data for H5N1 risk mapping.

This module provides helper functions for:
- Loading and processing NYC zip code data
- Calculating derived risk factors
- Data validation and cleaning
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from typing import Optional, Dict, List
import warnings
warnings.filterwarnings('ignore')


def load_nyc_zip_codes(file_path: str) -> gpd.GeoDataFrame:
    """
    Load NYC zip code boundaries from various formats.
    
    Parameters
    ----------
    file_path : str
        Path to zip code boundary file (GeoJSON, Shapefile, etc.)
    
    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame with zip code boundaries
    """
    gdf = gpd.read_file(file_path)
    
    # Standardize zip code column name
    zip_cols = [col for col in gdf.columns if 'zip' in col.lower() or 'postal' in col.lower()]
    if zip_cols:
        gdf = gdf.rename(columns={zip_cols[0]: 'zip_code'})
    
    # Ensure zip_code is string
    if 'zip_code' in gdf.columns:
        gdf['zip_code'] = gdf['zip_code'].astype(str).str.zfill(5)
    
    return gdf


def calculate_area_from_geometry(gdf: gpd.GeoDataFrame, crs: str = 'EPSG:3857') -> pd.Series:
    """
    Calculate area in square kilometers from geometry.
    
    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame with geometry
    crs : str
        CRS to use for area calculation (Web Mercator by default)
    
    Returns
    -------
    pd.Series
        Area in square kilometers
    """
    gdf_projected = gdf.to_crs(crs)
    area_m2 = gdf_projected.geometry.area
    area_km2 = area_m2 / 1e6
    return area_km2


def merge_population_data(
    zip_gdf: gpd.GeoDataFrame,
    population_df: pd.DataFrame,
    zip_col: str = 'zip_code',
    pop_col: str = 'population'
) -> gpd.GeoDataFrame:
    """
    Merge population data with zip code boundaries.
    
    Parameters
    ----------
    zip_gdf : gpd.GeoDataFrame
        GeoDataFrame with zip code boundaries
    population_df : pd.DataFrame
        DataFrame with population data
    zip_col : str
        Name of zip code column in population_df
    pop_col : str
        Name of population column
    
    Returns
    -------
    gpd.GeoDataFrame
        Merged GeoDataFrame
    """
    # Ensure zip codes are strings and zero-padded
    population_df = population_df.copy()
    population_df[zip_col] = population_df[zip_col].astype(str).str.zfill(5)
    
    zip_gdf = zip_gdf.copy()
    if 'zip_code' in zip_gdf.columns:
        zip_gdf['zip_code'] = zip_gdf['zip_code'].astype(str).str.zfill(5)
    
    # Merge
    merged = zip_gdf.merge(
        population_df[[zip_col, pop_col]],
        left_on='zip_code',
        right_on=zip_col,
        how='left'
    )
    
    # Fill missing values with 0
    merged[pop_col] = merged[pop_col].fillna(0)
    
    return merged


def calculate_water_proximity(
    zip_gdf: gpd.GeoDataFrame,
    water_bodies_gdf: Optional[gpd.GeoDataFrame] = None,
    method: str = 'distance'
) -> pd.Series:
    """
    Calculate proximity to water bodies for each zip code.
    
    Parameters
    ----------
    zip_gdf : gpd.GeoDataFrame
        GeoDataFrame with zip code boundaries
    water_bodies_gdf : gpd.GeoDataFrame, optional
        GeoDataFrame with water body geometries
    method : str
        Calculation method: 'distance' or 'overlap'
    
    Returns
    -------
    pd.Series
        Water proximity scores (0-1 scale)
    """
    if water_bodies_gdf is None:
        # Return default scores if no water data
        return pd.Series(0.5, index=zip_gdf.index)
    
    # Ensure same CRS
    zip_gdf = zip_gdf.to_crs('EPSG:3857')
    water_bodies = water_bodies_gdf.to_crs('EPSG:3857')
    
    if method == 'distance':
        # Calculate minimum distance to water bodies
        distances = []
        for idx, zip_geom in zip_gdf.geometry.items():
            min_dist = water_bodies.geometry.distance(zip_geom).min()
            distances.append(min_dist)
        
        distances = pd.Series(distances, index=zip_gdf.index)
        # Normalize: closer = higher score
        max_dist = distances.max()
        if max_dist > 0:
            proximity = 1 - (distances / max_dist)
        else:
            proximity = pd.Series(0.5, index=zip_gdf.index)
    
    elif method == 'overlap':
        # Calculate overlap with water bodies
        overlaps = []
        for idx, zip_geom in zip_gdf.geometry.items():
            overlap = water_bodies.geometry.intersection(zip_geom).area.sum()
            zip_area = zip_geom.area
            if zip_area > 0:
                overlap_ratio = overlap / zip_area
            else:
                overlap_ratio = 0
            overlaps.append(overlap_ratio)
        
        proximity = pd.Series(overlaps, index=zip_gdf.index)
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return proximity.fillna(0)


def calculate_bird_density_from_facilities(
    zip_gdf: gpd.GeoDataFrame,
    facilities_gdf: gpd.GeoDataFrame,
    facility_type_col: Optional[str] = None,
    capacity_col: Optional[str] = None
) -> pd.Series:
    """
    Calculate bird density based on poultry facility locations.
    
    Parameters
    ----------
    zip_gdf : gpd.GeoDataFrame
        GeoDataFrame with zip code boundaries
    facilities_gdf : gpd.GeoDataFrame
        GeoDataFrame with facility locations
    facility_type_col : str, optional
        Column name for facility type
    capacity_col : str, optional
        Column name for facility capacity/bird count
    
    Returns
    -------
    pd.Series
        Bird density scores by zip code
    """
    # Spatial join: facilities within zip codes
    joined = gpd.sjoin(facilities_gdf, zip_gdf, how='inner', predicate='within')
    
    # Group by zip code and calculate density
    if capacity_col and capacity_col in joined.columns:
        # Use capacity if available
        bird_counts = joined.groupby('zip_code')[capacity_col].sum()
    else:
        # Count facilities
        bird_counts = joined.groupby('zip_code').size()
    
    # Merge back to zip codes
    bird_density = zip_gdf['zip_code'].map(bird_counts).fillna(0)
    
    # Normalize by area if available
    if 'area_km2' in zip_gdf.columns:
        bird_density = bird_density / zip_gdf['area_km2']
        bird_density = bird_density.fillna(0)
    
    return bird_density


def validate_risk_data(df: pd.DataFrame, required_cols: List[str]) -> Dict[str, bool]:
    """
    Validate that required columns exist and have valid data.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate
    required_cols : list
        List of required column names
    
    Returns
    -------
    dict
        Dictionary with validation results
    """
    results = {}
    
    for col in required_cols:
        if col not in df.columns:
            results[col] = False
            print(f"WARNING: Required column '{col}' not found")
        elif df[col].isna().all():
            results[col] = False
            print(f"WARNING: Column '{col}' has no valid data")
        else:
            results[col] = True
    
    return results


def prepare_risk_data(
    zip_gdf: gpd.GeoDataFrame,
    population_df: Optional[pd.DataFrame] = None,
    facilities_gdf: Optional[gpd.GeoDataFrame] = None,
    water_bodies_gdf: Optional[gpd.GeoDataFrame] = None
) -> gpd.GeoDataFrame:
    """
    Prepare a complete dataset for risk mapping by merging all data sources.
    
    Parameters
    ----------
    zip_gdf : gpd.GeoDataFrame
        Base zip code boundaries
    population_df : pd.DataFrame, optional
        Population data
    facilities_gdf : gpd.GeoDataFrame, optional
        Poultry facility locations
    water_bodies_gdf : gpd.GeoDataFrame, optional
        Water body geometries
    
    Returns
    -------
    gpd.GeoDataFrame
        Prepared dataset ready for risk mapping
    """
    result = zip_gdf.copy()
    
    # Calculate area if not present
    if 'area_km2' not in result.columns:
        result['area_km2'] = calculate_area_from_geometry(result)
    
    # Merge population data
    if population_df is not None:
        result = merge_population_data(result, population_df)
    elif 'population' not in result.columns:
        print("WARNING: No population data provided")
        result['population'] = 0
    
    # Calculate bird density
    if facilities_gdf is not None:
        result['bird_density'] = calculate_bird_density_from_facilities(
            result, facilities_gdf
        )
    elif 'bird_density' not in result.columns:
        print("WARNING: No bird density data provided")
        result['bird_density'] = 0
    
    # Calculate water proximity
    if water_bodies_gdf is not None:
        result['water_proximity'] = calculate_water_proximity(
            result, water_bodies_gdf
        )
    elif 'water_proximity' not in result.columns:
        print("WARNING: No water proximity data provided")
        result['water_proximity'] = 0
    
    # Add default values for optional columns if missing
    if 'healthcare_capacity' not in result.columns:
        result['healthcare_capacity'] = 0.5  # Default medium capacity
    if 'vulnerability_index' not in result.columns:
        result['vulnerability_index'] = 0.5  # Default medium vulnerability
    
    return result


