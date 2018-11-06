-- 閲覧ランキング用SQL
SELECT
     item_code
    ,COUNT(1) AS COUNTS
FROM
    user_actions
WHERE
    action_code = '1'
{}
GROUP BY
    item_code
ORDER BY
    COUNTS DESC
LIMIT {}