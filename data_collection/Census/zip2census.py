import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
This code will convert a given list of zip code to the cooresponding census data
'''

# define the race categories and their corresponding subtopic IDs in the page HTML
CATEGORIES = {
    "American Indian and Alaska Native":       "american-indian-and-alaska-native",
    "Asian":                                   "asian",
    "Black or African American":               "black-or-african-american",
    "Hispanic or Latino":                      "hispanic-or-latino",
    "Native Hawaiian and Other Pacific Islander": "native-hawaiian-and-other-pacific-islander",
    "Not Hispanic or Latino":                  "not-hispanic-or-latino",
    "Some Other Race":                         "some-other-race",
    "Two or More Races":                       "two-or-more-races",
    "White":                                   "white",
}

def fetch_race_ethnicity(zip_code, driver, wait):
    """
    Navigate to the Census profile for this ZIP and scrape only the first
    (ZIP-level) estimate for each category in CATEGORIES.
    """
    url = f"https://data.census.gov/profile/ZCTA5_{zip_code}?g=860XX00US{zip_code}#race-and-ethnicity"
    driver.get(url)

    results = {}
    for label, slug in CATEGORIES.items():
        section_id = f"subtopic_{slug}"
        anchor = wait.until(EC.presence_of_element_located((By.ID, section_id)))
        driver.execute_script("arguments[0].scrollIntoView(true);", anchor)
        xpath = (
            f"//div[@id='{section_id}']/ancestor::div[contains(@class,'SubTopic')]" 
            + "//span[contains(@class,'measure-estimate-value')]"
        )
        spans = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        raw = spans[0].text.strip()
        results[label] = int(raw.replace(",", ""))
    return results


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

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

fieldnames = ["zip_code"] + list(CATEGORIES.keys())
filename = "census_race_ethnicity.csv"
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for z in zip_list:
        try:
            data = fetch_race_ethnicity(z, driver, wait)
            data["zip_code"] = z
            writer.writerow(data)
            print(f"OK: {z}")
        except Exception as e:
            print(f"ERROR for {z}: {e}")

driver.quit()
print(f"All done! Results in {filename}")


