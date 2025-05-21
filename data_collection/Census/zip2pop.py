import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


place = 'county'

def fetch_total_population(zip_code, driver, wait):
    """
    打开 ZIP code 的 Census profile 页，
    从顶部 Highlights 模块里读取“Total Population”数值。
    """
    url = f"https://data.census.gov/profile/ZCTA5_{zip_code}?g=860XX00US{zip_code}"
    driver.get(url)

    # 等待 “Total Population” 高亮模块加载完成
    highlight = wait.until(EC.presence_of_element_located(
        (By.ID, "measure-highlight-populations-and-people")
    ))

    # 定位其中显示数值的 div.highlight-value
    value_el = highlight.find_element(By.CSS_SELECTOR, "div.highlight-value.nowrap")
    raw = value_el.text.strip().replace(",", "")

    if not raw:
        raise ValueError(f"No total population found for {zip_code}")
    return int(raw)

if place == 'city':
    '''
    St. Louis city ZCTAs
    '''
    zip_list = [
        "63101","63102","63103","63104","63105","63106","63107","63108",
        "63109","63110","63111","63112","63113","63115","63116","63117",
        "63118","63119","63120","63123","63125","63130","63133","63136",
        "63137","63138","63139","63143","63147"
    ]
elif place == 'county':
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

output_file = f"zip_population_{place}.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["zip_code", "population"])

    for z in zip_list:
        try:
            pop = fetch_total_population(z, driver, wait)
            writer.writerow([z, pop])
            print(f"{z}: {pop}")
        except Exception as e:
            print(f"Error for {z}: {e}")

driver.quit()
print(f"Wrote into {output_file}")

