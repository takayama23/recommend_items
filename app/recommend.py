import codecs
import random
import numpy as np
import pandas as pd
from flask_login import current_user
from app import app
from app.models import Item
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


# レコメンドタイプ1／3（みんな／ユーザーがよく閲覧している商品）
def most_watch_items(user_id=None):

    # レコメンド商品数の設定
    limit = app.config['LIMIT']

    sql_file = 'recommend_items/app/static/sql/recommend_sql/most_watch_items.sql'

    # SQLファイルの読込とSQL実行
    with codecs.open(sql_file, 'r', 'utf-8') as f:
        sql = f.read()

        # user_idが指定されていない場合は全ユーザー、指定されている場合はそのユーザーを条件にする
        if user_id is None:
            user_select = ''
        else:
            user_select = 'AND user_id = ' + str(user_id)

        sql = sql.format(user_select, limit)
        df = pd_sql_to_df(sql)

    # 取得した商品コードで商品テーブルを参照して商品情報を取得しリスト化する
    recommend_items = []
    for row in df.itertuples():
        item_code = int(row[1])
        # item = Item.query.filter_by(item_code=item_code).first()
        recommend_items.append(item_code)

    return recommend_items


# レコメンドタイプ2
def most_sale_items():

    # レコメンド商品数の設定
    limit = app.config['LIMIT']

    sql_file = 'recommend_items/app/static/sql/recommend_sql/most_sale_items.sql'

    with codecs.open(sql_file, 'r', 'utf-8') as f:
        sql = f.read()
        sql = sql.format(limit)
        df = pd_sql_to_df(sql)

    recommend_items = []
    for row in df.itertuples():
        item_code = int(row[1])
        recommend_items.append(item_code)

    return recommend_items


# レコメンドタイプ3（類似ユーザー１）, レコメンドタイプ4（類似ユーザー２）
def same_type_users(target_user_id, ref_users=1):

    # レコメンド商品数の設定
    limit = app.config['LIMIT']

    sql_file = 'recommend_items/app/static/sql/recommend_sql/which_users_buy_which_items.sql'

    with codecs.open(sql_file, 'r', 'utf-8') as f:
        sql = f.read()
        df = pd_sql_to_df(sql)

    # 縦持ちデータを横持ちデータに変換する
    data0 = df.pivot_table(values=['flag'], index=['user_id'], columns=['item_code'], aggfunc='sum')
    target_user_index = data0.index.get_loc(target_user_id)

    # 相関行列からtarget_user_id行列の相関係数ベクトルの取得
    data1 = np.corrcoef(data0)[target_user_index]

    # 相関係数の高い順に並べる
    data2 = (-data1).argsort()

    # 参考ユーザーの選択（インデックス取得）
    ref_user_ids = data2[1:ref_users+1]

    # 【参考】参考ユーザーの購買履歴取得
    # data3 = data0.iloc[ref_user_ids]

    # 参考ユーザーの購入商品から対象ユーザーの購入商品を引く
    recommend_items = select_items(ref_user_ids, target_user_id)

    # 5商品を抽出する
    recommend_items = recommend_items[0:limit]

    return recommend_items


# レコメンドタイプ5（類似商品１）, レコメンドタイプ6（類似商品２）
def same_type_items(target_item_code, ref_users=1):

    # レコメンド商品数の設定
    limit = app.config['LIMIT']

    sql_file = 'recommend_items/app/static/sql/recommend_sql/who_watch_this_item_watch_which_items.sql'

    # 条件分作成
    target_item_select = ' AND item_code = ' + str(target_item_code)

    with codecs.open(sql_file, 'r', 'utf-8') as f:
        sql = f.read()
        sql = sql.format(target_item_select, ref_users)
        df = pd_sql_to_df(sql)

    ref_user_ids = []
    for row in df.itertuples():
        ref_user_ids.append(row[1])

    # ログインユーザーの取得
    target_user_id = 0 if current_user.get_id() is None else current_user.get_id()
    # 参考ユーザーの購入商品から対象ユーザーの購入商品を引く
    recommend_items = select_items(ref_user_ids, target_user_id)

    # 5商品を抽出する
    recommend_items = recommend_items[0:limit]

    return recommend_items
