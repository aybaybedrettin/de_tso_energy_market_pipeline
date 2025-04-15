# This script orchestrates data scraping and cleaning for the DE energy dashboard project.
# Make sure chromedriver.exe is in path for selenium.

from python_scripts.fetch_smard import setup_driver, download_dataset
import time
# ------------------------------------------------------------
# Data Scraping
# ------------------------------------------------------------
# Define the arguments to scrape actual generation, total load, congestion management costs, and price data
# Global settings
START_DATE = "01/01/2015"
END_DATE = "04/09/2025"
FILETYPE = "CSV"
# Specific settings
TSOS = [
    "Control Area (DE): 50Hertz",
    "Control Area (DE): Amprion",
    "Control Area (DE): TenneT",
    "Control Area (DE): TransnetBW"
]
download_jobs = []
# Actual electricity generation for each TSO, monthly
for tso in TSOS:
    download_jobs.append({
        "main_category": "Main category: Electricity generation",
        "data_category": "Data category: Actual generation",
        "bidding_zone": tso,
        "resolution": "Resolution: Month"
    })
# Actual total load for each TSO, monthly
for tso in TSOS:
    download_jobs.append({
        "main_category": "Main category: Electricity consumption",
        "data_category": "Data category: Actual consumption",
        "bidding_zone": tso,
        "resolution": "Resolution: Month"
    })
# Actual congestion management costs for each TSO, monthly
for tso in TSOS:
    download_jobs.append({
        "main_category": "Main category: Balancing",
        "data_category": "Data category: Costs of TSOs (without costs of DSOs)",
        "bidding_zone": tso,
        "resolution": "Resolution: Month"
    })
# Day-ahead prices for Germany, daily
download_jobs.append({
    "main_category": "Main category: Market",
    "data_category": "Data category: Day-ahead prices",
    "bidding_zone": "Country: Germany",
    "resolution": "Resolution: Day"
})
# The download loop
driver = setup_driver()
try:
    for job in download_jobs:
        download_dataset(
            driver=driver,
            main_category=job["main_category"],
            data_category=job["data_category"],
            bidding_zone=job["bidding_zone"],
            start_date=START_DATE,
            end_date=END_DATE,
            resolution=job["resolution"],
            filetype=FILETYPE
        )
finally:
    driver.quit()
    time.sleep(5) # Otherwise the price data is sometimes left out of cleaning
# ------------------------------------------------------------
# Data cleaning
# ------------------------------------------------------------
# TSO level data
from python_scripts.cleaner_tso import clean_energy_dataset

clean_energy_dataset(
    input_prefix="actual_generation",
    output_name="cleaned_generation",
    start_date="01.01.2015",
    end_date="31.03.2025"
)

clean_energy_dataset(
    input_prefix="actual_consumption",
    output_name="cleaned_consumption",
    start_date="01.01.2015",
    end_date="31.03.2025"
)

clean_energy_dataset(
    input_prefix="costs_of_tsos",
    output_name="cleaned_costs",
    start_date="01.01.2015",
    end_date="31.03.2025"
)

# Price data
from python_scripts.cleaner_price import clean_day_ahead_price

clean_day_ahead_price(
    input_file_name="day-ahead_prices_germany_day_2015jan01_2025apr09.csv",
    start_date="05.01.2015",
    end_date="31.03.2025"
)