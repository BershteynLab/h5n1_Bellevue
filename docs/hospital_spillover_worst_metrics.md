# Hospital spillover metrics — `worst`

Incidence stream: **symptomatic** · 160 simulation days.

Baselines: ward occupancy 79.8%, ICU 79.4%.

City free beds (staffed × (1 − occupancy)): ward **3227**, ICU **346**.

Peak city census: ward **3227**, ICU **346**.

Spillover volume: ward **34767** patients, ICU **3822**.

## Bed strain timing

| Metric | First day | Cum. cases that day | First stretch (days) | Total days over |
|--------|-----------|---------------------|----------------------|-----------------|
| ward_any_hospital | 2 | 3,749 | 119 | 133 |
| icu_any_hospital | 0 | 480 | 132 | 150 |
| ward_citywide_aggregate | 4 | 9,180 | 109 | 118 |
| icu_citywide_aggregate | 2 | 3,749 | 120 | 131 |

## Top 3 hospital systems (v1 catchment cumulative cases)

1. **NYC H+H** — 1,274,280 cases · 45 ZIPs
2. **INDEPENDENT** — 662,021 cases · 21 ZIPs
3. **NEW YORK - PRESBYTERIAN** — 605,779 cases · 25 ZIPs

## Top 3 hospital systems (routed ward admissions after spillover)

1. **NYC H+H** — 10,765 ward admissions
2. **NEW YORK - PRESBYTERIAN** — 7,940 ward admissions
3. **MOUNT SINAI HEALTH SYSTEM** — 5,066 ward admissions

## Most vulnerable ZIPs (high cases / low free acute beds)

| ZIP | Cum. cases | Assigned hospital | Network | Free acute | Ratio |
|-----|------------|-------------------|---------|------------|-------|
| 10456 | 71,948 | BRONXCARE CENTER FULTON MANDY (1164) | INDEPENDENT | 29 | 2489.5 |
| 11229 | 50,882 | MAIMONIDES MIDWOOD COMMUNITY (1293) | MAIMONIDES HEALTH | 24 | 2102.6 |
| 11230 | 47,714 | MAIMONIDES MIDWOOD COMMUNITY (1293) | MAIMONIDES HEALTH | 24 | 1971.7 |
| 10002 | 57,329 | NYP: LOWER MANHATTAN (1437) | NEW YORK - PRESBYTERIAN | 30 | 1930.3 |
| 11385 | 59,174 | WYCKOFF HEIGHTS MC (1318) | INDEPENDENT | 34 | 1745.6 |
| 10468 | 60,782 | NYP: ALLEN HOSPITAL (3975) | NEW YORK - PRESBYTERIAN | 36 | 1688.4 |
| 11226 | 67,266 | UNIVERSITY: SUNY DOWNSTATE (1320) | SUNY DOWNSTATE | 45 | 1494.8 |
| 11355 | 55,393 | FLUSHING HOSPITAL MEDICAL CENTER (1628) | MEDISYS HEALTH NETWORK | 37 | 1489.1 |
| 10463 | 52,138 | NYP: ALLEN HOSPITAL (3975) | NEW YORK - PRESBYTERIAN | 36 | 1448.3 |
| 11234 | 52,385 | MOUNT SINAI: BROOKLYN (1324) | MOUNT SINAI HEALTH SYSTEM | 38 | 1371.3 |

## Notes

- Assignment: v1 nearest hospital (EPSG:2263); spillover walks next-nearest citywide.
- Ward demand uses `ratio_hospitalization_per_case`; ICU among ward via `ratio_icu_given_hospitalization`; census = rectangular LOS hold.
- Illustrative ZIP apportionment (population × composite risk), not spatial transmission.
