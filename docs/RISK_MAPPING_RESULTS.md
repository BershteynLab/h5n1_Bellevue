# H5N1 Risk Mapping Results - NYC

## Overview

Risk mapping has been completed for NYC zip codes using real data including:
- Population data (2020 Census) https://data.census.gov/all?g=040XX00US36$8600000
- Poultry susceptibility data (USGS raster) https://www.sciencebase.gov/catalog/item/62e2c58cd34e394b65364ed5
- Zip code boundaries https://data.cityofnewyork.us/Health/Modified-Zip-Code-Tabulation-Areas-MODZCTA-Map/5fzm-kpwv

## Risk Score Summary

- **Total zip codes analyzed:** 178
- **Risk score range:** 0.04 - 0.58
- **Mean risk score:** 0.40
- **Median risk score:** 0.40

## Risk Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| Low | 21 | 11.8% |
| Medium | 133 | 74.7% |
| High | 24 | 13.5% |
| Very High | 0 | 0% |

## High-Risk Areas

The top high-risk zip codes are primarily in the **Bronx** area, which shows:
- Highest poultry susceptibility scores (3,041 - maximum value)
- High population density
- Combination of factors leading to elevated H5N1 risk

### Key Findings

1. **Poultry Susceptibility:**
   - 169 out of 178 zip codes have poultry data
   - Values range from 0 to 3,041
   - Bronx zip codes (10451-10460) show maximum susceptibility

2. **Risk Factors:**
   - Population density varies significantly across NYC
   - Poultry susceptibility is the dominant risk factor in high-risk areas
   - Most zip codes fall in the "Medium" risk category

3. **Geographic Patterns:**
   - Bronx shows highest risk concentrations
   - Risk is distributed across all boroughs
   - No zip codes reached "Very High" category with current data

## Files Generated

### Data Files
- `nyc_zip_codes_with_poultry.geojson` - Complete dataset with poultry data
- `nyc_zip_codes_with_poultry.csv` - CSV version
- `nyc_risk_scores.csv` - Risk scores and categories

### Visualizations
- `poultry_susceptibility_map.png` - Static map of poultry susceptibility
- `poultry_susceptibility_map.html` - Interactive map of poultry data
- `nyc_risk_map.png` - Static map of H5N1 risk scores
- `nyc_risk_map.html` - Interactive map of risk scores

## Risk Calculation Methodology

Risk scores are calculated using weighted factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Population Density | 25% | Human contact risk |
| Bird/Poultry Density | 45% | Primary H5N1 reservoir (highest weight) |
| Water Proximity | 15% | Wild bird habitats |
| Healthcare Capacity | 10% | Response capability |
| Vulnerability Index | 5% | Socioeconomic factors |

**Note:** Water proximity and healthcare capacity use default values (0.5) as actual data is not yet available.

## Recommendations

### Immediate Actions
1. **Review high-risk zip codes** - Focus on Bronx areas with maximum poultry susceptibility
2. **Validate poultry data** - Verify the high susceptibility values in Bronx zip codes
3. **Add missing data:**
   - Water bodies/coastline data for wild bird proximity
   - Healthcare capacity data (hospital locations, ICU beds)
   - Socioeconomic vulnerability indices

### Next Steps
1. **Refine risk weights** - Adjust based on epidemiological evidence
2. **Temporal analysis** - Add time-series data if available
3. **Scenario modeling** - Test different R0 values and intervention strategies
4. **Validation** - Compare with historical outbreak data if available

## Data Quality Notes

- ✅ Population data: Complete (2020 Census)
- ✅ Poultry data: 169/178 zip codes (95% coverage)
- ⚠️ Water proximity: Using default values (needs real data)
- ⚠️ Healthcare capacity: Using default values (needs real data)
- ⚠️ Vulnerability index: Using default values (needs real data)

## Usage

To view the results:
1. Open `data/processed/nyc_risk_map.html` in a web browser for interactive exploration
2. Review `data/processed/nyc_risk_scores.csv` for detailed data
3. Check `data/processed/poultry_susceptibility_map.html` for poultry data visualization

## Scripts Used

- `src/process_nyc_data.py` - Processed zip code and population data
- `src/process_poultry_raster.py` - Extracted poultry susceptibility from raster
- `src/example_risk_map_real_data.py` - Calculated risk scores
- `src/visualize_poultry.py` - Created visualizations

