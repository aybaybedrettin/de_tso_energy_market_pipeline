-- TOTAL LOAD ACROSS ALL CONTROL ZONES, ALL TIME (JANUARY 2014 - FEBRUARY 2025)
SELECT 
	SUM(t.grid_load + t.hydro_pumped_storage) AS total_load_mwh
FROM 
	total_load t;



-- TOTAL LOAD BY CONTROL ZONE
SELECT 
	z.zone_name,
	ROUND(SUM(t.grid_load + t.hydro_pumped_storage)) AS total_load_mwh
FROM 
	total_load t
INNER JOIN 
	zone_dim z ON t.control_zone_id = z.control_zone_id
GROUP BY 
	z.zone_name
ORDER BY 
	total_load_mwh DESC;



-- GENERATION PER PRODUCTION TYPE, PERCENTAGE OF RENEWABLES IN GENERATION FOR CONTROL ZONES
SELECT 
	z.zone_name,
	ROUND(SUM(
		p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + 
		p.photovoltaics + p.other_renewable + p.hydro_pumped_storage
	), 1) AS renewable_mwh,
	ROUND(SUM(
		p.lignite + p.hard_coal + p.fossil_gas + 
		p.other_conventional + p.nuclear
	), 1) AS non_renewable_mwh,
	ROUND(
		100.0 * SUM(
			p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + 
			p.photovoltaics + p.other_renewable + p.hydro_pumped_storage
		) / SUM(
			p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + 
			p.photovoltaics + p.other_renewable + p.hydro_pumped_storage +
			p.lignite + p.hard_coal + p.fossil_gas + 
			p.other_conventional + p.nuclear
		), 1
	) AS renewable_share_pct
FROM 
	production_type_actual p
INNER JOIN 
	zone_dim z ON p.control_zone_id = z.control_zone_id
GROUP BY 
	z.zone_name
ORDER BY 
	renewable_share_pct DESC;



-- TOTAL LOAD VERSUS TOTAL GENERATION, CONTROL ZONE ELECTRICITY SURPLUS
SELECT 
	z.zone_name,
	ROUND(SUM(t.grid_load + t.hydro_pumped_storage), 1) AS total_load_mwh,
	ROUND(SUM(
		p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + 
		p.photovoltaics + p.other_renewable + p.hydro_pumped_storage +
		p.lignite + p.hard_coal + p.fossil_gas + 
		p.other_conventional + p.nuclear
	), 1) AS total_generation_mwh,
	ROUND(SUM(
		p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + 
		p.photovoltaics + p.other_renewable + p.hydro_pumped_storage +
		p.lignite + p.hard_coal + p.fossil_gas + 
		p.other_conventional + p.nuclear
	) - SUM(t.grid_load + t.hydro_pumped_storage), 1) AS surplus_mwh,
	ROUND(100.0 * (
		SUM(
			p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + 
			p.photovoltaics + p.other_renewable + p.hydro_pumped_storage +
			p.lignite + p.hard_coal + p.fossil_gas + 
			p.other_conventional + p.nuclear
		) - SUM(t.grid_load + t.hydro_pumped_storage)
	) / SUM(t.grid_load + t.hydro_pumped_storage), 1) AS surplus_pct
FROM 
	total_load t
INNER JOIN 
	zone_dim z ON t.control_zone_id = z.control_zone_id
INNER JOIN 
	production_type_actual p ON t.control_zone_id = p.control_zone_id AND t.month_id = p.month_id
GROUP BY 
	z.zone_name
ORDER BY 
	surplus_pct DESC;



-- ADD THE MIN/MAX/MEDIAN PRICE COLUMNS TO PRICE STATS
ALTER TABLE price_stats
ADD COLUMN min_price NUMERIC,
ADD COLUMN max_price NUMERIC,
ADD COLUMN median_price NUMERIC;

WITH price_with_month AS (
    SELECT
        dap.day_id,
        dap.price,
        md.month_id
    FROM day_ahead_price dap
    JOIN day_dim dd ON dap.day_id = dd.day_id
    JOIN month_dim md ON date_trunc('month', dd.date) = md.date
),
aggregates AS (
    SELECT
        month_id,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median_price
    FROM price_with_month
    GROUP BY month_id
)
UPDATE price_stats ps
SET 
    min_price = agg.min_price,
    max_price = agg.max_price,
    median_price = agg.median_price
FROM aggregates agg
WHERE ps.month_id = agg.month_id;



-- VOLATILITY/AVG PRICE AS VOLATILITY METRIC AND VOLATILITY LABELS
SELECT 
	m.date AS month,
	volatility,
	CASE 
		WHEN p.volatility  >= 0.5 THEN 'Very High'
		WHEN p.volatility  >= 0.35 THEN 'High'
		WHEN p.volatility  >= 0.2 THEN 'Moderate'
		ELSE 'Low'
	END AS volatility_labels
FROM 
	price_stats p
INNER JOIN 
	month_dim m ON p.month_id = m.month_id
ORDER BY 
	month;