# Hospital spillover metrics — `pandemic_flu`

Incidence stream: **symptomatic** · 160 simulation days.

Baselines: ward occupancy 79.8%, ICU 79.4%.

City free beds (staffed × (1 − occupancy)): ward **3227**, ICU **346**.

Peak city census: ward **3227**, ICU **346**.

Spillover volume: ward **19842** patients, ICU **4548**.

## Bed strain timing

| Metric | First day | Cum. cases that day | First stretch (days) | Total days over |
|--------|-----------|---------------------|----------------------|-----------------|
| ward_any_hospital | 7 | 10,717 | 153 | 153 |
| icu_any_hospital | 3 | 4,146 | 157 | 157 |
| ward_citywide_aggregate | 87 | 243,649 | 73 | 73 |
| icu_citywide_aggregate | 28 | 52,824 | 132 | 132 |

## Top 3 hospital systems (v1 catchment cumulative cases)

1. **NYC H+H** — 135,802 cases · 45 ZIPs
2. **INDEPENDENT** — 70,552 cases · 21 ZIPs
3. **NEW YORK - PRESBYTERIAN** — 64,559 cases · 25 ZIPs

## Top 3 hospital systems (routed ward admissions after spillover)

1. **NYC H+H** — 13,422 ward admissions
2. **NEW YORK - PRESBYTERIAN** — 9,149 ward admissions
3. **MOUNT SINAI HEALTH SYSTEM** — 5,813 ward admissions

## Most vulnerable ZIPs (high cases / low free acute beds)

| ZIP | Cum. cases | Assigned hospital | Network | Free acute | Ratio |
|-----|------------|-------------------|---------|------------|-------|
| 10456 | 7,668 | BRONXCARE CENTER FULTON MANDY (1164) | INDEPENDENT | 29 | 265.3 |
| 11229 | 5,423 | MAIMONIDES MIDWOOD COMMUNITY (1293) | MAIMONIDES HEALTH | 24 | 224.1 |
| 11230 | 5,085 | MAIMONIDES MIDWOOD COMMUNITY (1293) | MAIMONIDES HEALTH | 24 | 210.1 |
| 10002 | 6,110 | NYP: LOWER MANHATTAN (1437) | NEW YORK - PRESBYTERIAN | 30 | 205.7 |
| 11385 | 6,306 | WYCKOFF HEIGHTS MC (1318) | INDEPENDENT | 34 | 186.0 |
| 10468 | 6,478 | NYP: ALLEN HOSPITAL (3975) | NEW YORK - PRESBYTERIAN | 36 | 179.9 |
| 11226 | 7,169 | UNIVERSITY: SUNY DOWNSTATE (1320) | SUNY DOWNSTATE | 45 | 159.3 |
| 11355 | 5,903 | FLUSHING HOSPITAL MEDICAL CENTER (1628) | MEDISYS HEALTH NETWORK | 37 | 158.7 |
| 10463 | 5,556 | NYP: ALLEN HOSPITAL (3975) | NEW YORK - PRESBYTERIAN | 36 | 154.3 |
| 11234 | 5,583 | MOUNT SINAI: BROOKLYN (1324) | MOUNT SINAI HEALTH SYSTEM | 38 | 146.1 |

## Notes

- Assignment: v1 nearest hospital (EPSG:2263); spillover walks next-nearest citywide.
- Ward demand uses `ratio_hospitalization_per_case`; ICU among ward via `ratio_icu_given_hospitalization`; census = rectangular LOS hold.
- Illustrative ZIP apportionment (population × composite risk), not spatial transmission.
