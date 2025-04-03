"""
The script;
- Aggregates CSVs
- Cleans and standardizes column names and formats
- Maps control zones and months to IDs for normalization of tables in SQL
- Exports cleaned data to CSV

The data sources are;
ENTSO-E Transparency Platform: (https://transparency.entsoe.eu)
SMARD: (https://www.smard.de)

Before running, install required packages with:
    pip install -r requirements.txt
"""

import pandas
import glob
import os

# ------------------------------------------------------------
# Load and combine raw CSVs for actual generation by production type
# ------------------------------------------------------------
production_by_type = pandas.concat(
    [
        pandas.read_csv(f, sep=";", thousands=",", decimal=".").assign(
            control_zone=os.path.splitext(os.path.basename(f))[0]
        )
        for f in glob.glob("data/raw/actual_generation_per_production_type/*.csv")
    ],
    ignore_index=True,
    sort=False,
).fillna(0)

# ------------------------------------------------------------
# Convert first column to datetime and rename
# ------------------------------------------------------------
production_by_type.iloc[:, 0] = (
    pandas.to_datetime(production_by_type.iloc[:, 0], format="%b %d, %Y")
    .dt.to_period("M")
    .dt.to_timestamp()
)

production_by_type.rename(columns={production_by_type.columns[0]: "date"}, inplace=True)

# ------------------------------------------------------------
# Drop unnecessary columns and clean column names
# ------------------------------------------------------------
production_by_type.drop(
    production_by_type.columns[1], axis=1, inplace=True
)  # Drop 'End date'

production_by_type.columns = [
    col.split(" [")[0] if col not in ["date", "control_zone"] else col
    for col in production_by_type.columns
]

production_by_type.columns = [
    col.replace(" ", "_") for col in production_by_type.columns
]

# ------------------------------------------------------------
# Handle missing or non-numeric values and convert to float
# ------------------------------------------------------------
production_by_type.replace("-", 0, inplace=True)
production_by_type.fillna(0, inplace=True)

for col in production_by_type.columns:
    if col not in ["date", "control_zone"]:
        production_by_type[col] = (
            production_by_type[col]
            .astype(str)
            .replace("-", "0")
            .str.replace(",", "")
            .astype(float)
        )

# ------------------------------------------------------------
# Reorder and reformat date and columns
# ------------------------------------------------------------
production_by_type["date"] = pandas.to_datetime(production_by_type["date"])
production_by_type["date"] = (
    production_by_type["date"].dt.to_period("M").dt.to_timestamp()
)

production_by_type = production_by_type[
    ["date", "control_zone"]
    + [col for col in production_by_type.columns if col not in ["date", "control_zone"]]
]

# ------------------------------------------------------------
# Map control zone and month to integer IDs for SQL
# ------------------------------------------------------------
zone_map = {"50Hertz": 1, "Amprion": 2, "TenneT": 3, "TransnetBW": 4}
production_by_type["control_zone_id"] = production_by_type["control_zone"].map(zone_map)

unique_dates = sorted(production_by_type["date"].unique())
date_id_map = {date: idx + 1 for idx, date in enumerate(unique_dates)}
production_by_type["month_id"] = production_by_type["date"].map(date_id_map)

# Drop text columns after mapping
production_by_type.drop(columns=["control_zone", "date"], inplace=True)

# Reorder columns with IDs at the front
cols = ["control_zone_id", "month_id"] + [
    col
    for col in production_by_type.columns
    if col not in ["control_zone_id", "month_id"]
]
production_by_type = production_by_type[cols]

# ------------------------------------------------------------
# Save cleaned data to CSV
# ------------------------------------------------------------
production_by_type.to_csv("data/cleaned/production_by_type.csv", index=False)


# ------------------------------------------------------------
# STEP 2: Clean and aggregate total load data
# Maps control zones and months to IDs,
# and prepares the dataset for export.
# ------------------------------------------------------------

# Load and concatenate raw CSVs for total load
total_load = pandas.read_csv(
    "data/raw/actual_total_load.csv", sep=",", decimal="."
)

# Reorder columns
total_load = total_load[["date", "control_zone", "total_load"]]

# Map control zones and months to integer IDs
zone_map = {"50Hertz": 1, "Amprion": 2, "TenneT": 3, "TransnetBW": 4}
total_load["control_zone_id"] = total_load["control_zone"].map(zone_map)

unique_dates = sorted(total_load["date"].unique())
date_id_map = {date: idx + 1 for idx, date in enumerate(unique_dates)}
total_load["month_id"] = total_load["date"].map(date_id_map)

# Drop original labels
total_load.drop(columns=["control_zone", "date"], inplace=True)

# Reorder columns for export
cols = ["control_zone_id", "month_id"] + [
    col
    for col in total_load.columns
    if col not in ["control_zone_id", "month_id"]
]
total_load = total_load[cols]

# Save cleaned dataset
total_load.to_csv("data/cleaned/total_load.csv", index=False)


# ------------------------------------------------------------
# STEP 3: Clean congestion management cost data
#
# Loads ENTSO-E monthly congestion costs for German control zones,
# filters and renames zones, formats dates, maps IDs for SQL export,
# and saves cleaned dataset.
# ------------------------------------------------------------

# Load and combine raw CSVs for congestion management costs
congestion_costs = pandas.concat(
    [
        pandas.read_csv(f, sep="\t", decimal=".")
        for f in glob.glob("data/raw/costs_of_congestion_management/*.csv")
    ],
    ignore_index=True,
)

# Filter for relevant German control zones
valid_zones = ["DE_TransnetBW", "DE_TenneT_GER", "DE_Amprion", "DE_50HzT"]
congestion_costs = congestion_costs[congestion_costs["MapCode"].isin(valid_zones)]

# Rename zone codes to readable names
zone_map = {
    "DE_TransnetBW": "TransnetBW",
    "DE_TenneT_GER": "TenneT",
    "DE_Amprion": "Amprion",
    "DE_50HzT": "50Hertz",
}
congestion_costs["MapCode"] = congestion_costs["MapCode"].map(zone_map)
congestion_costs.rename(columns={"MapCode": "control_zone"}, inplace=True)

# Keep only relevant columns
congestion_costs = congestion_costs[
    [
        "DateTime",
        "control_zone",
        "TotalCost",
        "RedispatchingCosts",
        "CountertradingCosts",
    ]
]

# Rename columns for clarity
congestion_costs.rename(
    columns={
        "DateTime": "date",
        "TotalCost": "total_cost",
        "RedispatchingCosts": "redispatching_cost",
        "CountertradingCosts": "countertrading_cost",
    },
    inplace=True,
)

# Convert and standardize date column to monthly timestamps
congestion_costs["date"] = pandas.to_datetime(congestion_costs["date"])
congestion_costs["date"] = congestion_costs["date"].dt.to_period("M").dt.to_timestamp()
congestion_costs = congestion_costs[congestion_costs["date"] >= "2015-01-01"]

# Map control zones and dates to integer IDs for SQL
zone_map = {"50Hertz": 1, "Amprion": 2, "TenneT": 3, "TransnetBW": 4}
congestion_costs["control_zone_id"] = congestion_costs["control_zone"].map(zone_map)

unique_dates = sorted(congestion_costs["date"].unique())
date_id_map = {date: idx + 1 for idx, date in enumerate(unique_dates)}
congestion_costs["month_id"] = congestion_costs["date"].map(date_id_map)

# Drop original text columns after mapping
congestion_costs.drop(columns=["control_zone", "date"], inplace=True)

# Reorder columns for export
cols = ["control_zone_id", "month_id"] + [
    col
    for col in congestion_costs.columns
    if col not in ["control_zone_id", "month_id"]
]
congestion_costs = congestion_costs[cols]

# Save cleaned dataset
congestion_costs.to_csv("data/cleaned/congestion_costs.csv", index=False)


# ------------------------------------------------------------
# STEP 4: Clean and process day-ahead electricity prices
#
# Loads SMARD price data for Germany/Luxembourg,
# normalizes overlapping columns, computes monthly statistics
# and volatility, assigns IDs, and exports daily & monthly datasets.
# ------------------------------------------------------------

# Load raw price data
day_ahead_price = pandas.read_csv(
    "data/raw/day_ahead_prices.csv", sep=";", decimal=".", thousands=","
)

# Rename relevant columns
day_ahead_price.rename(
    columns={
        "Start date": "date",
        "Germany/Luxembourg [€/MWh] Calculated resolutions": "price2",
        "DE/AT/LU [€/MWh] Calculated resolutions": "price1",
    },
    inplace=True,
)

# Keep only necessary columns
day_ahead_price = day_ahead_price[["date", "price1", "price2"]]

# Clean and merge price columns
day_ahead_price[["price1", "price2"]] = day_ahead_price[["price1", "price2"]].replace(
    "-", pandas.NA
)
day_ahead_price["price1"] = pandas.to_numeric(day_ahead_price["price1"])
day_ahead_price["price2"] = pandas.to_numeric(day_ahead_price["price2"])
day_ahead_price["price"] = day_ahead_price["price1"].combine_first(
    day_ahead_price["price2"]
)

# Drop individual price columns and NAs
day_ahead_price.drop(columns=["price1", "price2"], inplace=True)
day_ahead_price = day_ahead_price.dropna(subset=["price"]).reset_index(drop=True)

# Parse date and filter to < March 2025
day_ahead_price["date"] = pandas.to_datetime(
    day_ahead_price["date"], format="%b %d, %Y"
)
day_ahead_price = day_ahead_price[day_ahead_price["date"] < "2025-03-01"]

# ------------------------------------------------------------
# Compute monthly price statistics and volatility
# ------------------------------------------------------------
price_stats_df = day_ahead_price.copy()
price_stats_df["month"] = price_stats_df["date"].dt.to_period("M").dt.to_timestamp()

monthly_price_stats = (
    price_stats_df.groupby("month")["price"]
    .agg(volatility="std", max_price="max", min_price="min", median_price="median")
    .reset_index()
)

# Assign month IDs for SQL export
unique_months = sorted(monthly_price_stats["month"].unique())
month_id_map = {month: idx + 1 for idx, month in enumerate(unique_months)}
monthly_price_stats["month_id"] = monthly_price_stats["month"].map(month_id_map)

# Reorder columns
monthly_price_stats = monthly_price_stats[
    ["month_id", "volatility", "max_price", "min_price", "median_price"]
]

# ------------------------------------------------------------
# Assign day IDs to individual daily prices
# ------------------------------------------------------------
unique_dates = sorted(day_ahead_price["date"].unique())
date_id_map = {date: idx + 1 for idx, date in enumerate(unique_dates)}
day_ahead_price["day_id"] = day_ahead_price["date"].map(date_id_map)

day_ahead_price.drop(columns=["date"], inplace=True)
day_ahead_price = day_ahead_price[["day_id", "price"]]

# ------------------------------------------------------------
# Save both daily and monthly price data
# ------------------------------------------------------------
day_ahead_price.to_csv("data/cleaned/day_ahead_price.csv", index=False)
monthly_price_stats.to_csv("data/cleaned/monthly_price_stats.csv", index=False)