/*
Creating the data tables including dimension tables for control zone, day and the month.
*/

CREATE TABLE zone_dim (
	control_zone_id SERIAL PRIMARY KEY,
	zone_name TEXT UNIQUE);

CREATE TABLE month_dim (
	month_id SERIAL PRIMARY KEY,
	date DATE UNIQUE);

CREATE TABLE day_dim (
	day_id SERIAL PRIMARY KEY,
	date DATE UNIQUE);

CREATE TABLE production_type_actual (
	control_zone_id INT,
	month_id INT,
	biomass NUMERIC,
	hydropower NUMERIC,
	wind_offshore NUMERIC,
	wind_onshore NUMERIC,
	photovoltaics NUMERIC,
	other_renewable NUMERIC,
	lignite NUMERIC,
	hard_coal NUMERIC,
	fossil_gas NUMERIC,
	hydro_pumped_storage NUMERIC,
	other_conventional NUMERIC,
	nuclear NUMERIC,
	PRIMARY KEY (control_zone_id, month_id),
	FOREIGN KEY (control_zone_id) REFERENCES public.zone_dim (control_zone_id),
	FOREIGN KEY (month_id) REFERENCES public.month_dim (month_id));

CREATE TABLE total_load (
	control_zone_id INT,
	month_id INT,
	grid_load NUMERIC,
	hydro_pumped_storage NUMERIC,
	residual_load NUMERIC,
	PRIMARY KEY (control_zone_id, month_id),
	FOREIGN KEY (control_zone_id) REFERENCES public.zone_dim (control_zone_id),
	FOREIGN KEY (month_id) REFERENCES public.month_dim (month_id));

CREATE TABLE congestion_costs (
	control_zone_id INT,
	month_id INT,
	balancing_services NUMERIC,
	network_security_of_the_tsos NUMERIC,
	countertrading NUMERIC,
	PRIMARY KEY (control_zone_id, month_id),
	FOREIGN KEY (control_zone_id) REFERENCES public.zone_dim (control_zone_id),
	FOREIGN KEY (month_id) REFERENCES public.month_dim (month_id));

CREATE TABLE price_stats (
	month_id INT PRIMARY KEY,
	volatility NUMERIC,
	FOREIGN KEY (month_id) REFERENCES public.month_dim (month_id));

CREATE TABLE day_ahead_price (
	day_id INT PRIMARY KEY,
	price NUMERIC,
	FOREIGN KEY (day_id) REFERENCES public.day_dim (day_id));