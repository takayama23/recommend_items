SELECT
     c.user_id
    ,c.item_code
    ,CASE WHEN e.user_id is NULL THEN 0 ELSE 1 END flag
FROM (SELECT
             a.id as user_id
            ,b.item_code
       FROM
            users a, items b
       ORDER BY a.id, b.item_code) c
LEFT JOIN (SELECT
                 d.user_id
                ,d.item_code
            FROM
                order_histories d
            GROUP BY d.user_id, d.item_code) e
ON  c.user_id = e.user_id
AND c.item_code = e.item_code
