import codecs
import random
import numpy as pd
from flask_login import current_user
from app import app, db
from app.models import Evaluation, Favorite, Item, OrderHistory, RecommendType, User
from app.functions import pd_sql_to_df


# 参考ユーザーの購買商品（和集合）から対象ユーザーの購買商品を引く（差集合）
def select_items(ref_user_ids, target_user_id):
    sql_file = 'recommend_items/app/static/sql/recommend_sql/select_items.sql'

    # 条件文作成
    ref_user_select = 'WHERE a.user_id IN ('
    for ref_user_id in ref_user_ids:
        ref_user_select = ref_user_select + str(ref_user_id) + ','

    ref_user_select = ref_user_select[:-1] + ')'
    target_user_select = 'WHERE b.user_id = ' + str(target_user_id)

    with codecs.open(sql_file, 'r', 'utf-8') as f:
        sql = f.read()
        sql = sql.format(ref_user_select, target_user_select)
        df = pd_sql_to_df(sql)

    item_codes = []
    for row in df.itertuples():
        item_codes.append(row[1])

    return item_codes