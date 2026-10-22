import sqlite3

conn = sqlite3.connect(r"C:\Users\Chitra\.gemini\antigravity\scratch\stellar_database\stellar_catalog.db")
cur = conn.cursor()

# 1. Total count
cur.execute("SELECT COUNT(*) FROM stars;")
count = cur.fetchone()[0]
print(f"Total stars in database: {count}")

# 2. Top 10 Nearest Stars
print("\n--- TOP 10 NEAREST STARS RELATIVE TO THE SUN ---")
cur.execute("""
SELECT rank_distance, common_name, bayer_flamsteed, constellation, distance_ly, distance_pc, 
       pos_x_ly, pos_y_ly, pos_z_ly, spectral_type 
FROM stars 
ORDER BY distance_ly ASC LIMIT 10;
""")
for r in cur.fetchall():
    print(f"#{r[0]:<2} {r[1]:<18} ({r[2]:<18}) {r[3]:<4} Dist: {r[4]:>6.3f} ly ({r[5]:>5.3f} pc) | Pos(ly): [{r[6]:>6.2f}, {r[7]:>6.2f}, {r[8]:>6.2f}] | {r[9]}")

# 3. Top 10 Brightest Stars
print("\n--- TOP 10 BRIGHTEST STARS IN THE NIGHT SKY ---")
cur.execute("""
SELECT rank_brightness, common_name, bayer_flamsteed, constellation, apparent_magnitude, absolute_magnitude, distance_ly, spectral_type 
FROM stars 
ORDER BY apparent_magnitude ASC LIMIT 10;
""")
for r in cur.fetchall():
    print(f"#{r[0]:<2} {r[1]:<18} ({r[2]:<18}) {r[3]:<4} V: {r[4]:>5.2f} | M_V: {r[5]:>5.2f} | Dist: {r[6]:>6.1f} ly | {r[7]}")

# 4. Check for any NULLs in critical columns
cur.execute("""
SELECT count(*) FROM stars 
WHERE common_name IS NULL OR distance_ly IS NULL OR ra_deg IS NULL OR dec_deg IS NULL 
   OR pos_x_ly IS NULL OR pos_y_ly IS NULL OR pos_z_ly IS NULL 
   OR gal_x_ly IS NULL OR gal_y_ly IS NULL OR gal_z_ly IS NULL;
""")
null_count = cur.fetchone()[0]
print(f"\nMissing essential columns count: {null_count}")

# 5. Check mathematical distance consistency
cur.execute("""
SELECT common_name, distance_ly, 
       sqrt(pos_x_ly*pos_x_ly + pos_y_ly*pos_y_ly + pos_z_ly*pos_z_ly) as r_calc,
       abs(distance_ly - sqrt(pos_x_ly*pos_x_ly + pos_y_ly*pos_y_ly + pos_z_ly*pos_z_ly)) as diff
FROM stars
ORDER BY diff DESC LIMIT 5;
""")
print("\nMax difference in Equatorial 3D distance reconstruction:")
for r in cur.fetchall():
    print(f"{r[0]:<18}: catalog_d={r[1]:.4f} ly, r_calc={r[2]:.4f} ly, diff={r[3]:.6f} ly")

conn.close()
