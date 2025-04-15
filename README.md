# German Energy Market Data Pipeline (2015–2025)

This project builds a fully automated data pipeline for downloading, cleaning, storing, and visualizing electricity market data from Germany. It integrates public data from [SMARD.de](https://www.smard.de/) with a PostgreSQL database and an interactive Power BI dashboard to analyze production, consumption, congestion costs, and electricity prices across Germany’s four control zones.

---

## Project Structure

```text
de_energy_pipeline/
│
├── dashboard/               # Power BI files, screenshots and README for the visuals
│   ├── de_energy_dashboard.pbix
│   ├── de_energy_dashboard.pbit
│   ├── screenshots/
│   └── README.md
│
├── data/
│   ├── raw/                 # Raw CSV files downloaded via Selenium
│   └── cleaned/             # Cleaned data sets
│
├── python_scripts/          # Data scraping and cleaning logic
│   ├── fetch_smard.py
│   ├── cleaner_tso.py
│   ├── cleaner_price.py
│
├── sql_scripts/             # PostgreSQL schema and SQL transformations
│   ├── 00_create_table.sql
│   ├── 01_analysis.sql
│   └── 02_export_data.sql
│
├── main.py                  # Orchestrates full scraping and cleaning workflow
├── insert_to_sql.py         # Insertion of cleaned data into PostgreSQL
├── requirements.txt         # Required Python packages
└── README.md
```

---

## Features

- **Automated Data Downloading**  
  Uses Selenium to interact with SMARD.de and download electricity generation, consumption, price, and congestion cost data sets.

- **Cleaned and Structured Data**  
  Custom Python scripts clean and structure the data using pandas.

- **Relational Database Design**  
  A PostgreSQL schema organizes time, control zones, energy types, and prices into normalized tables.

- **Database Insertion with GUI**  
  A standalone Python script allows users to insert the cleaned CSVs into their PostgreSQL database via a simple popup login window.

- **Interactive Power BI Dashboard**  
  Dynamic visualizations and KPIs provide insights into Germany’s production mix, load trends, cost structures, and price volatility.

---

## Technologies Used

- **Python 3.13** – scripting and automation  
- **Selenium** – scraping from SMARD.de  
- **pandas** – data wrangling  
- **PostgreSQL** – structured storage and SQL queries  
- **Power BI** – visualization and analysis

---

## Setup Instructions

### 1. Clone the Repository  
(Requires Git to be installed: https://git-scm.com/downloads)  
*Make sure you're not inside another Python project or virtual environment.*

```bash
git clone https://github.com/aybaybedrettin/de_tso_energy_market_pipeline.git
cd de_tso_energy_market_pipeline
```

### 2. Set Up Python Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Data Pipeline

This script downloads and cleans the entire dataset:

```bash
python main.py      # Windows
python3 main.py     # Mac/Linux
```

Cleaned outputs will appear in the `data/cleaned/` folder.

### 4. Set Up PostgreSQL

- Create a new database (e.g., `de_energy`) in your PostgreSQL setup.
- Run the schema creation script "sql_scripts/00_create_table.sql" in your database client (DBeaver, pgAdmin, VSCode etc.).


### 5. Insert Data into PostgreSQL using Python

```bash
python insert_to_sql.py      # Windows
python3 insert_to_sql.py     # Mac/Linux
```

You’ll be prompted via popup to enter with default in brackets:

- Host (localhost)
- Port (5432)
- Username (postgres)
- Password
- Database name

If credentials are correct, the script will populate both dimension and fact tables from the cleaned CSVs.

### 6. Run the SQL analysis and view scripts
- Run the scripts "01_analysis.sql" and "02_export_data.sql" in the sql_scripts folder.

### 7. Load the Power BI Dashboard

- Open `dashboard/de_energy_dashboard.pbit` in Power BI Desktop.
- When prompted, enter your PostgreSQL credentials.
- The dashboard will automatically load from your live database.
- Alternatively, simply open the `dashboard/de_energy_dashboard.pbix` in Power BI.

---

## Data Source

All data used in this project is publicly available from [SMARD.de](https://www.smard.de/).

---

## Common Issues

- If Selenium fails, make sure `chromedriver` is installed and available in your system PATH.  
  - On Windows: download `chromedriver.exe`, place it in a known folder, and add that folder to your Environment Variables.  
  - On macOS/Linux: install with `brew install chromedriver` or use a package manager.

---

## Contact

- GitHub: [aybaybedrettin](https://github.com/aybaybedrettin)  
- Email: aybaybedrettin@gmail.com