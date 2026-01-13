# 🔒 PARITY_LOCK.md

This document defines **LOCKED, VERIFIED, NON-NEGOTIABLE logic** for the Kundli engine.

Any change to items listed here **MUST be treated as a regression** unless re‑verified against **Jagannatha Hora (JHora)** and **AstroSage**.

---

## 🧭 Verification Standards

All parity checks are validated against:

* **Jagannatha Hora (JHora)** – primary astronomical truth
* **AstroSage** – UI & semantic parity target
* **Swiss Ephemeris (swisseph)** – authoritative ephemeris backend

Ayanamsa standard:

* **Lahiri (True Sidereal)**

---

## ⏱️ 1. Time & Julian Day (LOCKED)

### File

`app/utils/time_utils.py`

### Logic (FINAL)

* Birth **local civil time** is parsed first
* Timezone offset is applied **exactly once**
* Local time → UTC conversion:

  ```text
  UTC = Local Time − Timezone Offset
  ```
* Fractional hour is computed as:

  ```python
  hour_fraction = hour + minute / 60 + second / 3600
  ```
* Julian Day is computed using:

  ```python
  swe.julday(year, month, day, hour_fraction, swe.GREG_CAL)
  ```

### Guarantees

* No double UTC correction
* No rounding loss
* Julian Day is **UT-based**, compatible with `swe.calc_ut()`

### Parity Status

✅ Moon sign & degree match JHora

---

## 🌍 2. Ascendant (Lagna) Computation (LOCKED)

### File

`app/engine/houses.py`

### Logic

* Uses **Julian Day (UT)**
* Uses **Swiss Ephemeris** sidereal mode
* Ayanamsa: **Lahiri**

### Output

* `lagna_sign` (1–12)
* `lagna_degree` (0–30 within sign)

### Parity Status

✅ Lagna sign and degree match JHora

---

## 🪐 3. Planetary Longitude Computation (LOCKED)

### File

`app/engine/planets.py`

### Logic

* Uses `swe.calc_ut()` for all planets
* Sidereal mode enabled globally:

  ```python
  swe.set_sid_mode(swe.SIDM_LAHIRI)
  ```
* Absolute longitude normalized to 0–360
* Sign computed as:

  ```python
  sign = int(longitude // 30) + 1
  ```
* Degree-in-sign:

  ```python
  degree_in_sign = longitude % 30
  ```

### Special Cases

* **Rahu**: Mean Node (`swe.MEAN_NODE`)
* **Ketu**: Rahu + 180° (same retrograde flag)

### Parity Status

✅ All planetary longitudes match JHora

---

## 🌟 4. Nakshatra & Pada (LOCKED)

### Logic

* Nakshatra is computed from **absolute longitude**, not degree-in-sign
* Nakshatra span: **13°20′ (13.333333°)**
* Pada span: **3°20′**

### Formula

```python
nakshatra_index = int(longitude // 13.333333) + 1
pada = int((longitude % 13.333333) // 3.333333) + 1
```

### Parity Status

✅ Nakshatra & Pada match JHora

---

## 🔥 5. Combustion Logic (LOCKED)

### Logic

* Angular separation from Sun is computed as:

  ```python
  separation = min(abs(lon - sun_lon), 360 - abs(lon - sun_lon))
  ```
* Planet-specific combustion thresholds are applied

### Parity Status

✅ Matches AstroSage behaviour

---

## 🤝 6. Planet–Sign Relationship (LOCKED)

### Logic

Priority order:

1. Exalted
2. Debilitated
3. Own sign
4. Friendly
5. Enemy
6. Neutral

* Based on **naisargik friendship matrix**
* Matches AstroSage deviations (e.g., Moon–Jupiter enemy)

### Special Case

* Mercury in **Scorpio, Jyeshtha Pada 1** → Neutral (AstroSage parity)

### Parity Status

✅ Matches AstroSage

---

## 🧱 7. D1 (Rāśi) Chart Mapping (LOCKED)

### File

`app/engine/chart_builder.py`

### Logic

* **Sign-based (whole sign) chart**
* Planets are grouped by **sign**, not house
* Lagna sign is always **House 1**

House formula:

```python
house = ((planet_sign - lagna_sign + 12) % 12) + 1
```

### Ascendant Handling

* Ascendant is injected as a pseudo-planet
* Uses absolute longitude for nakshatra

### Parity Status

✅ Matches JHora & AstroSage

---

## 🚫 FORBIDDEN CHANGES

The following must **NOT** be changed without full re‑verification:

* Julian Day computation
* UTC conversion logic
* Ayanamsa mode
* Swiss Ephemeris usage
* Planet sign math
* Nakshatra math
* D1 sign-based grouping

---

## 🧊 STATUS

**D1 PARITY: OFFICIALLY LOCKED** 🔒
Chara Karaka (Jaimini) computation
Baladi (Bala–Mrityu) Avastha
Degree source consistency (degree vs degree_in_sign)
D1, D9.
Vimshottari Dasha
Summary Strip
Karak

Date Locked: *January 2026*


