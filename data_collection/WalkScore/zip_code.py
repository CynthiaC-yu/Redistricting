import requests
import time
import csv

'''
This one can help you to convert a list of zip code to the cooresponding coords
However, there is still an issue of unable to find certain zips' coords.
'''

def get_coords_for_zips(zip_codes, country="US", delay=1):
    # It will return none if the coords cooresponding to the given zip is not found.
    base_url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "ZipToCoords/1.0 (your_email@example.com)"
    }
    results = []

    for z in zip_codes:
        z_str = str(z).strip()
        params = {
            "postalcode": z_str,
            "country": country,
            "format": "json",
            "limit": 1,
        }

        try:
            resp = requests.get(base_url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
            else:
                lat = lon = None
        except Exception as e:
            print(f"Error geocoding {z_str}: {e}")
            lat = lon = None
    
        results.append((z_str, lat, lon))
        print(f'{z_str} is added')
        time.sleep(delay)

    return results

print('Program started...')
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

coords = get_coords_for_zips(zip_list)
for z, lat, lon in coords:
    print(f"ZIP {z}:  lat={lat}, lon={lon}")


output_file = "zip_code_to_coords.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["lat", "lng"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for z, lat, lon in coords:
        writer.writerow({
            "lat": lat,
            "lng": lon
        })


print(f"\nSaved the result to {output_file}")

