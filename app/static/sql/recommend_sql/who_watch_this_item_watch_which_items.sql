select
     user_id
    ,count(1) as watch_count
from
    user_actions
where
    action_code = '1'
{}
group by
    user_id
order by
    watch_count desc
limit {}