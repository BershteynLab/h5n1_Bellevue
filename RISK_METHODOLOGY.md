# H5N1 Risk Mapping Methodology

This document explains the methodology used to calculate H5N1 (Avian Influenza) risk scores for NYC zip codes. The approach combines multiple epidemiological risk factors into a composite risk score that identifies areas most vulnerable to H5N1 outbreaks.

## Data Sources Summary

All risk factors use **real-world data** from authoritative sources:

| Risk Factor | Data Source | Coverage | File Location |
|------------|-------------|----------|---------------|
| **Population Density** | 2020 US Census Decennial Data | 100% (178 zip codes) | `data/raw/DECENNIALDHC2020.P1-Data.csv` |
| **Zip Code Boundaries** | NYC Modified ZCTA (2025) | 100% | `data/raw/Modified_Zip_Code_Tabulation_Areas_(MODZCTA)_20251205.csv` |
| **Poultry Density** | USGS Poultry Susceptibility Raster (2022) | 95% (169/178 zip codes) | `data/raw/Poultry.tif` |
| **Water Proximity** | USGS National Hydrography Dataset (NHD) | 100% | `data/raw/Shape/NHDWaterbody.shp`, `NHDFlowline.shp`, `NHDArea.shp` |
| **Healthcare Capacity** | CDC SVI - Healthcare Access Indicator | 99.4% (177/178 zip codes) | `data/raw/NewYork_ZCTA.csv` (EP_UNINSUR) |
| **Vulnerability Index** | CDC Social Vulnerability Index (2022) | 99.4% (177/178 zip codes) | `data/raw/NewYork_ZCTA.csv` (RPL_THEMES) |

**Processed Data:** All data is integrated into `data/processed/nyc_zip_codes_with_water_with_svi.geojson`

**Data Quality:** All 5 risk factors (100% of risk score) use real data from authoritative sources.

## Risk Calculation Framework

### Composite Risk Score

Risk scores are calculated as a weighted sum of normalized risk factors:

```
Risk Score = Σ (Normalized_Factor_i × Weight_i)
```

Where:
- Each factor is normalized to a 0-1 scale
- Weights sum to 1.0
- Final risk scores range from 0 (lowest risk) to 1 (highest risk)

### Risk Categories

- **Low**: 0.0 - 0.25
- **Medium**: 0.25 - 0.5
- **High**: 0.5 - 0.75
- **Very High**: 0.75 - 1.0

**References:**
- Si Y, de Boer WF, Gong P (2013) Different Environmental Drivers of Highly Pathogenic Avian Influenza H5N1 Outbreaks in Poultry and Wild Birds. PLoS ONE 8(1): e53362. https://doi.org/10.1371/journal.pone.0053362
- Prosser DJ, Hungerford LL, Erwin RM, Ottinger MA, Takekawa JY, Ellis EC. Mapping avian influenza transmission risk at the interface of domestic poultry and wild birds. Front Public Health. 2013 Aug 30;1:28. doi: 10.3389/fpubh.2013.00028. 
- Yamaguchi E, Hayama Y, Kondo S, Yamamoto T. Risk factors for highly pathogenic avian influenza outbreaks in Japan during 2022-2023 season identified by additive Bayesian network modeling. Sci Rep. 2025 Jul 23;15(1):26739. doi: 10.1038/s41598-025-13003-5. 
- Fang L-Q, de Vlas SJ, Liang S, Looman CWN, Gong P, Xu B, et al. (2008) Environmental Factors Contributing to the Spread of H5N1 Avian Influenza in Mainland China. PLoS ONE 3(5): e2268. https://doi.org/10.1371/journal.pone.0002268

---

## Risk Factors and Rationale

### 1. Population Density (Weight: 25%)

**Why it matters:**
- H5N1 can transmit from birds to humans (zoonotic transmission)
- Higher population density increases:
  - Contact rates between individuals
  - Potential for human-to-human transmission (if the virus mutates)
  - Speed of outbreak spread
  - Healthcare system burden

**Epidemiological Evidence:**
- Urban areas with high population density have shown faster disease spread in past pandemics
- Contact networks are denser in urban settings, facilitating transmission
- NYC's dense population makes it particularly vulnerable to rapid spread

**Calculation:**
- Population density = Total population / Area (km²)
- Normalized using min-max scaling

**Data Source:**
- **2020 US Census Decennial Data** (`DECENNIALDHC2020.P1-Data.csv`)
  - Official population counts by ZCTA
  - Total population (P1_001N) for each zip code
- **NYC Modified ZCTA Boundaries** (`Modified_Zip_Code_Tabulation_Areas_(MODZCTA)_20251205.csv`)
  - Geographic boundaries for 178 NYC zip codes
  - Includes geometry for area calculations

**References:**
- Reyes R, Ahn R, Thurber K, Burke TF. Urbanization and Infectious Diseases: General Principles, Historical Perspectives, and Contemporary Challenges. Challenges in Infectious Diseases. 2012 May 19:123–46. doi: 10.1007/978-1-4614-4496-1_4.
- Hazarie, S., Soriano-Paños, D., Arenas, A. et al. Interplay between population density and mobility in determining the spread of epidemics in cities. Commun Phys 4, 191 (2021). https://doi.org/10.1038/s42005-021-00679-0


---

### 2. Bird/Poultry Density (Weight: 45%)  **HIGHEST PRIORITY**

**Why it matters:**
- **H5N1 is an avian influenza virus** - birds are the primary reservoir
- Poultry facilities are the main interface between wild birds and humans
- Higher poultry density = more opportunities for:
  - Wild bird → poultry transmission
  - Poultry → human transmission
  - Outbreak amplification

**Epidemiological Evidence:**
- Most H5N1 human cases have been linked to direct contact with infected poultry
- Poultry farms serve as "mixing vessels" where viruses can reassort
- The 2022-2023 H5N1 outbreak in the US was primarily driven by wild bird → poultry transmission
- Studies show poultry density is the strongest predictor of avian influenza risk

**Why Highest Weight:**
- This is the **primary risk factor** for H5N1 specifically
- Unlike general respiratory diseases, H5N1 requires bird-human interface
- Without poultry/bird contact, human risk is minimal
- This factor distinguishes H5N1 risk from other infectious diseases

**Calculation:**
- Uses USGS Poultry Susceptibility Index
- Represents cumulative susceptibility based on:
  - Poultry farm locations
  - Farm types (commercial vs. backyard)
  - Species (chicken vs. turkey)
  - Commodity type (broilers, layers, pullets)
  - Biosecurity measures
- Values range from 1.0 to 3,041 (higher = more susceptible)

**Data Source:**
- **USGS Poultry Susceptibility Raster** (`Poultry.tif`, 2022)
  - Based on USDA Hybrid Poultry Model
  - Raster values extracted for each zip code polygon
  - DOI: 10.5066/P94BT78I
  - Values range from 1.0 to 3,041 (higher = more susceptible)
  - Coverage: 169/178 zip codes (95%)

**References:**
- Keawcharoen J, van den Broek J, Bouma A, Tiensin T, Osterhaus AD, Heesterbeek H. Wild birds and increased transmission of highly pathogenic avian influenza (H5N1) among poultry, Thailand. Emerg Infect Dis. 2011 Jun;17(6):1016-22. doi: 10.3201/eid/1706.100880. 
- Jindal M, Stone H, Lim S, MacIntyre CR. A Geospatial Perspective Toward the Role of Wild Bird Migrations and Global Poultry Trade in the Spread of Highly Pathogenic Avian Influenza H5N1. Geohealth. 2025 Mar 25;9(3):e2024GH001296. doi: 10.1029/2024GH001296. 
- Gilbert, M., Golding, N., Zhou, H. et al. Predicting the risk of avian influenza A H7N9 infection in live-poultry markets across Asia. Nat Commun 5, 4116 (2014). https://doi.org/10.1038/ncomms5116
- Velkers FC, Manders TTM, Vernooij JCM, Stahl J, Slaterus R, Stegeman JA. Association of wild bird densities around poultry farms with the risk of highly pathogenic avian influenza virus subtype H5N8 outbreaks in the Netherlands, 2016. Transbound Emerg Dis. 2021 Jan;68(1):76-87. doi: 10.1111/tbed.13595. Epub 2020 May 18.
---

### 3. Water Proximity (Weight: 15%)

**Why it matters:**
- Wild waterfowl (ducks, geese) are natural reservoirs of H5N1
- Water bodies serve as:
  - Migration stopover points
  - Breeding and feeding grounds
  - Areas where wild birds congregate
- Proximity to water = proximity to potential virus sources

**Epidemiological Evidence:**
- H5N1 is maintained in wild bird populations, especially waterfowl
- Outbreaks often correlate with bird migration routes
- Water bodies create "hotspots" where wild birds and poultry may interact
- Coastal areas and wetlands are particularly important for bird migration

**Calculation:**
- Distance to nearest water body (coastline, rivers, lakes, wetlands)
- Closer proximity = higher risk
- Calculated from zip code centroid to nearest water feature
- Normalized to 0-1 scale (closer = higher risk)

**Data Source:**
- **USGS National Hydrography Dataset (NHD)**
  - `NHDWaterbody.shp` - Lakes, ponds, reservoirs
  - `NHDFlowline.shp` - Rivers, streams, canals
  - `NHDArea.shp` - Water area polygons
  - Filtered to NYC bounding box for efficiency
  - Coverage: 100% (all 178 zip codes)

**References:**
- Hill SC, Lee YJ, Song BM, Kang HM, Lee EK, Hanna A, Gilbert M, Brown IH, Pybus OG. Wild waterfowl migration and domestic duck density shape the epidemiology of highly pathogenic H5N8 influenza in the Republic of Korea. Infect Genet Evol. 2015 Aug;34:267-77. doi: 10.1016/j.meegid.2015.06.014. Epub 2015 Jun 12.
- Ahmad S, Koh K, Yoo D, Suh G, Lee J, Lee CM. Impact of inland waters on highly pathogenic avian influenza outbreaks in neighboring poultry farms in South Korea. J Vet Sci. 2022 Feb;23(3):e36. https://doi.org/10.4142/jvs.21278


---

### 4. Healthcare Capacity (Weight: 10%)

**Why it matters:**
- H5N1 has high case fatality rate (~50% in humans)
- Requires intensive care and specialized treatment
- Limited healthcare capacity means:
  - Delayed treatment
  - Inability to handle surge capacity
  - Higher mortality rates
  - Slower outbreak containment

**Epidemiological Evidence:**
- Healthcare system capacity was a critical factor in COVID-19 outcomes
- H5N1 cases often require ICU care and mechanical ventilation
- Areas with better healthcare infrastructure can:
  - Detect cases earlier
  - Provide better treatment
  - Reduce transmission through isolation

**Calculation:**
- Uses healthcare access indicator from CDC SVI
- Based on percentage uninsured population (`EP_UNINSUR`)
- Inverted: Lower uninsured rate = Better healthcare access = Lower risk
- Normalized to 0-1 scale (1.0 = best access, 0.0 = worst access)
- Range: 0.43 - 1.00 (mean: 0.94)

**Data Source:**
- **CDC Social Vulnerability Index (SVI) 2022**
  - `NewYork_ZCTA.csv` - Healthcare access indicator (`EP_UNINSUR`)
  - Percentage of population without health insurance
  - Coverage: 177/178 zip codes (99.4%)
  - Note: This is a proxy for healthcare capacity; direct hospital data could be added in the future


**References:**
- Richardson S, Hirsch JS, Narasimhan M, et al. Presenting Characteristics, Comorbidities, and Outcomes Among 5700 Patients Hospitalized With COVID-19 in the New York City Area. JAMA. 2020;323(20):2052–2059. doi:10.1001/jama.2020.6775
- Jarrett M, Garrick R, Gaeta A, Lombardi D, Mayo R, McNulty P, Panzer R, Krahn WD. Pandemic Preparedness: COVID-19 Lessons Learned in New York's Hospitals. Jt Comm J Qual Patient Saf. 2022 Sep;48(9):475-491. doi: 10.1016/j.jcjq.2022.06.002. Epub 2022 Jun 10. 
- Wouter S. Hoogenboom, Antoine Pham, Harnadar Anand, Roman Fleysher, Alexandra Buczek, Selvin Soby, Parsa Mirhaji, Judy Yee, Tim Q. Duong, Clinical characteristics of the first and second COVID-19 waves in the Bronx, New York: A retrospective cohort study, The Lancet Regional Health - Americas, Volume 3, 2021, 100041, ISSN 2667-193X, https://doi.org/10.1016/j.lana.2021.100041.
- Schaye V. E., Reich J. A., Bosworth B. P., Stern D. T., Volpicelli F., Shapiro N. M., Hauck K. D., Fagan I. M., Villagomez S. M., Uppal A., Sauthoff H., LoCurcio M., Cocks P. M., Bails D. B. (2020). Collaborating Across Private, Public, Community, and Federal Hospital Systems: Lessons Learned from the Covid-19 Pandemic Response in NYC. NEJM Catalyst Innovations in Care Delivery, 1(6). doi:10.1056/CAT.20.0343  


---

### 5. Socioeconomic Vulnerability (Weight: 5%)

**Why it matters:**
- Vulnerable populations may have:
  - Limited access to healthcare
  - Higher exposure risks (essential workers, crowded housing)
  - Reduced ability to follow public health measures
  - Underlying health conditions
- These factors can amplify outbreak impact

**Epidemiological Evidence:**
- COVID-19 showed clear disparities in outcomes by socioeconomic status
- Vulnerable communities often have:
  - Higher rates of comorbidities
  - Limited healthcare access
  - Denser living conditions
  - Essential workers who cannot isolate

**Calculation:**
- Uses CDC Social Vulnerability Index (SVI) overall rank (`RPL_THEMES`)
- Normalized to 0-1 scale (higher = more vulnerable)
- Combines four themes:
  - Theme 1: Socioeconomic status
  - Theme 2: Household composition
  - Theme 3: Minority status & language
  - Theme 4: Housing type & transportation
- Range: 0.001 - 0.010 (mean: 0.008)

**Data Source:**
- **CDC Social Vulnerability Index (SVI) 2022**
  - `NewYork_ZCTA.csv` - Overall vulnerability rank (`RPL_THEMES`)
  - Rank percentile (0-100) normalized to 0-1
  - Coverage: 177/178 zip codes (99.4%)

**References:**
- Tosam MJ, Ambe JR, Chi PC. Global Emerging Pathogens, Poverty and Vulnerability: An Ethical Analysis. Socio-cultural Dimensions of Emerging Infectious Diseases in Africa. 2019 Mar 20:243–53. doi: 10.1007/978-3-030-17474-3_18. 
- Yuan B, Huang X, Li J, He L. Socioeconomic disadvantages and vulnerability to the pandemic among children and youth: A macro-level investigation of American counties. Child Youth Serv Rev. 2022 May;136:106429. doi: 10.1016/j.childyouth.2022.106429. Epub 2022 Feb 23.
- Mongin D, Cullati S, Kelly-Irving M, Rosselet M, Regard S, Courvoisier DS; Covid-SMC Study Group. Neighbourhood socio-economic vulnerability and access to COVID-19 healthcare during the first two waves of the pandemic in Geneva, Switzerland: A gender perspective. EClinicalMedicine. 2022 Mar 28;46:101352. doi: 10.1016/j.eclinm.2022.101352. 

---


## Normalization Methods

### Min-Max Normalization (Default)

```
Normalized = (Value - Min) / (Max - Min)
```

**Advantages:**
- Preserves relative relationships
- Easy to interpret (0-1 scale)
- Works well with bounded data

**Used for:**
- Population density
- Bird density
- Water proximity
- Healthcare capacity
- Vulnerability index


---

### Limitations

1. **Temporal Data:**
   - Current data is a snapshot (2020-2022)
   - No time-series analysis
   - Cannot model temporal dynamics

2. **Missing Factors:**
   - Bird migration patterns (seasonal)
   - Poultry facility biosecurity levels
   - Human behavior patterns
   - Climate factors

3. **Spatial Resolution:**
   - Zip code level may mask local variations
   - Large zip codes may average out hotspots
   - Small zip codes may have sparse data

4. **Assumptions:**
   - Linear relationships between factors
   - Additive risk model
   - Static weights (not scenario-dependent)

---

## Validation and Calibration

### Validation Approaches

1. **Historical Data:**
   - Compare with past H5N1 outbreaks (if available)
   - Validate against known high-risk areas
   - Check against expert assessments

2. **Sensitivity Analysis:**
   - Test different weight combinations
   - Assess impact of missing data
   - Evaluate normalization methods

3. **Expert Review:**
   - Bellevue Hospital Critical Care Unit review
   - Public health expert consultation
   - Epidemiological validation

### Calibration

Risk scores can be calibrated by:
- Adjusting weights based on outbreak data
- Incorporating case fatality rates
- Adding transmission parameters (R0)
- Including intervention effectiveness

---

## Scenario Modeling

The framework supports scenario analysis:

### Different R0 Values
- Low R0 (1.2-1.5): Endemic spread
- Medium R0 (1.5-2.0): Moderate outbreak
- High R0 (2.0+): Pandemic potential

### Intervention Scenarios
- Poultry culling effectiveness
- Biosecurity improvements
- Human vaccination coverage
- Social distancing measures

### Natural History Variations
- Incubation period
- Infectious period
- Case fatality rate
- Asymptomatic transmission

---
