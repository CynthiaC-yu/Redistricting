import pgeocode
import requests
from bs4 import BeautifulSoup
import re
import csv

# Zip to coords
nomi = pgeocode.Nominatim('us')  # 'us' for United States

def get_coords_for_zips(zip_codes):
    """
    input: zip_codes: List[str] or List[int]
    output: List[(zip_code, lat, lon)]
    """
    results = []
    for z in zip_codes:
        info = nomi.query_postal_code(str(z))
        # info.latitude, info.longitude may be NaN
        lat, lon = info.latitude, info.longitude
        if not (lat and lon):
            lat = lon = None
        results.append((str(z), lat, lon))
    return results

# coords to score
def extract_score(img_tag):
    if img_tag and img_tag.has_attr("src"):
        m = re.search(r'/score/(\d+)\.svg', img_tag["src"])
        if m:
            return int(m.group(1))
    return None

def get_scores(lat, lng):
    url = f"https://www.walkscore.com/score/loc/lat={lat}/lng={lng}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        return 'nan', 'nan'
    soup = BeautifulSoup(resp.text, 'html.parser')
    walk = extract_score(soup.find("img", src=re.compile(r'/badge/walk/score/\d+\.svg')))
    bike = extract_score(soup.find("img", src=re.compile(r'/badge/bike/score/\d+\.svg'))) or 0
    return walk, bike


'''
Zip list for St. Louis County
'''
zip_list = [
    "63021","63129","63031","63123","63136","63026","63017","63033",
    "63122","63011","63114","63119","63125","63146","63130","63128",
    "63121","63043","63141","63137","63005","63034","63131","63138",
    "63042","63135","63105","63069","63126","63074","63025","63132",
    "63134","63044","63124","63117","63144","63088","63143","63040",
    "63038","63133","63127","63140","63045","63001","63198","63145",
    "63099","63006","63022","63024","63032","63151","63167","63171",
    "63195"
]

'''
Zip list for St. Louis City
'''
# zip_list = [
#     "63116", "63118", "63109", "63139", "63110", "63111", "63137", "63112",
#     "63115", "63104", "63108", "63113", "63103", "63143", "63147", "63107",
#     "63106", "63120", "63196", "63102", "63101", "63180", "63190", "63182",
#     "63150", "63155", "63157", "63156", "63160", "63158", "63164", "63163",
#     "63166", "63169", "63178", "63177", "63179", "63188", "63197", "63199"
# ]




'''
Below is the implementations
'''
zip_coords = get_coords_for_zips(zip_list)

rows = []
for z, lat, lon in zip_coords:
    if lat is None or lon is None:
        print(f"!!! ZIP {z} No Coords, PASS")
        continue
    walk, bike = get_scores(lat, lon)
    rows.append({
        "zip_code": z,
        "lat": lat,
        "lng": lon,
        "walk_score": walk,
        "bike_score": bike
    })
    print(f"ZIP {z} → ({lat:.5f},{lon:.5f})  Walk:{walk}  Bike:{bike}")

# Write into csv
fileName = "zip_walk_bike_scores.csv"
with open(fileName, "w", newline="", encoding="utf-8") as f:
    cols = ["zip_code","lat","lng","walk_score","bike_score"]
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()
    writer.writerows(rows)

print(f"\nDone: saved to {fileName}")
