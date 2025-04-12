import pandas as pandas
from pathlib import Path

def clean_energy_dataset(
    input_prefix: str,
    output_name: str,
    start_date: str,
    end_date: str,
    raw_dir: str = "data/raw",
    output_dir: str = "data/cleaned"
):
    """
    General-purpose cleaning function for energy datasets from SMARD.de.

    Parameters:
        input_prefix (str): Prefix of files to process (e.g., 'actual_generation', 'actual_consumption').
        output_name (str): Output filename suffix, used in 'cleaned_{output_name}.csv'.
        start_date (str): Earliest date to keep, format: 'YYYY-MM-DD'.
        end_date (str): Latest date to keep (exclusive), format: 'YYYY-MM-DD'.
        raw_dir (str): Path to the raw data directory.
        output_dir (str): Path to the cleaned data output directory.
    """

    raw_path = Path(raw_dir)
    cleaned_path = Path(output_dir)
    cleaned_path.mkdir(parents=True, exist_ok=True)

    files = list(raw_path.glob(f"{input_prefix}_*_month_*.csv"))

    dfs = []
    for file in files:
        tso_name = file.name.split("_month_")[0].split("_")[-1]

        df = pandas.read_csv(file, delimiter=";", thousands=",")

        df["tso"] = tso_name
        dfs.append(df)

    df_all = pandas.concat(dfs, ignore_index=True)

    # Combine date columns into one
    df_all["date"] = pandas.to_datetime(df_all["Start date"])
    df_all = df_all.drop(columns=["Start date", "End date"])

    # Remove commas as thousand separator
    df_all = df_all.applymap(
        lambda x: x.replace(",", "") if isinstance(x, str) else x
    )

    # Clean column names
    df_all.columns = [
        col.split(" [")[0].lower().replace(" ", "_") if col not in ["date", "tso"] else col
        for col in df_all.columns
    ]

    # Cutoff by date
    df_all = df_all[(df_all["date"] >= start_date) & (df_all["date"] < end_date)]

    # Replace non-numeric values with 0
    df_all = df_all.replace("-", 0).fillna(0)

    # Convert to float
    value_columns = df_all.columns.difference(["date", "tso"])
    df_all[value_columns] = df_all[value_columns].astype(float)

    # Create zone and date ids
    zone_map = {"50hertz": 1, "amprion": 2, "tennet": 3, "transnetbw": 4}
    df_all["control_zone_id"] = df_all["tso"].map(zone_map)

    unique_months = pandas.Series(sorted(df_all["date"].unique()))
    month_id_map = {date: idx + 1 for idx, date in enumerate(unique_months)}
    df_all["month_id"] = df_all["date"].map(month_id_map)

    # Final structure
    cols = ["control_zone_id", "month_id"] + [
        col for col in df_all.columns if col not in ["control_zone_id", "month_id", "tso", "date"]
    ]
    df_all = df_all[cols]
    df_all.reset_index(drop=True, inplace=True)

    # Remove the aggregation column from load data set as it is redundant
    if "grid_load_incl._hydro_pumped_storage" in df_all.columns:
        df_all.drop(columns=["grid_load_incl._hydro_pumped_storage"], inplace=True)

    # Export
    output_path = cleaned_path / f"{output_name}.csv"
    df_all.to_csv(output_path, index=False)