import sqlite3
import math
import sys

DB_PATH = r"C:\Users\Chitra\.gemini\antigravity\scratch\stellar_database\stellar_catalog.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def distance_between_stars(name1, name2):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT common_name, pos_x_ly, pos_y_ly, pos_z_ly, distance_ly FROM stars WHERE common_name LIKE ? COLLATE NOCASE", (f"%{name1}%",))
    star1 = cur.fetchone()
    cur.execute("SELECT common_name, pos_x_ly, pos_y_ly, pos_z_ly, distance_ly FROM stars WHERE common_name LIKE ? COLLATE NOCASE", (f"%{name2}%",))
    star2 = cur.fetchone()
    conn.close()
    
    if not star1:
        print(f"Star not found: {name1}")
        return
    if not star2:
        print(f"Star not found: {name2}")
        return
        
    dx = star1[1] - star2[1]
    dy = star1[2] - star2[2]
    dz = star1[3] - star2[3]
    dist_ly = math.sqrt(dx*dx + dy*dy + dz*dz)
    dist_pc = dist_ly / 3.261563777
    
    print(f"\n3D Distance between {star1[0]} and {star2[0]}:")
    print(f"  - Distance: {dist_ly:.3f} light-years ({dist_pc:.3f} parsecs)")
    print(f"  - {star1[0]} distance from Sun: {star1[4]:.3f} ly | 3D: ({star1[1]:.2f}, {star1[2]:.2f}, {star1[3]:.2f}) ly")
    print(f"  - {star2[0]} distance from Sun: {star2[4]:.3f} ly | 3D: ({star2[1]:.2f}, {star2[2]:.2f}, {star2[3]:.2f}) ly")

def print_star_detail(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stars WHERE common_name LIKE ? COLLATE NOCASE", (f"%{name}%",))
    row = cur.fetchone()
    if not row:
        print(f"No star found matching '{name}'.")
        conn.close()
        return
    cols = [d[0] for d in cur.description]
    data = dict(zip(cols, row))
    conn.close()
    
    print("\n" + "=" * 65)
    print(f"  {data['common_name'].upper()} ({data['bayer_flamsteed']})")
    print("=" * 65)
    print(f"  Constellation      : {data['constellation_full']} ({data['constellation']})")
    print(f"  Category           : {data['category']}")
    print(f"  Rank (Brightness)  : #{data['rank_brightness']} | Rank (Distance): #{data['rank_distance']}")
    print(f"  Identifiers        : SIMBAD: {data['simbad_main_id']} | HIP: {data['hip_id']} | HD: {data['hd_id']}")
    print(f"  Spectral Class     : {data['spectral_type']}")
    print(f"  Apparent Mag (V)   : {data['apparent_magnitude']:+.2f} | Absolute Mag (M_V): {data['absolute_magnitude']:+.2f}")
    print(f"  Parallax           : {data['parallax_mas']:.4f} ± {data['parallax_error_mas']} mas")
    print(f"  Distance from Sun  : {data['distance_ly']:.3f} ly ({data['distance_pc']:.3f} pc)")
    print(f"  Equatorial Pos     : RA {data['ra_hms']} ({data['ra_deg']:.4f}°), Dec {data['dec_dms']} ({data['dec_deg']:.4f}°)")
    print(f"  Galactic Pos       : l = {data['galactic_lon_deg']:.4f}°, b = {data['galactic_lat_deg']:.4f}°")
    print(f"  Equatorial 3D (ly) : X = {data['pos_x_ly']:+8.3f}, Y = {data['pos_y_ly']:+8.3f}, Z = {data['pos_z_ly']:+8.3f}")
    print(f"  Galactic 3D (ly)   : X = {data['gal_x_ly']:+8.3f}, Y = {data['gal_y_ly']:+8.3f}, Z = {data['gal_z_ly']:+8.3f}")
    print(f"  Significance       : {data['significance']}")
    print("=" * 65)

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "dist":
        distance_between_stars(sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 1:
        print_star_detail(sys.argv[1])
    else:
        print_star_detail("Sirius")
        distance_between_stars("Sirius", "Proxima Centauri")
