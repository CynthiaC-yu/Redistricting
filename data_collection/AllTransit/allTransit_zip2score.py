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
St. Louis city ZCTAs
'''
zip_list = [
    "63101","63102","63103","63104","63105","63106","63107","63108",
    "63109","63110","63111","63112","63113","63115","63116","63117",
    "63118","63119","63120","63123","63125","63130","63133","63136",
    "63137","63138","63139","63143","63147"
]

'''
St. Louis county ZCTAs
'''
# zip_list = [
#     "63005","63011","63017","63021","63025","63026","63031","63033",
#     "63034","63038","63040","63042","63043","63044","63049","63069",
#     "63074","63088","63105","63114","63117","63119","63120","63121",
#     "63122","63123","63124","63125","63126","63127","63128","63129",
#     "63130","63131","63132","63133","63134","63135","63136","63137",
#     "63138","63140","63141","63143","63144","63146"
# ]

df = fetch_multiple_zips(zip_list)

print(df)

fileName = "allTransit_city.csv"
records = df.reset_index().to_dict("records")

fieldnames = df.reset_index().columns.tolist()

with open(fileName, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"Data is wrote into {fileName}")
