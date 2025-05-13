import requests
from bs4 import BeautifulSoup
import re
import csv
import time

def get_zip_code(lat, lng, delay=1):
    """
    Using OpenStreetMap Nominatim API to get postcode。
    Warning: be careful with the request freq. delay is for the time interval between two sent
    requests
    """
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "json",
        "lat": lat,
        "lon": lng,
        "addressdetails": 1,
    }
    headers = {
        "User-Agent": "BatchWalkBike/1.0 (your_email@example.com)"
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        postcode = data.get("address", {}).get("postcode", "")
    except Exception as e:
        print(f"Reverse geocode failed for {lat},{lng}: {e}")
        postcode = ""
    time.sleep(delay)
    return postcode

def extract_score(img_tag):
    if img_tag and img_tag.has_attr("src"):
        m = re.search(r'/score/(\d+)\.svg', img_tag["src"])
        if m:
            return int(m.group(1))
    return None


def get_scores(lat, lng):
    """
    Same score as walk_score.py file Walk Score & Bike Score
    """
    url = f"https://www.walkscore.com/score/loc/lat={lat}/lng={lng}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        print(f"Failed to fetch page for {lat},{lng}: {resp.status_code}")
        return None, None

    soup = BeautifulSoup(resp.text, 'html.parser')
    walk_img = soup.find("img", src=re.compile(r'/badge/walk/score/\d+\.svg'))
    bike_img = soup.find("img", src=re.compile(r'/badge/bike/score/\d+\.svg'))

    walk = extract_score(walk_img)
    bike = extract_score(bike_img)

    return walk, bike

# 1) Read multiple coords for user

'''
TWO FUNCTIONS:
1) you can input an existed coords array
2) leave the coords to be empty, then you can input several coords
'''
# coords = []

coords = [
(38.639633, -90.330800),
(40.712776, -74.005974)
]

print(len(coords))

if coords:
    pass
else:
    print("Input multiple input coords, each row should be: 'lat,lng', enter space to stop:")
    while True:
        line = input().strip()
        if not line:
            break
        try:
            lat_str, lng_str = line.split(",")
            lat = float(lat_str)
            lng = float(lng_str)
            coords.append((lat, lng))
        except:
            print("Wrong format, input: lat,lng(e.g. 38.639633,-90.330800)")
    if not coords:
        print("Received no coordinate. Program exits.") 

# 2) Find result for each row
results = []
for lat, lng in coords:
    print(f"Processing {lat}, {lng} …")
    walk, bike = get_scores(lat, lng)
    zip_code = get_zip_code(lat, lng)
    results.append({
        "lat": lat,
        "lng": lng,
        "walk_score": walk,
        "bike_score": bike,
        "zip_code": zip_code
    })

# 3) Write into CSV File
output_file = "walk_bike_scores.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["lat", "lng", "walk_score", "bike_score", "zip_code"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"\nSaved the result to {output_file}")




