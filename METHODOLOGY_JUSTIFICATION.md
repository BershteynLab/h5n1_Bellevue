# Methodology Justification: H5N1 Risk Mapping Components and Weights

## Executive Summary

This document explains the rationale for selecting the 5 risk components and their specific weights in our H5N1 risk mapping framework. It distinguishes between:
- **Literature-supported components**: Factors with direct evidence from H5N1/avian influenza studies
- **Project-specific decisions**: Choices made based on available data, project goals, and practical considerations

## The Weighted Sum Approach: Standard Methodology

The weighted sum approach (combining multiple risk factors with weights) is a standard methodology in:
- Spatial epidemiology
- Risk assessment frameworks
- Composite indices (e.g., Social Vulnerability Index, Environmental Health Indices)

**This is not novel** - it's an established approach. What is project-specific is the **selection of components and their weights**.

---

## Component Selection: Literature Support vs. Project Decisions

### 1. Bird/Poultry Density (Weight: 45%) ✓ **STRONGLY SUPPORTED**

**Literature Evidence:**
- **Keawcharoen et al. (2011)**: Wild birds and increased transmission of H5N1 among poultry in Thailand
- **Velkers et al. (2021)**: Association of wild bird densities around poultry farms with H5N8 outbreaks in Netherlands
- **Gilbert et al. (2014)**: Poultry market risk for avian influenza A H7N9
- **Jindal et al. (2025)**: Geospatial perspective on wild bird migrations and global poultry trade in H5N1 spread

**Consensus**: Poultry density is the **strongest predictor** of avian influenza risk. Most human H5N1 cases are linked to direct poultry contact.

**Why 45% weight**: This is the primary distinguishing factor for H5N1. Without bird-human interface, human risk is minimal. This weight reflects the literature consensus that poultry is the most important risk factor.

---

### 2. Water Proximity (Weight: 15%) ✓ **SUPPORTED**

**Literature Evidence:**
- **Hill et al. (2015)**: Wild waterfowl migration and domestic duck density shape H5N8 epidemiology in South Korea
- **Ahmad et al. (2022)**: Impact of inland waters on HPAI outbreaks in neighboring poultry farms in South Korea
- **Si et al. (2013)**: Environmental drivers of H5N1 outbreaks include water bodies as wild bird habitats

**Consensus**: Water bodies serve as wild bird habitats, migration stopover points, and areas where wild birds congregate. Proximity to water = proximity to potential virus sources.

**Why 15% weight**: Important for early outbreak risk (wild bird introduction), but secondary to poultry density for sustained transmission.

---

### 3. Population Density (Weight: 25%) ⚠️ **GENERAL PRINCIPLE, NOT H5N1-SPECIFIC**

**Literature Evidence:**
- **Reyes et al. (2012)**: Urbanization and infectious diseases - general principles
- **Hazarie et al. (2021)**: Population density and mobility in epidemic spread - general principles
- **Note**: These are general infectious disease principles, not H5N1-specific studies

**Why included**: Higher population density increases:
- Contact rates between individuals
- Potential for human-to-human transmission (if virus mutates)
- Speed of outbreak spread
- Healthcare system burden

**Why 25% weight**: Important for human transmission potential, but less critical than bird contact for initial H5N1 risk. Acknowledges that H5N1 is primarily zoonotic, not primarily human-to-human.

**Limitation**: As your boss noted, population density alone may not predict R0 well in NYC due to high-rise buildings with HVAC systems. This is a known limitation we should address.

---

### 4. Healthcare Capacity (Weight: 10%) ⚠️ **EXTRAPOLATED FROM COVID-19**

**Literature Evidence:**
- **Richardson et al. (2020)**: Healthcare capacity in NYC COVID-19 outcomes
- **Jarrett et al. (2022)**: Pandemic preparedness lessons from COVID-19 in NYC hospitals
- **Note**: This evidence is from COVID-19, not H5N1. H5N1 has different transmission dynamics but similar healthcare burden concerns.

**Why included**: 
- H5N1 has high case fatality rate (~50% in humans)
- Requires intensive care and specialized treatment
- Limited healthcare capacity = delayed treatment, higher mortality, slower containment

**Why 10% weight**: Important for outcome severity and long-term burden, but less critical for initial outbreak detection. Reflects that this is about response capacity, not transmission risk.

**Limitation**: This is extrapolated from COVID-19 evidence, not directly from H5N1 studies.

---

### 5. Social Vulnerability (Weight: 5%) ⚠️ **EXTRAPOLATED FROM COVID-19**

**Literature Evidence:**
- **Yuan et al. (2022)**: Socioeconomic disadvantages and pandemic vulnerability
- **Mongin et al. (2022)**: Neighbourhood socio-economic vulnerability and COVID-19 healthcare access
- **Note**: This evidence is from COVID-19, not H5N1.

**Why included**:
- Vulnerable populations may have limited healthcare access
- Higher exposure risks (essential workers, crowded housing)
- Reduced ability to follow public health measures
- Underlying health conditions

**Why 5% weight**: Important for understanding disparate impacts and long-term burden, but less critical for initial transmission risk. Lowest weight reflects that this is more about equity and outcomes than transmission.

**Limitation**: This is extrapolated from COVID-19 evidence, not directly from H5N1 studies.

---

## Weight Selection Rationale

### Why These Specific Weights?

The weight distribution reflects:

1. **H5N1-specific epidemiology** (45% + 15% = 60%):
   - Bird/poultry density (45%): Primary transmission interface
   - Water proximity (15%): Wild bird introduction risk
   - **Total: 60% for early outbreak/transmission risk**

2. **Human transmission and burden** (25% + 10% + 5% = 40%):
   - Population density (25%): Human-to-human transmission potential
   - Healthcare capacity (10%): Response and outcome severity
   - Social vulnerability (5%): Disparate impacts
   - **Total: 40% for long-term burden and human factors**

### Decision Process

The weights were determined through:
1. **Literature review**: Emphasis on poultry as primary risk factor
2. **Available data**: What data we could obtain for NYC zip codes
3. **Project goals**: Balance between early outbreak detection vs. long-term burden
4. **Expert consultation**: Input from Bellevue Hospital Critical Care Unit (informal)
5. **Pragmatic considerations**: Framework needs to be usable with available data

**Note**: This was not a formal expert panel or statistical optimization. It's a pragmatic framework based on best available evidence and practical considerations.

---

## Limitations and Acknowledged Gaps

### What We Acknowledge:

1. **No single published study uses this exact combination** of 5 components with these exact weights
2. **Some components are extrapolated** from COVID-19 evidence (healthcare, vulnerability)
3. **Weights are not statistically optimized** - they're based on expert judgment and literature review
4. **Population density limitation**: As noted, may not predict R0 well in NYC high-rises
5. **No validation against historical H5N1 outbreaks** (limited data available)

### What We Can Defend:

1. **Poultry density emphasis (45%)** - Strongly supported by literature
2. **Water proximity (15%)** - Supported by H5N1-specific studies
3. **Weighted sum approach** - Standard methodology
4. **Pragmatic framework** - Designed for NYC with available data
5. **Transparent methodology** - All components and weights are documented

---

## Recommendations for Strengthening

To make this more defensible:

1. **Sensitivity analysis**: Test how results change with different weight combinations
2. **Formal expert panel**: Document consensus on weights from multiple experts
3. **Literature review**: Systematic review of all H5N1 risk mapping studies
4. **Validation**: Compare against historical outbreak data if available
5. **Address population density limitation**: Consider multigenerational housing or other proxies
6. **Document decision process**: Create formal documentation of weight selection process

---

## Conclusion

**What is standard methodology**: Weighted sum approach ✓

**What is literature-supported**: 
- Poultry density as primary risk factor ✓
- Water proximity for wild bird habitats ✓

**What is project-specific**:
- Exact combination of 5 components
- Specific weight distribution
- Inclusion of healthcare and vulnerability (extrapolated from COVID-19)

**What we can say**: This is a **pragmatic, evidence-informed framework** for NYC H5N1 risk assessment, designed with available data and project goals in mind. It's not a direct replication of a published methodology, but it's grounded in H5N1 epidemiology and standard risk assessment practices.

**What we should acknowledge**: Some components and weights are based on extrapolation and expert judgment rather than direct H5N1-specific evidence. This is a limitation we should be transparent about.



