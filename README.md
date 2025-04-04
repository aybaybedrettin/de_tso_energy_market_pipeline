# Germany Energy Market Analysis (2015–2025)
This project analyzes Germany's electricity production, load, and price dynamics across its four transmission system operators(TSOs): Amprion, TenneT, 50Hertz, and TransnetBW.
It includes a complete pipeline from raw data cleaning in Python to analysis and maintenance in SQL and a dashboard in Power BI.


## The pipeline
- Cleaned and transformed 10 years of data
- Structured PostgreSQL schema with fact and dimension tables
- SQL based analysis of renewable share, production vs. load balance, and price volatility
- Power BI dashboard with interactive insights by control zone, year and month


## Folder Structure
    dashboard/        # The .pbix file, images from the dashboard and README
    data/
        raw/          # Raw input data sets(actual total load has been trimmed due to its initial size)
        cleaned/      # Python cleaned data ready for SQL
        ready/        # Data sets generated in SQL for Power BI
    sql/              # SQL scripts(run in order)
    LICENSE           # Project license (MIT)
    main.py           # Python script for data cleaning
    README.md         # README
    requirements.txt  # Python dependencies


## Project setup and versions used
- Python==3.13.2
- pandas==2.2.3
- PostgreSQL

Install Python dependencies with:
pip install -r requirements.txt


## Data Sources
All data used in this project is public:
- ENTSO-E Transparency Platform: https://transparency.entsoe.eu
- SMARD – Bundesnetzagentur: https://www.smard.de


## Dashboard
Due to Power BI publishing restrictions, the interactive dashboard could only be shared with the source file.  
Screenshots of the final version are available in the `dashboard/` folder.

I am happy to demonstrate the dashboard interactively upon request.

## SQL Notes
- Create a postgres database and make sure it is selected as the default
- Make sure that the scripts are connected to the appropriate database
- To read the data, replace "[Insert File Path]"
- Export the tables from the last script to csv


## This project is designed to be reproducible:
- All data cleaning is handled in Python
- SQL logic is included and documented
- Publicly shareable datasets are included directly

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
