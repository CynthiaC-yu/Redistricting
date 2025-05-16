import requests
from bs4 import BeautifulSoup
import re


'''
Although Walk Score website does not directly gives us the access to the walk score, 
I found the information of score is carried in their image of scores. Thus, I will take 
the information from the source link of images. 

'''

def get_scores(lat, lng):
    url = f"https://www.walkscore.com/score/loc/lat={lat}/lng={lng}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find cooresponidng image links
    walk_img = soup.find("img", src=re.compile(r'/badge/walk/score/\d+\.svg'))
    bike_img = soup.find("img", src=re.compile(r'/badge/bike/score/\d+\.svg'))

    def extract_score(img_tag):
        if img_tag and "src" in img_tag.attrs:
            match = re.search(r'/score/(\d+)\.svg', img_tag['src'])
            if match:
                return int(match.group(1))
        return None

    walk_score = extract_score(walk_img)
    bike_score = extract_score(bike_img)

    return walk_score, bike_score


# Example Usage
if __name__ == "__main__":
    lat = input("Enter latitude: ")
    lng = input("Enter longitude: ")
    walk, bike = get_scores(lat, lng)
    print(f"Walk Score: {walk}")
    # When the location is a mid-of-nowhere, the website will not show bike score, so we just
    # assign a 0 value to it to prevent data type errors in future.
    print(f"Bike Score: {bike}")
