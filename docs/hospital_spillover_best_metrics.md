# Hospital spillover metrics — `best`

Incidence stream: **symptomatic** · 160 simulation days.

Baselines: ward occupancy 79.8%, ICU 79.4%.

City free beds (staffed × (1 − occupancy)): ward **3227**, ICU **346**.

Peak city census: ward **64**, ICU **12**.

Spillover volume: ward **0** patients, ICU **2**.

## Bed strain timing

| Metric | First day | Cum. cases that day | First stretch (days) | Total days over |
|--------|-----------|---------------------|----------------------|-----------------|
| ward_any_hospital | — | — | 0 | 0 |
| icu_any_hospital | — | — | 0 | 0 |
| ward_citywide_aggregate | — | — | 0 | 0 |
| icu_citywide_aggregate | — | — | 0 | 0 |

## Top 3 hospital systems (v1 catchment cumulative cases)

1. **NYC H+H** — 5,580 cases · 45 ZIPs
2. **INDEPENDENT** — 2,899 cases · 21 ZIPs
3. **NEW YORK - PRESBYTERIAN** — 2,652 cases · 25 ZIPs

## Top 3 hospital systems (routed ward admissions after spillover)

1. **NYC H+H** — 78 ward admissions
2. **INDEPENDENT** — 40 ward admissions
3. **NEW YORK - PRESBYTERIAN** — 37 ward admissions

## Most vulnerable ZIPs (high cases / low free acute beds)

| ZIP | Cum. cases | Assigned hospital | Network | Free acute | Ratio |
|-----|------------|-------------------|---------|------------|-------|
| 10456 | 315 | BRONXCARE CENTER FULTON MANDY (1164) | INDEPENDENT | 29 | 10.9 |
| 11229 | 223 | MAIMONIDES MIDWOOD COMMUNITY (1293) | MAIMONIDES HEALTH | 24 | 9.2 |
| 11230 | 209 | MAIMONIDES MIDWOOD COMMUNITY (1293) | MAIMONIDES HEALTH | 24 | 8.6 |
| 10002 | 251 | NYP: LOWER MANHATTAN (1437) | NEW YORK - PRESBYTERIAN | 30 | 8.5 |
| 11385 | 259 | WYCKOFF HEIGHTS MC (1318) | INDEPENDENT | 34 | 7.6 |
| 10468 | 266 | NYP: ALLEN HOSPITAL (3975) | NEW YORK - PRESBYTERIAN | 36 | 7.4 |
| 11226 | 295 | UNIVERSITY: SUNY DOWNSTATE (1320) | SUNY DOWNSTATE | 45 | 6.5 |
| 11355 | 243 | FLUSHING HOSPITAL MEDICAL CENTER (1628) | MEDISYS HEALTH NETWORK | 37 | 6.5 |
| 10463 | 228 | NYP: ALLEN HOSPITAL (3975) | NEW YORK - PRESBYTERIAN | 36 | 6.3 |
| 11234 | 229 | MOUNT SINAI: BROOKLYN (1324) | MOUNT SINAI HEALTH SYSTEM | 38 | 6.0 |

## Notes

- Assignment: v1 nearest hospital (EPSG:2263); spillover walks next-nearest citywide.
- Ward demand uses `ratio_hospitalization_per_case`; ICU among ward via `ratio_icu_given_hospitalization`; census = rectangular LOS hold.
- Illustrative ZIP apportionment (population × composite risk), not spatial transmission.
