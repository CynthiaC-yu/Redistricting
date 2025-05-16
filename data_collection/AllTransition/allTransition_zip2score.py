import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

'''
Convert ZIP to cooresponding AllTransit score 
'''

def fetch_all_metrics(zip_code, chrome_options=None):
    driver = webdriver.Chrome(options=chrome_options) if chrome_options else webdriver.Chrome()
    try:
        driver.get("https://alltransit.cnt.org/metrics/")

        # Type the ZIP code into the search bar
        inp = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mapboxgl-ctrl-geocoder input[type=text]"))
        )
        inp.clear()
        inp.send_keys(zip_code)

        # Click the first item in the suggestion bar
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mapboxgl-ctrl-geocoder .suggestions li"))
        ).click()

        # Wait
        time.sleep(0.5)

        # Wait for the metric value appears
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.as-metric-value[id]"))
        )

        # Fetch the value
        spans = driver.find_elements(By.CSS_SELECTOR, "span.as-metric-value[id]")
        metrics = {}
        for span in spans:
            mid = span.get_attribute("id")
            raw = span.get_attribute("innerText") or ""
            m = re.search(r"\d+(\.\d+)?", raw)
            if mid and m:
                metrics[mid] = m.group(0)
        return metrics
    finally:
        driver.quit()

def fetch_multiple_zips(zip_codes, chrome_options=None):
    records = []
    for z in zip_codes:
        # First try
        metrics = fetch_all_metrics(z, chrome_options=chrome_options)
        # If the key value is nan, try again -- we want to prevent the case of getting nan
        if not metrics.get("wt_avg_L"):
            time.sleep(1)  # Wait for try again
            metrics = fetch_all_metrics(z, chrome_options=chrome_options)
        metrics['zip_code'] = z
        records.append(metrics)
    df = pd.DataFrame(records).set_index('zip_code')
    return df

'''
Zip list for St. Louis County
'''
# zip_list = [
#     "63021","63129","63031","63123","63136","63026","63017","63033",
#     "63122","63011","63114","63119","63125","63146","63130","63128",
#     "63121","63043","63141","63137","63005","63034","63131","63138",
#     "63042","63135","63105","63069","63126","63074","63025","63132",
#     "63134","63044","63124","63117","63144","63088","63143","63040",
#     "63038","63133","63127","63140","63045","63001","63198","63145",
#     "63099","63006","63022","63024","63032","63151","63167","63171",
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
df = fetch_multiple_zips(zip_list)

print(df)

fileName = "allTransit_city2.csv"
records = df.reset_index().to_dict("records")

fieldnames = df.reset_index().columns.tolist()

with open(fileName, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"Data is wrote into {fileName}")
