/*
IMPORTANT NOTE: Replace [Insert File Path] with the full path to the file on your local machine.
*/

INSERT INTO zone_dim 
	(zone_name)
VALUES 
	('50Hertz'),
	('Amprion'),
	('TenneT'),
	('TransnetBW');

INSERT INTO month_dim (date)
SELECT
	generate_series('2015-01-01'::DATE, '2025-03-01'::DATE, INTERVAL '1 month')::DATE;

INSERT INTO day_dim (date)
SELECT
	generate_series('2015-01-05'::DATE, '2025-03-31'::DATE, INTERVAL '1 day')::DATE;

COPY production_type_actual
FROM '[Insert File Path]\cleaned_generation.csv'
DELIMITER ',' CSV HEADER;

COPY total_load
FROM '[Insert File Path]\cleaned_consumption.csv'
DELIMITER ',' CSV HEADER;

COPY congestion_costs
FROM '[Insert File Path]\cleaned_costs.csv'
DELIMITER ',' CSV HEADER;

COPY day_ahead_price
FROM '[Insert File Path]\cleaned_day_ahead_price.csv'
DELIMITER ',' CSV HEADER;

COPY price_stats
FROM '[Insert File Path]\cleaned_price_stats.csv'
DELIMITER ',' CSV HEADER;