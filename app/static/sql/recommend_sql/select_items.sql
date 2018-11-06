SELECT
    a.item_code
FROM
    order_histories a
{}
GROUP BY
    a.item_code
EXCEPT
SELECT
    b.item_code
FROM
    order_histories b
{}
GROUP BY
    b.item_code
