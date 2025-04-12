import pandas as pandas

def clean_day_ahead_price(input_file_name, start_date, end_date):
    """
    Cleans Germany day-ahead price data from SMARD and computes monthly volatility.
    Volatility is computed by the monthly standard deviation of price divided by monthly average price(coefficient of variation)

    Parameters:
        input_file_name (str): File name in data/raw/ (e.g., "day-ahead_prices_germany_day_2015jan01_2025apr09.csv")
        start_date (str): Start date for keeping data, in "DD.MM.YYYY" format
        end_date (str): End date for keeping data, in "DD.MM.YYYY" format

    Outputs:
        - cleaned_day_ahead_price.csv: daily prices with day_id
        - cleaned_price_stats.csv: monthly volatility metric
    """
    df_price = pandas.read_csv(f"data/raw/{input_file_name}", delimiter=";")

    df_price["date"] = pandas.to_datetime(df_price["Start date"])
    df_price = df_price.drop(columns=["Start date", "End date"])

    col1 = "DE/AT/LU [€/MWh] Calculated resolutions"
    col2 = "Germany/Luxembourg [€/MWh] Calculated resolutions"
    df_price[col1] = df_price[col1].replace("-", 0)
    df_price[col2] = df_price[col2].replace("-", 0)
    df_price["price"] = df_price[col1].astype(float) + df_price[col2].astype(float)
    df_price = df_price[["date", "price"]]

    df_price = df_price[df_price["date"] >= pandas.to_datetime(start_date, format="%d.%m.%Y")]
    df_price = df_price[df_price["date"] < pandas.to_datetime(end_date, format="%d.%m.%Y")]
    df_price = df_price.reset_index(drop=True)

    unique_days = pandas.Series(sorted(df_price["date"].unique()))
    day_id_map = {day: idx + 1 for idx, day in enumerate(unique_days)}
    df_price["day_id"] = df_price["date"].map(day_id_map)
    df_price = df_price[["day_id", "price"]]

    month_groups = df_price["day_id"].map(lambda i: unique_days[i - 1].to_period("M"))
    unique_months = pandas.Series(sorted(month_groups.unique()))
    month_id_map = {period: idx + 1 for idx, period in enumerate(unique_months)}

    df_volatility = (
        df_price.copy()
        .assign(month_period=month_groups)
        .assign(month_id=lambda df: df["month_period"].map(month_id_map))
        .groupby("month_id")["price"]
        .agg(["std", "mean"])
        .rename(columns={"std": "std_dev", "mean": "avg_price"})
        .assign(volatility=lambda x: x["std_dev"] / x["avg_price"])
        .reset_index()[["month_id", "volatility"]]
    )

    df_price.to_csv("data/cleaned/cleaned_day_ahead_price.csv", index=False)
    df_volatility.to_csv("data/cleaned/cleaned_price_stats.csv", index=False)
