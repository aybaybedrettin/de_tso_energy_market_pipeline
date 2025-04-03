-- TOTAL LOAD ACROSS ALL CONTROL ZONES, ALL TIME (JANUARY 2014 - FEBRUARY 2025)
SELECT 
	SUM(t.total_load) AS total_load_mwh
FROM 
	total_load t;



-- TOTAL LOAD BY CONTROL ZONE
SELECT 
	z.zone_name,
	ROUND(SUM(t.total_load)) AS total_load_mwh
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
		) / NULLIF(SUM(
			p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + 
			p.photovoltaics + p.other_renewable + p.hydro_pumped_storage +
			p.lignite + p.hard_coal + p.fossil_gas + 
			p.other_conventional + p.nuclear
		), 0), 1
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
	ROUND(SUM(t.total_load), 1) AS total_load_mwh,
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
	) - SUM(t.total_load), 1) AS surplus_mwh,
	ROUND(100.0 * (
		SUM(
			p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + 
			p.photovoltaics + p.other_renewable + p.hydro_pumped_storage +
			p.lignite + p.hard_coal + p.fossil_gas + 
			p.other_conventional + p.nuclear
		) - SUM(t.total_load)
	) / NULLIF(SUM(t.total_load), 0), 1) AS surplus_pct
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



-- VOLATILITY/MEDIAN PRICE AS VOLATILITY METRIC AND VOLATILITY LABELS
SELECT 
	m.date AS month,
	ROUND(p.volatility, 2) AS volatility,
	ROUND(p.median_price, 2) AS median_price,
	ROUND(p.volatility / NULLIF(p.median_price, 0), 2) AS volatility_ratio,
	CASE 
		WHEN p.volatility / NULLIF(p.median_price, 0) >= 0.5 THEN 'Very High'
		WHEN p.volatility / NULLIF(p.median_price, 0) < 0.5 AND p.volatility / NULLIF(p.median_price, 0) >= 0.35 THEN 'High'
		WHEN p.volatility / NULLIF(p.median_price, 0) < 0.35 AND p.volatility / NULLIF(p.median_price, 0) >= 0.2 THEN 'Moderate'
		WHEN p.volatility / NULLIF(p.median_price, 0) < 0.2 THEN 'Low'
		ELSE 'Undefined'
	END AS volatility_labels
FROM 
	price_stats p
INNER JOIN 
	month_dim m ON p.month_id = m.month_id
ORDER BY 
	month;