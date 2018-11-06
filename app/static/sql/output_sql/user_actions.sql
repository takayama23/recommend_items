SELECT
     id
    ,user_id
    ,item_code
    ,action_code
    ,timestamp
FROM
    public.user_actions
LIMIT 10
