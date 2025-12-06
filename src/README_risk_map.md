# Spatial Risk Map Module for H5N1

This module provides functionality to create spatial risk maps for H5N1 outbreaks at the zip code level.

## Overview

The `RiskMap` class calculates composite risk scores for zip codes based on multiple risk factors relevant to H5N1 transmission:

- **Population Density**: Higher population density increases contact rates
- **Bird/Poultry Density**: Primary reservoir for H5N1
- **Water Proximity**: Wild bird habitats (migration routes)
- **Healthcare Capacity**: Ability to respond to outbreaks
- **Socioeconomic Vulnerability**: Factors affecting outbreak response

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from risk_map import RiskMap
import pandas as pd

# Load your zip code data
data = pd.read_csv('data/raw/zip_codes.csv')

# Initialize RiskMap
risk_map = RiskMap(zip_code_data=data)

# Calculate risk scores
risk_scores = risk_map.calculate_risk_scores()

# Get high-risk zip codes
high_risk = risk_map.get_high_risk_zips(top_n=10)

# Export results
risk_map.export_risk_data('output/risk_scores.csv', format='csv')
```

### With Custom Risk Weights

```python
# Customize risk factor weights
custom_weights = {
    'population_density': 0.25,
    'bird_density': 0.45,  # Higher weight for avian flu
    'water_proximity': 0.20,
    'healthcare_capacity': 0.05,
    'vulnerability_index': 0.05
}

risk_map = RiskMap(
    zip_code_data=data,
    risk_weights=custom_weights
)
```

### Loading Geospatial Data

```python
# Load from GeoJSON
risk_map = RiskMap()
gdf = risk_map.load_zip_code_data('data/raw/nyc_zip_codes.geojson')

# Calculate risk scores
risk_scores = risk_map.calculate_risk_scores()

# Create visualizations
risk_map.visualize_risk_map(output_path='output/risk_map.png')
risk_map.create_interactive_map(output_path='output/risk_map.html')
```

## Data Requirements

Your zip code data should include the following columns:

### Required Columns
- `zip_code`: Zip code identifier
- `population`: Population count
- `area_km2`: Area in square kilometers (or geometry for automatic calculation)

### Optional Columns
- `bird_density`: Density of birds/poultry
- `water_proximity`: Proximity to water bodies (0-1 scale)
- `healthcare_capacity`: Healthcare capacity index (0-1 scale)
- `vulnerability_index`: Socioeconomic vulnerability index (0-1 scale)
- `geometry`: GeoSeries geometry (for spatial visualizations)

## Risk Score Calculation

Risk scores are calculated as a weighted sum of normalized risk factors:

```
risk_score = Σ (normalized_factor_i × weight_i)
```

Each factor is normalized to a 0-1 scale using min-max normalization. Risk scores range from 0 (lowest risk) to 1 (highest risk).

Risk categories:
- **Low**: 0.0 - 0.25
- **Medium**: 0.25 - 0.5
- **High**: 0.5 - 0.75
- **Very High**: 0.75 - 1.0

## Methods

### `calculate_risk_scores()`
Calculates composite risk scores for all zip codes.

### `get_high_risk_zips(threshold, top_n)`
Returns zip codes with risk scores above a threshold or top N zip codes.

### `visualize_risk_map(output_path, ...)`
Creates a static choropleth map visualization (requires geometry data).

### `create_interactive_map(output_path, ...)`
Creates an interactive Folium map (requires geometry data).

### `export_risk_data(output_path, format)`
Exports risk scores to CSV, GeoJSON, or Shapefile format.

## Example Workflow

1. **Prepare Data**: Collect zip code data with population, area, and risk factors
2. **Load Data**: Use `load_zip_code_data()` or pass DataFrame to `RiskMap()`
3. **Calculate Risk**: Call `calculate_risk_scores()`
4. **Analyze**: Use `get_high_risk_zips()` to identify priority areas
5. **Visualize**: Create maps for reporting and communication
6. **Export**: Save results for further analysis or integration

## Integration with NYC Data

For NYC-specific implementation, you'll need:

1. **Zip Code Boundaries**: 
   - NYC Open Data: https://data.cityofnewyork.us/Business/Zip-Code-Boundaries/i8iw-xf4u
   - Or US Census Bureau TIGER/Line files

2. **Population Data**:
   - US Census Bureau ACS data
   - NYC Department of City Planning

3. **Bird/Poultry Data**:
   - USDA poultry facility locations
   - Wild bird migration data
   - Waterfowl habitat maps

4. **Healthcare Capacity**:
   - Hospital locations and bed counts
   - ICU capacity data

5. **Socioeconomic Data**:
   - CDC Social Vulnerability Index
   - NYC Department of Health data

## Future Enhancements

- Temporal risk mapping (risk over time/stages of outbreak)
- Integration with epidemiological models
- Real-time data updates
- Scenario modeling with different parameter sets
- API endpoints for rapid deployment

## References

- H5N1 epidemiological parameters from literature review
- Spatial risk assessment methodologies
- NYC public health data sources


