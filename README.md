# Important note: If selenium fails, try adding chromedriver.exe to path
# German Energy Market Data Pipeline(2015-2025)

This project builds a fully automated data pipeline for downloading, cleaning, storing, and visualizing multiple data sets from Germany's electricity market. It integrates publicly available data from SMARD.de with a PostgreSQL database and a Power BI dashboard, to conduct an analysis of trends in production, consumption, costs, and prices across the four German control zones.

---

## Project Structure

```
de_energy_pipeline/
│
├── dashboard/               # Power BI visuals (.pbix, .pbit)
│   ├── EnergyDashboard.pbix
│   ├── EnergyDashboardTemplate.pbit
│   ├── screenshots/
│   └── README.md
│
├── data/
│   ├── raw/                 # Raw CSV files downloaded via Selenium
│   └── cleaned/             # Cleaned datasets ready for database insertion
│
├── python_scripts/          # Data scraping and cleaning logic
│   ├── fetch_smard.py
│   ├── cleaner_tso.py
│   ├── cleaner_price.py
│
├── sql_scripts/             # PostgreSQL schema, data insertion, analysis views, Power BI preparation
│   ├── 00_create_table.sql
│   ├── 01_insert_table.sql
│   ├── 02_analysis.sql
│   └── 03_export_data.sql
│
├── main.py                  # Orchestrates full scraping and cleaning workflow
├── requirements.txt         # Required Python packages
└── README.md                # (You are here)
```

---

## Features

- **Automated Data Downloading**  
  Uses Selenium to interact with SMARD.de and download electricity generation, consumption, price, and congestion cost data sets.

- **Cleaned and Structured Data**  
  Custom scripts clean raw CSV files and format them for structured use in SQL and Power BI.

- **Relational Database Design**  
  A PostgreSQL schema organizes time, control zones, energy types, and prices across normalized dimension tables.

- **Power BI Dashboard**  
  Dynamic visualizations and KPI cards provide insights into Germany’s energy production mix, load trends, cost structures, and price volatility.

---

## Technologies Used

- **Python 3**: for scripting and automation  
- **Selenium**: for data scraping from SMARD.de  
- **Pandas**: for data cleaning and transformation  
- **PostgreSQL**: for structured storage and querying  
- **Power BI**: for dashboard development and data visualization

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/aybaybedrettin/de_energy_pipeline.git
cd de_energy_pipeline
```

### 2. Set Up Python Environment (Windows)

In your terminal (VS Code, PyCharm, or command line), run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Data Pipeline
This script downloads and cleans the entire dataset.

```bash
python main.py
```
The output will be placed in the `data/cleaned/` folder.

### 4. Set Up PostgreSQL
- Create a new database (e.g., `energy_data`)
- Run the SQL files in this order:
  1. `00_create_table.sql`
  2. `01_insert_table.sql`
  3. `02_analysis.sql`
  4. `03_export_data.sql`


### 5. Load the Power BI Dashboard
- Open `dashboard/de_energy_dashboard.pbit` in Power BI.
- When prompted, enter your PostgreSQL connection details (host, port, database, username, password).
- The dashboard will connect directly to your live database and populate with data.

---

## Data Source

All data used in this project is publicly available from [SMARD.de](https://www.smard.de/).

---

## Contact

For questions feel free to reach out:

- GitHub: [aybaybedrettin](https://github.com/aybaybedrettin)
- Email: aybaybedrettin@gmail.com

---