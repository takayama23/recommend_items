select
     a.item_code
    ,a.item_name
    ,b.brand_name
    ,c.category1_name
    ,d.category2_name
    ,e.category3_name
    ,a.price
from items a
inner join
    brands b
on
    a.brand_code = b.id
inner join
    categories1 c
on
    a.category1_code = c.id
inner join
    categories2 d
on
    a.category2_code = d.id
inner join
    categories3 e
on
    a.category3_code = e.id