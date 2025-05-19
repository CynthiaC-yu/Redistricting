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
St. Louis city ZCTAs
'''
# zip_list = [
#     "63101","63102","63103","63104","63105","63106","63107","63108",
#     "63109","63110","63111","63112","63113","63115","63116","63117",
#     "63118","63119","63120","63123","63125","63130","63133","63136",
#     "63137","63138","63139","63143","63147"
# ]

'''
St. Louis county ZCTAs
'''
zip_list = [
    "63005","63011","63017","63021","63025","63026","63031","63033",
    "63034","63038","63040","63042","63043","63044","63049","63069",
    "63074","63088","63105","63114","63117","63119","63120","63121",
    "63122","63123","63124","63125","63126","63127","63128","63129",
    "63130","63131","63132","63133","63134","63135","63136","63137",
    "63138","63140","63141","63143","63144","63146"
]

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
