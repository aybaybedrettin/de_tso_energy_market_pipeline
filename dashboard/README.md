# Power BI Dashboard
This folder contains screenshots of the interactive Power BI dashboard built for the Germany Energy Market and TSO Analysis project.
Due to limitations in sharing Power BI dashboards publicly, the interactive version cannot be hosted online. However, images of the final dashboard views are provided below. I am happy to demonstrate the dashboard live upon request.

## Dashboard Overview
The dashboard provides monthly insights (2015–2025) into electricity production, load, price, and congestion management across Germany’s four Transmission System Operators:

- **50Hertz**
- **TenneT**
- **Amprion**
- **TransnetBW**

It includes a control area selector, year/month filters, and KPIs.

---
## Elements Displayed
### 1. **Map and TSO Selector**
An interactive map highlights the selected TSO. Four buttons allow filtering the dashboard by TSO (or viewing all zones together).

### 2. **Generation Type Breakdown**
A bar chart shows the top 3 generation sources (e.g., Lignite, Wind, Gas) by MWh produced within the selected area and time frame.

### 3. **Renewable Share**
A KPI card displays the share of renewables (biomass, wind, solar, hydro, etc.) in total electricity production.

### 4. **Total Load and Congestion Costs**
- **Total Load in MWh**: Energy demand in the selected control zone and time period.
- **Costs of Congestion Management**: Redispatching + countertrading costs in the selected zone and time period.

### 5. **Electricity Price Statistics**
Four KPIs:
- **Lowest price** (€/MWh)
- **Highest price**
- **Median price**
- **Volatility Measure**: Ratio of price volatility to median price, categorized as:
  - ≥ 0.50 → *Very High*
  - 0.35–0.50 → *High*
  - 0.20–0.35 → *Moderate*
  - < 0.20 → *Low*

### 6. **Electricity Price Over Time**
A line chart tracks electricity prices across the selected period. Users can observe spikes during energy crises or dips in low demand months.
