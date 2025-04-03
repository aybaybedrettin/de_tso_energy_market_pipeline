-- Generation, load, costs, and price statistics except for price itself
SELECT
	m.date,
	z.zone_name,
	c.total_cost,
	c.redispatching_cost,
	c.countertrading_cost,
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
	t.total_load,
	ps.volatility,
	ps.max_price,
	ps.min_price,
	ps.median_price
FROM
	congestion_costs AS c
INNER JOIN	month_dim AS m ON c.month_id = m.month_id
INNER JOIN	production_type_actual AS p ON c.month_id = p.month_id AND c.control_zone_id = p.control_zone_id
INNER JOIN	total_load AS t ON c.month_id = t.month_id AND c.control_zone_id = t.control_zone_id
INNER JOIN	price_stats AS ps ON c.month_id = ps.month_id
INNER JOIN  zone_dim AS z ON c.control_zone_id = z.control_zone_id
ORDER BY date, zone_name;

-- Price
SELECT
	d.date,
	p.price
FROM
	day_ahead_price AS p
INNER JOIN
	day_dim AS d ON p.day_id = d.day_id;