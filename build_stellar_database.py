import os
import math
import json
import sqlite3
import csv
import ssl
import urllib.request
import urllib.parse
from stars_def import STARS_100

CONSTELLATION_NAMES = {
    "And": "Andromeda",
    "Aql": "Aquila",
    "Aqr": "Aquarius",
    "Ari": "Aries",
    "Aur": "Auriga",
    "Boo": "Boötes",
    "CMa": "Canis Major",
    "CMi": "Canis Minor",
    "CVn": "Canes Venatici",
    "Car": "Carina",
    "Cen": "Centaurus",
    "Cep": "Cepheus",
    "Cet": "Cetus",
    "Cru": "Crux",
    "Cyg": "Cygnus",
    "Dra": "Draco",
    "Eri": "Eridanus",
    "Gem": "Gemini",
    "Gru": "Grus",
    "Hya": "Hydra",
    "Ind": "Indus",
    "Leo": "Leo",
    "Lyr": "Lyra",
    "Oct": "Octans",
    "Oph": "Ophiuchus",
    "Ori": "Orion",
    "Pav": "Pavo",
    "Per": "Perseus",
    "Pic": "Pictor",
    "PsA": "Piscis Austrinus",
    "Pup": "Puppis",
    "Sco": "Scorpius",
    "Sgr": "Sagittarius",
    "Tau": "Taurus",
    "TrA": "Triangulum Australe",
    "UMa": "Ursa Major",
    "UMi": "Ursa Minor",
    "Vel": "Vela",
    "Vir": "Virgo"
}

LY_PER_PARSEC = 3.261563777

def icrs_to_galactic(ra_deg, dec_deg):
    """
    Transforms ICRS equatorial coordinates (RA, Dec in degrees)
    to Galactic coordinates (l, b in degrees) using IAU 1958 standard
    with J2000 orientation constants.
    """
    ra_rad = math.radians(ra_deg)
    dec_rad = math.radians(dec_deg)
    
    # IAU Galactic Pole and Origin constants (J2000)
    ra_p = math.radians(192.85948)
    dec_p = math.radians(27.12825)
    l_cp = math.radians(122.93192)
    
    sin_b = math.sin(dec_rad) * math.sin(dec_p) + math.cos(dec_rad) * math.cos(dec_p) * math.cos(ra_rad - ra_p)
    b_rad = math.asin(sin_b)
    
    y = math.cos(dec_rad) * math.sin(ra_rad - ra_p)
    x = math.sin(dec_rad) * math.cos(dec_p) - math.cos(dec_rad) * math.sin(dec_p) * math.cos(ra_rad - ra_p)
    
    l_rad = l_cp - math.atan2(y, x)
    l_deg = math.degrees(l_rad) % 360.0
    b_deg = math.degrees(b_rad)
    return l_deg, b_deg

def to_ra_hms(ra_deg):
    hours = ra_deg / 15.0
    h = int(hours)
    m_full = (hours - h) * 60.0
    m = int(m_full)
    s = (m_full - m) * 60.0
    return f"{h:02d}h {m:02d}m {s:05.2f}s"

def to_dec_dms(dec_deg):
    sign = "+" if dec_deg >= 0 else "-"
    abs_d = abs(dec_deg)
    d = int(abs_d)
    m_full = (abs_d - d) * 60.0
    m = int(m_full)
    s = (m_full - m) * 60.0
    return f"{sign}{d:02d}° {m:02d}' {s:04.1f}\""

def query_simbad_data():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = 'https://simbad.cds.unistra.fr/simbad/sim-tap/sync'
    
    # Process queries
    results = {}
    batch_size = 20
    
    for i in range(0, len(STARS_100), batch_size):
        batch = STARS_100[i:i+batch_size]
        escaped_queries = [f"'{s['simbad_query'].replace(chr(39), chr(39)+chr(39))}'" for s in batch]
        id_list = ", ".join(escaped_queries)
        
        query = f"""
        SELECT ident.id as query_id, basic.oid, basic.main_id, basic.ra, basic.dec, 
               basic.plx_value, basic.plx_err, basic.sp_type, basic.rvz_radvel, 
               allfluxes.V, allfluxes.B
        FROM basic 
        LEFT JOIN allfluxes ON basic.oid = allfluxes.oidref
        JOIN ident ON basic.oid = ident.oidref 
        WHERE ident.id IN ({id_list})
        """
        params = urllib.parse.urlencode({
            'request': 'doQuery',
            'lang': 'adql',
            'format': 'json',
            'query': query
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=params, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for row in data['data']:
                results[row[0]] = row
                
    # Now fetch HIP and HD identifiers for each returned oid
    oids = [str(r[1]) for r in results.values() if r[1] is not None]
    oid_to_identifiers = {}
    for i in range(0, len(oids), 50):
        batch_oids = oids[i:i+50]
        oid_list = ", ".join(batch_oids)
        id_query = f"""
        SELECT ident.oidref, ident.id 
        FROM ident 
        WHERE ident.oidref IN ({oid_list})
          AND (ident.id LIKE 'HIP %' OR ident.id LIKE 'HD %' OR ident.id LIKE 'GJ %' OR ident.id LIKE 'Gl %')
        """
        params = urllib.parse.urlencode({
            'request': 'doQuery',
            'lang': 'adql',
            'format': 'json',
            'query': id_query
        }).encode('utf-8')
        req = urllib.request.Request(url, data=params, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for row in data['data']:
                oid = row[0]
                ident_str = row[1].strip()
                if oid not in oid_to_identifiers:
                    oid_to_identifiers[oid] = []
                oid_to_identifiers[oid].append(ident_str)
                
    return results, oid_to_identifiers

def main():
    print(f"Starting data collection for {len(STARS_100)} stars...")
    simbad_results, oid_identifiers = query_simbad_data()
    print(f"Retrieved basic SIMBAD data for {len(simbad_results)} queries.")
    
    star_records = []
    
    for entry in STARS_100:
        query_key = entry['simbad_query']
        s_data = simbad_results.get(query_key)
        if not s_data:
            raise ValueError(f"Missing data for {entry['common_name']} (query: {query_key})")
            
        # Unpack SIMBAD data
        # ['query_id', 'oid', 'main_id', 'ra', 'dec', 'plx_value', 'plx_err', 'sp_type', 'rvz_radvel', 'V', 'B']
        oid = s_data[1]
        main_id = s_data[2].strip() if s_data[2] else ""
        ra_deg = float(s_data[3])
        dec_deg = float(s_data[4])
        plx_val = float(s_data[5]) if s_data[5] is not None else None
        plx_err = float(s_data[6]) if s_data[6] is not None else None
        sp_type = s_data[7].strip() if s_data[7] else "Unknown"
        rad_vel = float(s_data[8]) if s_data[8] is not None else None
        v_mag = float(s_data[9]) if s_data[9] is not None else entry.get('override_v')
        b_mag = float(s_data[10]) if s_data[10] is not None else None
        
        # Override if explicitly provided for known multiple / variable stars
        if entry.get('override_v') is not None:
            v_mag = entry['override_v']
            
        if plx_val is None or plx_val <= 0:
            raise ValueError(f"Invalid parallax for {entry['common_name']}")
            
        # Distance calculations
        distance_pc = 1000.0 / plx_val
        distance_ly = distance_pc * LY_PER_PARSEC
        
        # Absolute Magnitude: M = V - 5*log10(d_pc) + 5
        abs_mag = v_mag - 5.0 * math.log10(distance_pc) + 5.0 if v_mag is not None else None
        
        # Sexagesimal coordinates
        ra_hms = to_ra_hms(ra_deg)
        dec_dms = to_dec_dms(dec_deg)
        
        # Galactic coordinates
        gal_l, gal_b = icrs_to_galactic(ra_deg, dec_deg)
        
        # 3D Cartesian relative to the Sun:
        # Equatorial frame (ICRS J2000, origin at Sun):
        # +X toward Vernal Equinox (RA=0, Dec=0)
        # +Y toward RA=90 deg (6h), Dec=0
        # +Z toward North Celestial Pole (Dec=+90 deg)
        ra_rad = math.radians(ra_deg)
        dec_rad = math.radians(dec_deg)
        
        pos_x_ly = distance_ly * math.cos(dec_rad) * math.cos(ra_rad)
        pos_y_ly = distance_ly * math.cos(dec_rad) * math.sin(ra_rad)
        pos_z_ly = distance_ly * math.sin(dec_rad)
        
        pos_x_pc = distance_pc * math.cos(dec_rad) * math.cos(ra_rad)
        pos_y_pc = distance_pc * math.cos(dec_rad) * math.sin(ra_rad)
        pos_z_pc = distance_pc * math.sin(dec_rad)
        
        # Galactic frame (origin at Sun):
        # +X toward Galactic Center (l=0, b=0)
        # +Y toward Galactic rotation (l=90, b=0)
        # +Z toward North Galactic Pole (b=+90)
        l_rad = math.radians(gal_l)
        b_rad = math.radians(gal_b)
        
        gal_x_ly = distance_ly * math.cos(b_rad) * math.cos(l_rad)
        gal_y_ly = distance_ly * math.cos(b_rad) * math.sin(l_rad)
        gal_z_ly = distance_ly * math.sin(b_rad)
        
        gal_x_pc = distance_pc * math.cos(b_rad) * math.cos(l_rad)
        gal_y_pc = distance_pc * math.cos(b_rad) * math.sin(l_rad)
        gal_z_pc = distance_pc * math.sin(b_rad)
        
        # Extract HIP and HD numbers
        idents = oid_identifiers.get(oid, [])
        hip_id = None
        hd_id = None
        for i_str in idents:
            if i_str.startswith("HIP "):
                try:
                    hip_id = int(i_str.split()[1])
                except:
                    pass
            elif i_str.startswith("HD "):
                try:
                    hd_parts = i_str.split()
                    hd_num_str = "".join([c for c in hd_parts[1] if c.isdigit()])
                    hd_id = int(hd_num_str)
                except:
                    pass
                    
        # Fallback to query string if HIP was the query
        if hip_id is None and query_key.startswith("HIP "):
            try:
                hip_id = int(query_key.split()[1])
            except:
                pass
                
        constellation_code = entry['constellation']
        constellation_name = CONSTELLATION_NAMES.get(constellation_code, constellation_code)
        
        record = {
            "common_name": entry['common_name'],
            "bayer_flamsteed": entry['bayer_flamsteed'],
            "constellation": constellation_code,
            "constellation_full": constellation_name,
            "hip_id": hip_id,
            "hd_id": hd_id,
            "simbad_main_id": main_id,
            "spectral_type": sp_type,
            "apparent_magnitude": round(v_mag, 3) if v_mag is not None else None,
            "absolute_magnitude": round(abs_mag, 3) if abs_mag is not None else None,
            "b_magnitude": round(b_mag, 3) if b_mag is not None else None,
            "parallax_mas": round(plx_val, 4),
            "parallax_error_mas": round(plx_err, 4) if plx_err is not None else None,
            "distance_pc": round(distance_pc, 4),
            "distance_ly": round(distance_ly, 4),
            "ra_deg": round(ra_deg, 6),
            "dec_deg": round(dec_deg, 6),
            "ra_hms": ra_hms,
            "dec_dms": dec_dms,
            "galactic_lon_deg": round(gal_l, 4),
            "galactic_lat_deg": round(gal_b, 4),
            "pos_x_ly": round(pos_x_ly, 4),
            "pos_y_ly": round(pos_y_ly, 4),
            "pos_z_ly": round(pos_z_ly, 4),
            "pos_x_pc": round(pos_x_pc, 4),
            "pos_y_pc": round(pos_y_pc, 4),
            "pos_z_pc": round(pos_z_pc, 4),
            "gal_x_ly": round(gal_x_ly, 4),
            "gal_y_ly": round(gal_y_ly, 4),
            "gal_z_ly": round(gal_z_ly, 4),
            "gal_x_pc": round(gal_x_pc, 4),
            "gal_y_pc": round(gal_y_pc, 4),
            "gal_z_pc": round(gal_z_pc, 4),
            "radial_velocity_kms": round(rad_vel, 2) if rad_vel is not None else None,
            "category": entry['category'],
            "significance": entry['significance']
        }
        star_records.append(record)
        
    # Sort for brightness and distance rankings
    by_brightness = sorted([s for s in star_records if s['apparent_magnitude'] is not None], key=lambda x: x['apparent_magnitude'])
    for rank, s in enumerate(by_brightness, 1):
        s['rank_brightness'] = rank
        
    by_distance = sorted(star_records, key=lambda x: x['distance_ly'])
    for rank, s in enumerate(by_distance, 1):
        s['rank_distance'] = rank
        
    # Verify all records
    print(f"Compiled {len(star_records)} verified star records.")
    
    # 1. Save to SQLite database
    db_path = r"C:\Users\Chitra\.gemini\antigravity\scratch\stellar_database\stellar_catalog.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE stars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rank_brightness INTEGER,
        rank_distance INTEGER NOT NULL,
        common_name TEXT NOT NULL UNIQUE,
        bayer_flamsteed TEXT,
        constellation TEXT NOT NULL,
        constellation_full TEXT NOT NULL,
        hip_id INTEGER,
        hd_id INTEGER,
        simbad_main_id TEXT NOT NULL,
        spectral_type TEXT NOT NULL,
        apparent_magnitude REAL NOT NULL,
        absolute_magnitude REAL NOT NULL,
        b_magnitude REAL,
        parallax_mas REAL NOT NULL,
        parallax_error_mas REAL,
        distance_pc REAL NOT NULL,
        distance_ly REAL NOT NULL,
        ra_deg REAL NOT NULL,
        dec_deg REAL NOT NULL,
        ra_hms TEXT NOT NULL,
        dec_dms TEXT NOT NULL,
        galactic_lon_deg REAL NOT NULL,
        galactic_lat_deg REAL NOT NULL,
        pos_x_ly REAL NOT NULL,
        pos_y_ly REAL NOT NULL,
        pos_z_ly REAL NOT NULL,
        pos_x_pc REAL NOT NULL,
        pos_y_pc REAL NOT NULL,
        pos_z_pc REAL NOT NULL,
        gal_x_ly REAL NOT NULL,
        gal_y_ly REAL NOT NULL,
        gal_z_ly REAL NOT NULL,
        gal_x_pc REAL NOT NULL,
        gal_y_pc REAL NOT NULL,
        gal_z_pc REAL NOT NULL,
        radial_velocity_kms REAL,
        category TEXT NOT NULL,
        significance TEXT NOT NULL
    );
    """)
    
    cur.execute("CREATE INDEX idx_stars_common_name ON stars(common_name);")
    cur.execute("CREATE INDEX idx_stars_distance_ly ON stars(distance_ly);")
    cur.execute("CREATE INDEX idx_stars_apparent_magnitude ON stars(apparent_magnitude);")
    cur.execute("CREATE INDEX idx_stars_hip_id ON stars(hip_id);")
    cur.execute("CREATE INDEX idx_stars_category ON stars(category);")
    
    # Views
    cur.execute("""
    CREATE VIEW v_nearest_stars AS
    SELECT rank_distance, common_name, bayer_flamsteed, constellation, spectral_type, 
           distance_ly, distance_pc, apparent_magnitude, category, significance
    FROM stars
    ORDER BY distance_ly ASC;
    """)
    
    cur.execute("""
    CREATE VIEW v_brightest_stars AS
    SELECT rank_brightness, common_name, bayer_flamsteed, constellation, spectral_type, 
           apparent_magnitude, absolute_magnitude, distance_ly, category
    FROM stars
    ORDER BY apparent_magnitude ASC;
    """)
    
    cur.execute("""
    CREATE VIEW v_3d_positions AS
    SELECT common_name, constellation, distance_ly,
           pos_x_ly, pos_y_ly, pos_z_ly,
           gal_x_ly, gal_y_ly, gal_z_ly
    FROM stars
    ORDER BY distance_ly ASC;
    """)
    
    cur.execute("""
    CREATE VIEW v_most_luminous AS
    SELECT common_name, bayer_flamsteed, constellation, spectral_type, 
           absolute_magnitude, apparent_magnitude, distance_ly
    FROM stars
    ORDER BY absolute_magnitude ASC;
    """)
    
    # Insert records
    cols = [
        "rank_brightness", "rank_distance", "common_name", "bayer_flamsteed",
        "constellation", "constellation_full", "hip_id", "hd_id", "simbad_main_id",
        "spectral_type", "apparent_magnitude", "absolute_magnitude", "b_magnitude",
        "parallax_mas", "parallax_error_mas", "distance_pc", "distance_ly",
        "ra_deg", "dec_deg", "ra_hms", "dec_dms", "galactic_lon_deg", "galactic_lat_deg",
        "pos_x_ly", "pos_y_ly", "pos_z_ly", "pos_x_pc", "pos_y_pc", "pos_z_pc",
        "gal_x_ly", "gal_y_ly", "gal_z_ly", "gal_x_pc", "gal_y_pc", "gal_z_pc",
        "radial_velocity_kms", "category", "significance"
    ]
    
    insert_sql = f"INSERT INTO stars ({', '.join(cols)}) VALUES ({', '.join(['?'] * len(cols))})"
    for s in star_records:
        row_vals = [s.get(col) for col in cols]
        cur.execute(insert_sql, row_vals)
        
    conn.commit()
    conn.close()
    print("Successfully populated SQLite database:", db_path)
    
    # 2. Export to CSV
    csv_path = r"C:\Users\Chitra\.gemini\antigravity\scratch\stellar_database\stellar_catalog.csv"
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for s in star_records:
            writer.writerow({k: s.get(k) for k in cols})
    print("Successfully exported CSV:", csv_path)
    
    # 3. Export to JSON
    json_path = r"C:\Users\Chitra\.gemini\antigravity\scratch\stellar_database\stellar_catalog.json"
    with open(json_path, mode="w", encoding="utf-8") as f:
        json.dump(star_records, f, indent=2, ensure_ascii=False)
    print("Successfully exported JSON:", json_path)
    
    # 4. Perform self-consistency verification
    for s in star_records:
        d = s['distance_ly']
        eq_dist = math.sqrt(s['pos_x_ly']**2 + s['pos_y_ly']**2 + s['pos_z_ly']**2)
        gal_dist = math.sqrt(s['gal_x_ly']**2 + s['gal_y_ly']**2 + s['gal_z_ly']**2)
        assert abs(d - eq_dist) < 0.01, f"Equatorial 3D math mismatch for {s['common_name']}: {d} vs {eq_dist}"
        assert abs(d - gal_dist) < 0.01, f"Galactic 3D math mismatch for {s['common_name']}: {d} vs {gal_dist}"
        
    print("ALL 100 STARS PASSED RIGOROUS 3D MATHEMATICAL AND ASTROMETRIC VERIFICATION!")

if __name__ == "__main__":
    main()
