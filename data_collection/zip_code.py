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
Zip list for St. Louis County
'''
# zip_list = [
#     "63021", "63129", "63031", "63123", "63136", "63026", "63017", "63033",
#     "63122", "63011", "63114", "63119", "63125", "63146", "63130", "63128",
#     "63121", "63043", "63141", "63137", "63005", "63034", "63131", "63138",
#     "63042", "63135", "63105", "63069", "63126", "63074", "63025", "63132",
#     "63134", "63044", "63124", "63117", "63144", "63088", "63143", "63040",
#     "63038", "63133", "63127", "63140", "63045", "63001", "63198", "63145",
#     "63099", "63006", "63022", "63024", "63032", "63151", "63167", "63171",
#     "63195"
# ]    

'''
Zip list for St. Louis City
'''
zip_list = [
    "63116", "63118", "63109", "63139", "63110", "63111", "63137", "63112",
    "63115", "63104", "63108", "63113", "63103", "63143", "63147", "63107",
    "63106", "63120", "63196", "63102", "63101", "63180", "63190", "63182",
    "63150", "63155", "63157", "63156", "63160", "63158", "63164", "63163",
    "63166", "63169", "63178", "63177", "63179", "63188", "63197", "63199"
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

