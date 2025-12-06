# Quick Start Guide - H5N1 Risk Mapping

## Installation

### Using Conda (Recommended)

Activate the conda environment:

```bash
conda activate h5n1_bellevue
```

All dependencies are already installed! If you need to reinstall:

```bash
conda install -c conda-forge geopandas pandas numpy matplotlib folium
```

### Using venv (Alternative)

If you prefer the standard Python venv:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Basic Usage

### 1. Using Sample Data (for testing)

```python
from src.risk_map import RiskMap, create_sample_data

# Create sample data
data = create_sample_data(n_zips=50)

# Initialize and calculate risk
risk_map = RiskMap(zip_code_data=data)
risk_scores = risk_map.calculate_risk_scores()

# View results
print(risk_scores.head())
high_risk = risk_map.get_high_risk_zips(top_n=10)
print(high_risk)
```

### 2. Using Real Data

```python
from src.risk_map import RiskMap
import pandas as pd

# Load your data
data = pd.read_csv('data/raw/zip_codes.csv')

# Initialize with custom weights
custom_weights = {
    'population_density': 0.25,
    'bird_density': 0.45,  # Higher weight for H5N1
    'water_proximity': 0.20,
    'healthcare_capacity': 0.05,
    'vulnerability_index': 0.05
}

risk_map = RiskMap(zip_code_data=data, risk_weights=custom_weights)
risk_scores = risk_map.calculate_risk_scores()

# Export results
risk_map.export_risk_data('data/processed/risk_scores.csv')
```

### 3. With Geospatial Data (for maps)

```python
from src.risk_map import RiskMap

# Load GeoJSON or Shapefile
risk_map = RiskMap()
gdf = risk_map.load_zip_code_data('data/raw/nyc_zip_codes.geojson')

# Calculate risk
risk_scores = risk_map.calculate_risk_scores()

# Create visualizations
risk_map.visualize_risk_map(output_path='output/risk_map.png')
risk_map.create_interactive_map(output_path='output/risk_map.html')
```

## Running the Example

```bash
python src/example_risk_map.py
```

## Data Format

Your CSV should have these columns:

**Required:**
- `zip_code`: Zip code (e.g., "10001")
- `population`: Population count
- `area_km2`: Area in square kilometers

**Optional (for better risk assessment):**
- `bird_density`: Bird/poultry density
- `water_proximity`: Proximity to water (0-1)
- `healthcare_capacity`: Healthcare capacity (0-1)
- `vulnerability_index`: Vulnerability index (0-1)

## Next Steps

1. Collect NYC zip code data with population and area
2. Gather bird/poultry facility data
3. Obtain water body/coastline data for proximity calculations
4. Run risk calculations
5. Visualize and analyze results

See `src/README_risk_map.md` for detailed documentation.

