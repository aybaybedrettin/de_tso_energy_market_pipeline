-- DATA SETS TO BE IMPORTED TO POWER BI
-- EITHER CONNECT POWER BI TO THIS DATABASE AND OPEN THE PBIT FILE OR
-- DIRECTLY OPEN THE PBIX FILE
-----------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_tso_market_data AS
SELECT 
	m.date AS date,
	z.zone_name,
	-- Generation types
	p.biomass,
	p.hydropower,
	p.wind_offshore,
	p.wind_onshore,
	p.photovoltaics,
	p.other_renewable,
	p.lignite,
	p.hard_coal,
	p.fossil_gas,
	p.hydro_pumped_storage,
	p.other_conventional,
	p.nuclear,
	-- Total load
	t.grid_load + t.hydro_pumped_storage AS total_load,
	-- Congestion costs
	c.network_security_of_the_tsos + c.countertrading AS total_cost,
	-- Price stats
	ps.volatility,
	ps.min_price,
	ps.max_price,
	ps.median_price,
	-- Aggregates
	(p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + p.photovoltaics + p.other_renewable + p.hydro_pumped_storage) AS renewable_total,
	(p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + p.photovoltaics + p.other_renewable +
	 p.lignite + p.hard_coal + p.fossil_gas + p.hydro_pumped_storage + p.other_conventional + p.nuclear) AS production_total,
	ROUND((
			p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + p.photovoltaics + p.other_renewable + p.hydro_pumped_storage
		) /
				(
			p.biomass + p.hydropower + p.wind_offshore + p.wind_onshore + p.photovoltaics + p.other_renewable +
			p.lignite + p.hard_coal + p.fossil_gas + p.hydro_pumped_storage + p.other_conventional + p.nuclear
		),
		4
	) AS renewable_share,
	CASE 
		WHEN ps.volatility >= 0.5 THEN 'Very High'
		WHEN ps.volatility >= 0.35 THEN 'High'
		WHEN ps.volatility >= 0.2 THEN 'Moderate'
		ELSE 'Low'
	END AS VolatilityLabel
FROM production_type_actual p
INNER JOIN total_load t ON p.control_zone_id = t.control_zone_id AND p.month_id = t.month_id
INNER JOIN congestion_costs c ON p.control_zone_id = c.control_zone_id AND p.month_id = c.month_id
INNER JOIN month_dim m ON p.month_id = m.month_id
INNER JOIN zone_dim z ON p.control_zone_id = z.control_zone_id
INNER JOIN price_stats ps ON p.month_id = ps.month_id;
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_tso_market_data_unpivot AS
SELECT 
	zone_name,
	date,
	'biomass' AS production_type,
	biomass AS production_value,
	'Renewable' AS production_category
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'hydropower',
	hydropower,
	'Renewable'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'wind_offshore',
	wind_offshore,
	'Renewable'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'wind_onshore',
	wind_onshore,
	'Renewable'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'photovoltaics',
	photovoltaics,
	'Renewable'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'other_renewable',
	other_renewable,
	'Renewable'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'hydro_pumped_storage',
	hydro_pumped_storage,
	'Renewable'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'lignite',
	lignite,
	'Other'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'hard_coal',
	hard_coal,
	'Other'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'fossil_gas',
	fossil_gas,
	'Other'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'other_conventional',
	other_conventional,
	'Other'
FROM vw_tso_market_data
UNION ALL
SELECT 
	zone_name,
	date,
	'nuclear',
	nuclear,
	'Other'
FROM vw_tso_market_data;
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_price_data AS
SELECT 
	d.date,
	EXTRACT(YEAR FROM d.date) AS year,
	dap.price
FROM day_ahead_price dap
INNER JOIN day_dim d ON dap.day_id = d.day_id;
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_production_name_map AS
SELECT * FROM (
	VALUES 
	('biomass', 'Biomass'),
	('fossil_gas', 'Fossil Gas'),
	('hard_coal', 'Hard Coal'),
	('hydro_pumped_storage', 'Hydro (Pumped Storage)'),
	('hydropower', 'Hydropower'),
	('lignite', 'Lignite'),
	('nuclear', 'Nuclear'),
	('other_conventional', 'Other Conventional'),
	('other_renewable', 'Other Renewable'),
	('photovoltaics', 'Solar PV'),
	('wind_offshore', 'Wind (Offshore)'),
	('wind_onshore', 'Wind (Onshore)')
) AS mapping(production_type, label);
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_calendar AS
SELECT 
	date,
	EXTRACT(YEAR FROM date)::INT AS year,
	TO_CHAR(date, 'Month') AS month,
	EXTRACT(MONTH FROM date)::INT AS monthnumber,
	TO_CHAR(date, 'Mon YYYY') AS monthyear
FROM day_dim
ORDER BY date;
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_calendar_month AS
SELECT
	month_id,
	date AS first_day_of_month,
	EXTRACT(YEAR FROM date) AS year,
	TO_CHAR(date, 'Month') AS month_name,
	EXTRACT(MONTH FROM date) AS month_number,
	TO_CHAR(date, 'Mon YYYY') AS month_year_label
FROM month_dim
ORDER BY date;