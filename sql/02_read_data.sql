/*
IMPORTANT NOTE: Replace [Insert File Path] with the full path to the file on your local machine.

COPY production_type_actual FROM '[Insert File Path]\production_by_type.csv' DELIMITER ',' CSV HEADER;

COPY total_load FROM '[Insert File Path]\total_load.csv' DELIMITER ',' CSV HEADER;

COPY congestion_costs FROM '[Insert File Path]\congestion_costs.csv' DELIMITER ',' CSV HEADER;

COPY price_stats FROM '[Insert File Path]\monthly_price_stats.csv' DELIMITER ',' CSV HEADER;

COPY day_ahead_price FROM '[Insert File Path]\day_ahead_price.csv' DELIMITER ',' CSV HEADER;
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
	generate_series('2015-01-01'::DATE, '2025-02-01'::DATE, INTERVAL '1 month')::DATE;

INSERT INTO day_dim (date)
SELECT
	generate_series('2015-01-05'::DATE, '2025-03-31'::DATE, INTERVAL '1 day')::DATE;

COPY production_type_actual
FROM '[Insert File Path]\production_by_type.csv'
DELIMITER ',' CSV HEADER;

COPY total_load
FROM '[Insert File Path]\total_load.csv'
DELIMITER ',' CSV HEADER;

COPY congestion_costs
FROM '[Insert File Path]\congestion_costs.csv'
DELIMITER ',' CSV HEADER;

COPY price_stats
FROM '[Insert File Path]\monthly_price_stats.csv'
DELIMITER ',' CSV HEADER;

COPY day_ahead_price
FROM '[Insert File Path]\day_ahead_price.csv'
DELIMITER ',' CSV HEADER;