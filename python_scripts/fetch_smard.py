"""
Downloads energy market data from SMARD.de via automated browser interaction using Selenium.

The script opens the data download interface on the Chrome browser, applies the selected
parameters (main category, data category, bidding/control zone, date range, resolution, and filetype),
and downloads the results to /data/raw.

This script is designed to be imported and controlled by a central script(main.py).
"""
from datetime import datetime
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from pathlib import Path


def setup_driver():
    """
    Configures and returns a Selenium Chrome WebDriver with download settings
    pointing to the project's data/raw directory.
    """
    options = Options()

    download_folder = os.path.join("data", "raw")

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    prefs = {
        "download.default_directory": os.path.abspath(download_folder),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    return driver


def download_dataset(
    driver,
    main_category,
    data_category,
    bidding_zone,
    start_date,
    end_date,
    resolution,
    filetype
):
    """
    Automates selection and downloading of a specific data set from smard.de using Selenium.

    Parameters:
        driver (webdriver.Chrome): A configured Selenium WebDriver instance. (use setup_driver())
        main_category: Option from 'Main category' dropdown (e.g., "Main category: Electricity generation").
        data_category: Option from 'Data category' dropdown (e.g., "Data category: Actual generation").
        bidding_zone: Option from 'Select country/bidding zone' dropdown (e.g., "Control Area (DE): 50Hertz"). Can also refer to a country or a control zone.
        start_date: Start of date range in "mm/dd/yyyy" format.
        end_date: End of date range in "mm/dd/yyyy" format.
        resolution: Option from 'Select resolution' dropdown (e.g., "Resolution: Month").
        filetype: Option from 'Select filetype' dropdown.

    Notes:
        - The selected date range is embedded directly into the URL query.
    """
    wait = WebDriverWait(driver, 10)

    start_dt = int(datetime.strptime(start_date, "%m/%d/%Y").timestamp() * 1000)
    end_dt = int(datetime.strptime(end_date, "%m/%d/%Y").timestamp() * 1000)

    url = f"https://www.smard.de/en/downloadcenter/download-market-data/?downloadAttributes=%7B\"from\":{start_dt},\"to\":{end_dt}%7D"
    driver.get(url)

    time.sleep(1)

    # Main category
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[aria-label="Main category"]'))).click()
    select_element = driver.find_element(By.CSS_SELECTOR, 'select[aria-label="Main category"]')

    time.sleep(1)

    select = Select(select_element)
    select.select_by_visible_text(main_category)
    driver.find_element(By.CSS_SELECTOR, 'body').click()

    time.sleep(1)

    # Data category
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[aria-label="Data category"]'))).click()
    data_select_element = driver.find_element(By.CSS_SELECTOR, 'select[aria-label="Data category"]')

    time.sleep(1)

    data_select = Select(data_select_element)
    data_select.select_by_visible_text(data_category)
    driver.find_element(By.CSS_SELECTOR, 'body').click()

    time.sleep(1)

    # Bidding zone
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[aria-label="Select country/bidding zone"]'))).click()
    zone_select_element = driver.find_element(By.CSS_SELECTOR, 'select[aria-label="Select country/bidding zone"]')

    time.sleep(1)

    zone_select = Select(zone_select_element)
    zone_select.select_by_visible_text(bidding_zone)
    driver.find_element(By.CSS_SELECTOR, 'body').click()

    time.sleep(1)

    # Resolution
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[aria-label="Select resolution"]'))).click()
    res_select_element = driver.find_element(By.CSS_SELECTOR, 'select[aria-label="Select resolution"]')

    time.sleep(1)

    res_select = Select(res_select_element)
    res_select.select_by_visible_text(resolution)
    driver.find_element(By.CSS_SELECTOR, 'body').click()

    time.sleep(1)

    # Filetype
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[aria-label="Select filetype"]'))).click()
    type_select_element = driver.find_element(By.CSS_SELECTOR, 'select[aria-label="Select filetype"]')

    time.sleep(1)

    type_select = Select(type_select_element)
    type_select.select_by_visible_text(filetype)
    driver.find_element(By.CSS_SELECTOR, 'body').click()

    time.sleep(1)

    download_dir = os.path.join("data", "raw")
    before_files = set(Path(download_dir).glob("*"))
    # Download button
    download_button = wait.until(EC.element_to_be_clickable((By.ID, "help-download")))
    download_button.click()

    time.sleep(3)

    after_files = set(Path(download_dir).glob("*"))
    new_files = after_files - before_files

    if new_files:
        new_file = max(new_files, key=lambda p: p.stat().st_ctime)

        def clean(value):
            return value.split(": ")[1].lower().replace(" ", "_")

        category_part = clean(data_category)
        zone_part = clean(bidding_zone)
        res_part = clean(resolution)
        start_dt_fmt = datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y%b%d").lower()
        end_dt_fmt = datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y%b%d").lower()
        file_ext = new_file.suffix

        filename = f"{category_part}_{zone_part}_{res_part}_{start_dt_fmt}_{end_dt_fmt}{file_ext}"
        new_file.rename(Path(download_dir) / filename)