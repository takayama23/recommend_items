--販売数ランキング用SQL
SELECT
     item_code
    ,SUM(orders) AS orders
FROM
	order_histories
GROUP BY
	item_code
ORDER BY
	orders DESC
LIMIT {}