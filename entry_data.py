import codecs
import math
import random
import numpy as np
import pandas as pd
from app import app, db, fake
from app.models import Evaluation, Favorite, Item, User, UserAction, OrderHistory


# 基本マスタ登録
def entry_basic_masters():

    # データ削除・シーケンスリセット処理
    sql_files = ['./app/static/sql/entry_data_sql/truncate_areas.sql',
                 './app/static/sql/entry_data_sql/reset_areas_id_seq.sql',
                 './app/static/sql/entry_data_sql/truncate_prefectures.sql',
                 './app/static/sql/entry_data_sql/reset_prefectures_id_seq.sql',
                 './app/static/sql/entry_data_sql/truncate_sexes.sql',
                 './app/static/sql/entry_data_sql/reset_sexes_id_seq.sql',
                 './app/static/sql/entry_data_sql/truncate_brands.sql',
                 './app/static/sql/entry_data_sql/reset_brands_id_seq.sql',
                 './app/static/sql/entry_data_sql/truncate_categories1.sql',
                 './app/static/sql/entry_data_sql/reset_categories1_id_seq.sql',
                 './app/static/sql/entry_data_sql/truncate_categories2.sql',
                 './app/static/sql/entry_data_sql/reset_categories2_id_seq.sql',
                 './app/static/sql/entry_data_sql/truncate_categories3.sql',
                 './app/static/sql/entry_data_sql/reset_categories3_id_seq.sql'
                 ]

    for sql_file in sql_files:

        # SQLファイルの読込とSQL実行
        with codecs.open(sql_file, 'r', 'utf-8') as f:
            sql = f.read()

        db.session.execute(sql)
        db.session.commit()

    # 登録処理
    sql_files = ['./app/static/sql/entry_data_sql/entry_areas.sql',
                 './app/static/sql/entry_data_sql/entry_prefectures.sql',
                 './app/static/sql/entry_data_sql/entry_sexes.sql',
                 './app/static/sql/entry_data_sql/entry_brands.sql',
                 './app/static/sql/entry_data_sql/entry_categories1.sql',
                 './app/static/sql/entry_data_sql/entry_categories2.sql',
                 './app/static/sql/entry_data_sql/entry_categories3.sql'
                 ]

    for sql_file in sql_files:

        # SQLファイルの読込とSQL実行
        with codecs.open(sql_file, 'r', 'utf-8') as f:
            sql = f.read()

        db.session.execute(sql)
        db.session.commit()


# 商品マスタ登録
def entry_items():

    # データ削除・シーケンスリセット処理
    sql_files = [
                './app/static/sql/entry_data_sql/truncate_items.sql',
                './app/static/sql/entry_data_sql/reset_items_id_seq.sql'
                ]

    for sql_file in sql_files:

        # SQLファイルの読込とSQL実行
        with codecs.open(sql_file, 'r', 'utf-8') as f:
            sql = f.read()

        db.session.execute(sql)
        db.session.commit()

    # 登録処理
    sql_file = './app/static/sql/entry_data_sql/entry_items.sql'

    # SQLファイルの読込とSQL実行
    with codecs.open(sql_file, 'r', 'utf-8') as f:
        sql = f.read()

        db.session.execute(sql)
        db.session.commit()


# ユーザー登録
def entry_users(num=500):

    # データ削除・シーケンスリセット処理
    sql_files = ['./app/static/sql/entry_data_sql/truncate_users.sql',
                 './app/static/sql/entry_data_sql/reset_users_id_seq.sql'
                 ]

    for sql_file in sql_files:
        # SQLファイルの読込とSQL実行
        with codecs.open(sql_file, 'r', 'utf-8') as f:
            sql = f.read()

        db.session.execute(sql)
        db.session.commit()

    # 登録処理（pandasを使用）
    df = pd.read_csv('./app/static/csv/sample_users.csv')
    users = []

    # ファイルからユーザー名と性別を取得。都道府県と年齢はランダム
    for row in df.itertuples():
        if row[0] >= int(num):
            break

        user = User(user_name=row[1],
                    sex=row[2],
                    prefecture_code=random.randrange(1, 48),
                    age=random.randint(10, 99))
        users.append(user)

    db.session.add_all(users)
    db.session.commit()


# レコメンドタイプ登録
def entry_recommend_types():

    # データ削除・シーケンスリセット処理
    sql_files = ['./app/static/sql/entry_data_sql/truncate_recommend_types.sql',
                 './app/static/sql/entry_data_sql/reset_recommend_types_id_seq.sql'
                 ]

    for sql_file in sql_files:
        # SQLファイルの読込とSQL実行
        with codecs.open(sql_file, 'r', 'utf-8') as f:
            sql = f.read()

        db.session.execute(sql)
        db.session.commit()

    # 登録処理
    sql_file = './app/static/sql/entry_data_sql/entry_recommend_types.sql'

    # SQLファイルの読込とSQL実行
    with codecs.open(sql_file, 'r', 'utf-8') as f:
        sql = f.read()

        db.session.execute(sql)
        db.session.commit()


# 行動履歴（閲覧）登録
def entry_user_actions_watch(num):

    # データ削除・シーケンスリセット処理
    sql_files = ['./app/static/sql/entry_data_sql/truncate_user_actions.sql',
                 './app/static/sql/entry_data_sql/reset_user_actions_id_seq.sql',
                 './app/static/sql/entry_data_sql/truncate_order_histories.sql',
                 './app/static/sql/entry_data_sql/reset_order_histories_id_seq.sql'
                 ]

    for sql_file in sql_files:

        # SQLファイルの読込とSQL実行
        with codecs.open(sql_file, 'r', 'utf-8') as f:
            sql = f.read()

        db.session.execute(sql)
        db.session.commit()

    users = [i[0] for i in db.session.query(User.id).all()]
    items = [i[0] for i in db.session.query(Item.item_code).all()]

    # numpyの配列を使用する
    np_users = np.array(users)
    np_items = np.array(items)

    # 閲覧履歴の登録
    for _ in range(int(num)):
        user_id = int(np.random.choice(np_users, 1, replace=True)[0])
        item_code = str(np.random.choice(np_items, 1, replace=True)[0])
        action_code = '1'
        user_action = UserAction(user_id=user_id,
                                 item_code=item_code,
                                 action_code=action_code)
        db.session.add(user_action)
        db.session.commit()


# 行動履歴登録（お気に入りorカートに追加）
def entry_user_actions_favorite_or_cart():

    user_actions_watch = UserAction.query.filter_by(action_code='1').all()

    # 閲覧履歴からお気に入りとカートに追加する
    for user_action_watch in user_actions_watch:
        # 閲覧の92%は見ただけ、6%はお気に入り、2%はカートに追加と設定
        action_code = str(np.random.choice(a=['1', '2', '3'],
                                           size=1,
                                           p=[0.92, 0.06, 0.02],
                                           replace=True)[0])
        # 閲覧のみはスキップ
        if action_code == '1':
            continue
        # お気に入り
        elif action_code == '2':

            user_actions_favorite = UserAction.query.filter_by(user_id=user_action_watch.user_id,
                                                               item_code=user_action_watch.item_code,
                                                               action_code='2').first()
            # すでにお気に入りにしている場合はパス
            if user_actions_favorite:
                pass
            else:
                user_action_favorite = UserAction(user_id=user_action_watch.user_id,
                                                  item_code=user_action_watch.item_code,
                                                  action_code='2')
                db.session.add(user_action_favorite)

                # お気に入りテーブル登録
                favorite = Favorite(user_id=user_action_watch.user_id,
                                    item_code=user_action_watch.item_code,
                                    favorite_flag=True)
                db.session.add(favorite)

            # お気に入りにした人のうちの20%がカートに追加と設定
            action_code_cart = str(np.random.choice(a=['2', '3'],
                                                    size=1,
                                                    p=[0.8, 0.2],
                                                    replace=True)[0])
            if action_code_cart == '3':
                user_action_cart = UserAction(user_id=user_action_watch.user_id,
                                              item_code=user_action_watch.item_code,
                                              action_code='3')
                db.session.add(user_action_cart)
        # カートに追加（お気に入りにせずに追加）
        else:
            user_action_cart = UserAction(user_id=user_action_watch.user_id,
                                          item_code=user_action_watch.item_code,
                                          action_code='3')
            db.session.add(user_action_cart)

        db.session.commit()


# 行動履歴登録（購入）
def entry_user_actions_buy():

    user_actions_cart = UserAction.query.filter_by(action_code='3').all()

    # カートに追加された行動履歴から購入履歴を作成する
    for user_action_cart in user_actions_cart:
        # カートに追加された商品の60%が購入されたと設定
        action_code = str(np.random.choice(a=['3', '4'],
                                           size=1,
                                           p=[0.4, 0.6],
                                           replace=True)[0])
        # カート追加のみはスキップ
        if action_code == '3':
            continue
        else:
            user_action_buy = UserAction(user_id=user_action_cart.user_id,
                                         item_code=user_action_cart.item_code,
                                         action_code='4')
            db.session.add(user_action_buy)

        db.session.commit()


# 行動履歴登録（高評価）/評価テーブル登録
def entry_user_actions_review():

    user_actions_buy = UserAction.query.filter_by(action_code='4').all()

    for user_action_buy in user_actions_buy:
        # 購入した人による評価設定（評価はランダム）
        evaluation = Evaluation.query.filter_by(user_id=user_action_buy.user_id,
                                                item_code=user_action_buy.item_code).first()
        # すでに評価がある場合はパス
        if evaluation:
            pass
        else:
            evaluation_code = int(np.random.choice(a=[0, 1, 2, 3, 4, 5], size=1, replace=True)[0])
            evaluation = Evaluation(user_id=user_action_buy.user_id,
                                    item_code=user_action_buy.item_code,
                                    evaluation_code=evaluation_code)
            db.session.add(evaluation)

            # 行動履歴（評価）登録
            if evaluation_code in (1, 2):
                action_code = -5
            elif evaluation_code in (4, 5):
                action_code = 5
            else:
                action_code = 0

            user_action_review = UserAction(user_id=user_action_buy.user_id,
                                            item_code=user_action_buy.item_code,
                                            action_code=action_code)
            db.session.add(user_action_review)

        db.session.commit()


# 購買履歴登録
def entry_order_histories():

    user_actions_buy = UserAction.query.filter_by(action_code='4').all()

    # 行動履歴から購買履歴を作成する
    for user_action_buy in user_actions_buy:
        item = Item.query.filter_by(item_code=user_action_buy.item_code).first()
        orders = int(np.random.choice(a=[1, 2, 3, 4, 5],
                                      size=1,
                                      p=[0.85, 0.07, 0.04, 0.025, 0.015],
                                      replace=True)[0])
        on_tax = app.config['TAX'] + 1.0
        price_on_tax = math.floor(item.price * on_tax)

        # 注文日は当日から過去3年間でランダムに作成
        order_history = OrderHistory(order_date=fake.date_between(start_date='-3y', end_date='today'),
                                     user_id=user_action_buy.user_id,
                                     item_code=user_action_buy.item_code,
                                     orders=orders,
                                     price_no_tax=item.price * orders,
                                     price_on_tax=price_on_tax * orders)

        db.session.add(order_history)
        db.session.commit()
