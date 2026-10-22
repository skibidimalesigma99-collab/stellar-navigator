# 100 Important Stars Relative to the Sun: Astrometric & 3D Spatial Database

A precision astronomical database of the **100 most important stars relative to the Sun**, compiled directly from official astrometric catalogs (CDS / SIMBAD, Hipparcos, and Gaia DR3).

---

## 1. Database Files & Location

All files are stored in the project workspace:
`C:\Users\Chitra\.gemini\antigravity\scratch\stellar_database\`

| File | Description |
| :--- | :--- |
| **`index.html`** | Interactive 3D Stellar Navigator (Three.js WebGL app with 3D grid & spaceflight mode). |
| **`run_app.py`** | Python launcher that boots a local server and auto-launches the 3D navigator in your browser. |
| **`launch_navigator.bat`** | Double-click Windows shortcut to launch the 3D Navigator immediately. |
| **`stellar_catalog.db`** | Production SQLite3 database containing tables, precomputed views, and indexes. |
| **`stellar_catalog.csv`** | Comma-separated tabular export for Pandas, Excel, or R analysis. |
| **`stellar_catalog.json`** | Structured JSON export with complete nested metadata for web and app integration. |
| **`catalog_data.js`** | JavaScript-embedded dataset for zero-CORS offline browsing. |
| **`query_stars.py`** | Interactive CLI and Python utility to query stars and calculate 3D interstellar distances. |
| **`build_stellar_database.py`** | Automated ETL pipeline querying CDS/SIMBAD TAP and calculating 3D positions. |
| **`verify_db.py`** | Automated test suite verifying 3D mathematical and astronomical consistency. |

---

## 2. Interactive 3D Grid Navigator & Flight Controls

You can explore the 100 stars and the Sun across a 3D coordinate grid plane:

### How to Launch:
1. Double-click **`launch_navigator.bat`** or run `python run_app.py` in PowerShell.
2. Alternatively, double-click **`index.html`** to open it directly in Google Chrome, Microsoft Edge, or Mozilla Firefox.

### Navigation Modes:
- **✈️ Spaceflight / Plane Navigation Mode**:
  - Fly through the 3D star grid like a spacecraft pilot!
  - `W` / `S`: Pitch Down / Pitch Up or Throttle forward / backward
  - `A` / `D`: Yaw / Steer Left or Right
  - `Space` / `C`: Ascend / Descend vertically through the grid plane
  - `Shift`: Warp Afterburner boost (5x speed)
  - `Mouse Drag`: Steer and look in any 3D direction
- **🛰️ Tactical Orbit Mode**:
  - Left-Click + Drag: Orbit turntable around the Sun or targeted star
  - Right-Click + Drag: Pan across the grid
  - Scroll Wheel: Smooth zoom from 1 ly to 3,000 ly
  - Click any star: Open full telemetry card, view coordinates, and click `🚀 Warp / Travel to Star`

### 3D Spatial Grid Features:
- **Reference Grid Plane ($Z = 0$)**: Displays the celestial equator (or galactic disk) with selectable grid spacing (10 to 100 light-years).
- **Height Stems (Drop Lines)**: Vertical laser lines connecting each star down to its footprint on the reference grid plane (Cyan = above plane, Magenta = below plane) for intuitive 3D depth perception.
- **Concentric Distance Rings**: Rings at 5, 10, 20, 50, 100, 250, 500, and 1,000 light-years from the Sun.
- **Basic Solar System Simulation**: Positioned right at the origin `(0, 0, 0)`:
  - **The Sun (Sol)** with radiant corona and mass/spectral profile.
  - **All 8 Major Planets**: Mercury, Venus, Earth (+ orbiting Moon), Mars, Jupiter, Saturn (+ tilted 3D ring system), Uranus, and Neptune.
  - **Orbital Revolutions**: Planets animate along their orbital planes with Keplerian-proportional speeds.
  - **Interactive Telemetry**: Click on any planet or the Sun to inspect orbital distances (in AU and million km), periods, and planetary classifications.
  - **Focus Button**: Click `🪐 Focus Solar System` to fly the camera into the center and watch the planets revolve around the Sun.
  - **Orbit Speed Slider & Toggle**: Control simulation speed from 0x (pause) to 4x, or toggle solar system visibility.
- **Interstellar Ruler**: Live measurement tool calculating the exact 3D distance between any two selected stars.
- **Frame Switcher**: Seamless toggle between Equatorial ICRS J2000 and the Galactic Plane.

---

## 2. Selection Methodology (The 100 Important Stars)

The 100 stars are curated without duplicate entries, spanning three essential classes:

1. **Top Brightest Stars in the Night Sky (Ranks 1–63)**:
   - Includes Sirius, Canopus, Rigil Kentaurus (Alpha Cen A), Arcturus, Vega, Capella, Rigel, Procyon, Achernar, Betelgeuse, Hadar, Altair, Acrux, Aldebaran, Antares, Spica, Pollux, Fomalhaut, Deneb, Mimosa, Regulus, Adhara, Castor, Gacrux, Shaula, Bellatrix, Elnath, Miaplacidus, Alnilam, Alnair, Alioth, Alnitak, Dubhe, Mirfak, Wezen, Sargas, Kaus Australis, Avior, Alkaid, Menkalinan, Atria, Alhena, Peacock, Alsephina, Mirzam, Alphard, Polaris, Hamal, Algieba, Diphda, Nunki, Menkent, Mirach, Alpheratz, Saiph, Rasalhague, Kochab, Algol, Denebola, Muhlifain, Aspidiske, Suhail, and Mintaka.
2. **Nearest Stellar Neighbors (< 15 Light-Years, 22 Stars)**:
   - Complete local neighborhood: Proxima Centauri (4.25 ly), Toliman (Alpha Cen B, 4.39 ly), Barnard's Star (5.96 ly), Wolf 359 (7.86 ly), Lalande 21185 (8.30 ly), UV Ceti (8.72 ly), BL Ceti (8.87 ly), Ross 154 (9.71 ly), Ross 248 (10.31 ly), Ran / Epsilon Eridani (10.50 ly), Lacaille 9352 (10.72 ly), Ross 128 (11.01 ly), EZ Aquarii A (11.11 ly), 61 Cygni A & B (11.40 ly), Struve 2398 A (11.49 ly), Groombridge 34 A (11.62 ly), Epsilon Indi (11.87 ly), Tau Ceti (11.91 ly), Luyten's Star (12.35 ly), Teegarden's Star (12.50 ly), and Kapteyn's Star (12.83 ly).
3. **Renowned Landmark, Polar, Historical, Variable, and Extreme Stars (15 Stars)**:
   - **Polaris Australis** (Sigma Octantis, Southern Pole Star)
   - **Thuban** (Ancient Egyptian North Pole Star, c. 3000 BCE)
   - **Delta Cephei** (Prototype classical Cepheid variable, cosmic distance ladder foundation)
   - **Mira** (Prototype long-period pulsating variable)
   - **RR Lyrae** (Prototype horizontal branch pulsating variable standard candle)
   - **Albireo** (Archetype contrasting gold-and-blue visual double star)
   - **Mizar & Alcor** (First telescopic binary [1617], first spectroscopic binary [1889], ancient eye acuity test)
   - **Alcyone** (Brightest star of the Pleiades / M45)
   - **Merak & Phecda** (Big Dipper bowl and navigational pointer stars)
   - **Cor Caroli** (Prototype Alpha2 CVn magnetic variable)
   - **TRAPPIST-1** (Benchmark ultra-cool dwarf hosting 7 Earth-sized exoplanets)
   - **Zeta Puppis (Naos)** (Hottest and most luminous naked-eye O4 supergiant)
   - **Regor (Gamma2 Velorum)** (Brightest and closest Wolf-Rayet star)

---

## 3. Coordinate Frames & Mathematics

Every star's position is recorded in two distinct 3D Cartesian heliocentric coordinate systems (Sun = `[0, 0, 0]`):

### A. Heliocentric Equatorial (ICRS J2000)
- **Origin**: The Sun `(0, 0, 0)`
- **+X axis**: Directed toward the Vernal Equinox ($\alpha = 0^\circ, \delta = 0^\circ$)
- **+Y axis**: Directed toward $\alpha = 90^\circ$ ($6^{\text{h}}$), $\delta = 0^\circ$
- **+Z axis**: Directed toward the North Celestial Pole ($\delta = +90^\circ$)
- **Formulas**:
  $$X = d \cdot \cos(\delta) \cdot \cos(\alpha)$$
  $$Y = d \cdot \cos(\delta) \cdot \sin(\alpha)$$
  $$Z = d \cdot \sin(\delta)$$
  $$\text{Distance check: } \sqrt{X^2 + Y^2 + Z^2} = d$$

### B. Heliocentric Galactic Coordinates (IAU 1958 / J2000)
- **Origin**: The Sun `(0, 0, 0)`
- **+X axis**: Directed toward the Galactic Center ($l = 0^\circ, b = 0^\circ$, Sagittarius A*)
- **+Y axis**: Directed toward the direction of Galactic rotation ($l = 90^\circ, b = 0^\circ$)
- **+Z axis**: Directed toward the North Galactic Pole ($b = +90^\circ$)
- **Formulas**:
  $$X_{\text{gal}} = d \cdot \cos(b) \cdot \cos(l)$$
  $$Y_{\text{gal}} = d \cdot \cos(b) \cdot \sin(l)$$
  $$Z_{\text{gal}} = d \cdot \sin(b)$$
  $$\text{Distance check: } \sqrt{X_{\text{gal}}^2 + Y_{\text{gal}}^2 + Z_{\text{gal}}^2} = d$$

### C. Astronomical Conversions
- **Parallax to Distance**:
  $$d_{\text{pc}} = \frac{1000}{\varpi \text{ (mas)}}$$
  $$d_{\text{ly}} = d_{\text{pc}} \times 3.261563777$$
- **Absolute Magnitude**:
  $$M_V = V - 5 \log_{10}(d_{\text{pc}}) + 5$$

---

## 4. SQLite Database Schema

The primary table is `stars` (39 columns):

```sql
CREATE TABLE stars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank_brightness INTEGER,            -- Rank by apparent visual magnitude (1 = Sirius)
    rank_distance INTEGER NOT NULL,     -- Rank by distance from Sun (1 = Proxima Centauri)
    common_name TEXT NOT NULL UNIQUE,   -- Standard proper name (e.g. Sirius, Vega, Betelgeuse)
    bayer_flamsteed TEXT,               -- Bayer / Flamsteed designation (e.g. Alpha Canis Majoris)
    constellation TEXT NOT NULL,        -- 3-letter IAU constellation abbreviation (e.g. CMa)
    constellation_full TEXT NOT NULL,   -- Full constellation name (e.g. Canis Major)
    hip_id INTEGER,                     -- Hipparcos Catalog ID
    hd_id INTEGER,                      -- Henry Draper Catalog ID
    simbad_main_id TEXT NOT NULL,       -- Official SIMBAD primary identifier
    spectral_type TEXT NOT NULL,        -- MK Spectral Type & Luminosity Class
    apparent_magnitude REAL NOT NULL,   -- Apparent visual magnitude V
    absolute_magnitude REAL NOT NULL,   -- Absolute visual magnitude M_V
    b_magnitude REAL,                   -- Johnson B magnitude
    parallax_mas REAL NOT NULL,         -- Trigonometric parallax in milliarcseconds
    parallax_error_mas REAL,            -- Parallax uncertainty in milliarcseconds
    distance_pc REAL NOT NULL,          -- Distance from Sun in Parsecs
    distance_ly REAL NOT NULL,          -- Distance from Sun in Light-Years
    ra_deg REAL NOT NULL,               -- Right Ascension in decimal degrees (J2000)
    dec_deg REAL NOT NULL,              -- Declination in decimal degrees (J2000)
    ra_hms TEXT NOT NULL,               -- Right Ascension sexagesimal (HHh MMm SS.ss)
    dec_dms TEXT NOT NULL,              -- Declination sexagesimal (±DD° MM' SS.s")
    galactic_lon_deg REAL NOT NULL,     -- Galactic longitude l in degrees
    galactic_lat_deg REAL NOT NULL,     -- Galactic latitude b in degrees
    pos_x_ly REAL NOT NULL,             -- Equatorial 3D Cartesian X (ly)
    pos_y_ly REAL NOT NULL,             -- Equatorial 3D Cartesian Y (ly)
    pos_z_ly REAL NOT NULL,             -- Equatorial 3D Cartesian Z (ly)
    pos_x_pc REAL NOT NULL,             -- Equatorial 3D Cartesian X (pc)
    pos_y_pc REAL NOT NULL,             -- Equatorial 3D Cartesian Y (pc)
    pos_z_pc REAL NOT NULL,             -- Equatorial 3D Cartesian Z (pc)
    gal_x_ly REAL NOT NULL,             -- Galactic 3D Cartesian X (ly)
    gal_y_ly REAL NOT NULL,             -- Galactic 3D Cartesian Y (ly)
    gal_z_ly REAL NOT NULL,             -- Galactic 3D Cartesian Z (ly)
    gal_x_pc REAL NOT NULL,             -- Galactic 3D Cartesian X (pc)
    gal_y_pc REAL NOT NULL,             -- Galactic 3D Cartesian Y (pc)
    gal_z_pc REAL NOT NULL,             -- Galactic 3D Cartesian Z (pc)
    radial_velocity_kms REAL,           -- Heliocentric radial velocity in km/s
    category TEXT NOT NULL,             -- Categorical classification
    significance TEXT NOT NULL          -- Astrophysical & historical importance note
);
```

### Precomputed SQL Views
- **`v_nearest_stars`**: Stars sorted by distance from the Sun in ascending order.
- **`v_brightest_stars`**: Stars sorted by apparent visual magnitude in ascending order.
- **`v_3d_positions`**: Convenient summary of 3D coordinates in both Equatorial and Galactic frames.
- **`v_most_luminous`**: Stars sorted by intrinsic luminosity (absolute magnitude).

---

## 5. Sample SQL Queries

```sql
-- 1. Find all stars within 12 light-years of the Sun
SELECT common_name, distance_ly, spectral_type, apparent_magnitude
FROM stars
WHERE distance_ly <= 12.0
ORDER BY distance_ly ASC;

-- 2. Calculate true 3D Euclidean distance between Sirius and Vega
SELECT s1.common_name AS star1, s2.common_name AS star2,
       ROUND(SQRT(POW(s1.pos_x_ly - s2.pos_x_ly, 2) + 
                  POW(s1.pos_y_ly - s2.pos_y_ly, 2) + 
                  POW(s1.pos_z_ly - s2.pos_z_ly, 2)), 3) AS distance_ly
FROM stars s1, stars s2
WHERE s1.common_name = 'Sirius' AND s2.common_name = 'Vega';

-- 3. Top 5 most intrinsically luminous stars in the catalog
SELECT common_name, bayer_flamsteed, absolute_magnitude, spectral_type, distance_ly
FROM stars
ORDER BY absolute_magnitude ASC
LIMIT 5;
```

---

## 6. Python Usage Example

```python
import sqlite3

conn = sqlite3.connect(r"C:\Users\Chitra\.gemini\antigravity\scratch\stellar_database\stellar_catalog.db")
cur = conn.cursor()

# Query nearest 5 stars
cur.execute("SELECT rank_distance, common_name, distance_ly, pos_x_ly, pos_y_ly, pos_z_ly FROM stars ORDER BY distance_ly ASC LIMIT 5;")
for row in cur.fetchall():
    print(f"#{row[0]}: {row[1]} | Dist: {row[2]:.2f} ly | 3D: ({row[3]:.2f}, {row[4]:.2f}, {row[5]:.2f}) ly")

conn.close()
```
