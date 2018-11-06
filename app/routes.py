import app.events
import math
import random
from flask import render_template
from flask_login import current_user, login_user, logout_user
from sqlalchemy import func
from app import app, db
from app.models import Evaluation, Favorite, Item, OrderHistory, RecommendType, User


# ホーム画面
@app.route('/')
@app.route('/index')
@app.route('/index/<user_id>')
@app.route('/<user_id>/<recommend_type>/<recommend_items>')
def index_func(user_id=None, recommend_type=None, recommend_items=None):

    if user_id:
        user = User.query.get(user_id)
        login_user(user)
    elif current_user.is_authenticated:
        user = User.query.get(current_user.get_id())
    else:
        user = None

    # ログインしていない場合は、ランダムでログイン
    if current_user.is_anonymous:
        users = db.session.query(User.id).all()
        random.shuffle(users)
        user_id = list(users[0])[0]
        user = User.query.get(user_id)
        login_user(user, remember=True)
    else:
        pass

    # ホームページ向け（target=2）のレコメンド種類情報の取得
    recommend_type_list = RecommendType.query.filter_by(target=0).order_by(RecommendType.order_number).all()

    # 選択されたレコメンドタイプ
    if recommend_type:
        recommend_type = RecommendType.query.get(recommend_type)

    # レコメンド商品リスト
    recommend_item_list = []

    recommend_items = None if recommend_items is None else recommend_items[1:-1]

    if recommend_items:
        recommend_items = recommend_items.split(',')
        for recommend_item in recommend_items:
            item = Item.query.filter_by(item_code=recommend_item).first()
            recommend_item_list.append(item)

    recommend_info = [recommend_type_list, recommend_type, recommend_item_list]

    return render_template('index.html', user_info=user, recommend_info=recommend_info)


# ユーザー一覧画面
@app.route('/users')
def users_func():

    # ユーザー情報のリスト作成
    user_info_list = []

    # TODO: いずれ検索に対応したい
    users = User.query.order_by(User.id).all()

    for no, user in enumerate(users, start=1):
        user_info = {
            "no": no,
            "id": user.id,
            "user_name": user.user_name,
            "sex": user.user_sex.sex,
            "age": user.age,
            "prefecture_name": user.user_prefecture.prefecture_name
        }
        user_info_list.append(user_info)

    # ユーザー一覧の項目ラベル
    user_list_columns = ['No.', 'ユーザーID', 'ユーザー名', '性別', '年齢', '都道府県']
    # 表示するユーザー一覧（[[項目のリスト], [ユーザー情報]]）
    user_list = [user_list_columns, user_info_list]

    return render_template('users.html', user_list=user_list)


# ユーザー詳細画面
@app.route('/users/<user_id>')
@app.route('/users/<user_id>/<recommend_type>/<recommend_items>')
def user_detail_func(user_id, recommend_type=None, recommend_items=None):

    # 変数設定（購買情報／レコメンドの表示商品件数）
    limit = app.config['LIMIT']

    # 指定されたユーザーの基本情報の取得
    user = User.query.filter_by(id=user_id).first()

    # 指定されたユーザーの購買情報の取得
    order_histories = OrderHistory.query.filter_by(user_id=user_id).order_by(
        OrderHistory.order_date.desc()).limit(limit).all()

    # ユーザー詳細の項目ラベル
    user_info_columns = ['ユーザーID', 'ユーザー名', '性別', '年齢', '都道府県']

    # 購買情報の項目ラベル
    order_histories_columns = ['注文日', '商品コード', '商品名', '価格（税抜）', '数量', '購入金額（税込）']

    # ユーザー情報のリスト
    user_info = [user_info_columns, user, order_histories_columns, order_histories]

    # ユーザー向け（target=1）のレコメンド種類情報の取得
    recommend_type_list = RecommendType.query.filter_by(target=1).order_by(RecommendType.order_number).all()

    # 選択されたレコメンドタイプ
    if recommend_type:
        recommend_type = RecommendType.query.filter_by(type_code=recommend_type).first()
        
    # レコメンド商品リスト
    recommend_item_list = []

    recommend_items = None if recommend_items is None else recommend_items[1:-1]

    if recommend_items:
        recommend_items = recommend_items.split(',')
        for recommend_item in recommend_items:
            item = Item.query.filter_by(item_code=recommend_item).first()
            recommend_item_list.append(item)

    # レコメンド情報リスト
    recommend_info = [recommend_type_list, recommend_type, recommend_item_list]

    return render_template('user_detail.html', user_info=user_info, recommend_info=recommend_info)


# 商品一覧画面
@app.route('/items')
def items_func():

    # 定数取得（消費税）
    on_tax_rate = 1.00 + app.config['TAX']

    # 商品情報のリスト作成
    item_info_list = []
    # TODO: いずれ検索などに対応
    items = Item.query.order_by(Item.item_code).all()

    for no, item in enumerate(items, start=1):

        item_info = {
                    "no": no,
                    "item_code": item.item_code,
                    "item_name": item.item_name,
                    "brand_name": item.item_brand.brand_name,
                    "price": '{:,}'.format((lambda price, on_tax: math.floor(price * on_tax))(item.price, on_tax_rate))
                    }
        item_info_list.append(item_info)

    # 商品一覧の項目ラベル
    item_list_columns = ['No.', '商品コード', '商品名', 'ブランド名', '価格（税込）']
    # 表示する商品一覧（[[項目のリスト], [{商品情報}]]）
    item_list = [item_list_columns, item_info_list]

    return render_template('items.html', item_list=item_list)


# 商品詳細画面
@app.route('/items/<item_code>')
@app.route('/items/<item_code>/<recommend_type>/<recommend_items>/')
def item_detail_func(item_code, recommend_type=None, recommend_items=None):

    # 商品基本情報
    item = Item.query.filter_by(item_code=item_code).first()

    # 商品販売数
    item_orders = db.session.query(OrderHistory.orders).filter_by(item_code=item_code).all()
    item_sales = sum([item_order[0] for item_order in item_orders]) if item_orders else 0

    # ユーザー情報取得（お気に入り／評価情報）
    user_id = current_user.get_id() if current_user.is_authenticated else None

    user_favorite = db.session.query(Favorite.favorite_flag).\
        filter_by(user_id=user_id, item_code=item_code).first()

    user_evaluation = db.session.query(Evaluation.evaluation_code).\
        filter_by(user_id=user_id, item_code=item_code).first()

    # 平均評価
    evaluation = db.session.query(func.avg(Evaluation.evaluation_code).label("avg")).\
        filter_by(item_code=item_code).filter(Evaluation.evaluation_code > 0).first()[0]
    evaluation_avg = round(evaluation, 1) if evaluation else "まだ評価がありません。"

    # 商品詳細の項目ラベル
    item_info_columns = ['商品コード', '商品名', 'ブランド', '商品種別', '分類', 'シリーズ',
                         '価格（税抜）', '販売数', '平均評価', '画像']

    # 商品情報リスト
    item_info = [item_info_columns, item, item_sales, user_favorite, user_evaluation, evaluation_avg]

    # 商品向け（target=2）のレコメンド種類情報の取得
    recommend_type_list = RecommendType.query.filter_by(target=2).order_by(RecommendType.order_number).all()

    # 選択されたレコメンドタイプ
    if recommend_type:
        recommend_type = RecommendType.query.filter_by(type_code=recommend_type).first()

    # レコメンド商品リスト
    recommend_item_list = []

    recommend_items = None if recommend_items is None else recommend_items[1:-1]

    if recommend_items:
        recommend_items = recommend_items.split(',')
        for recommend_item in recommend_items:
            item = Item.query.filter_by(item_code=recommend_item).first()
            recommend_item_list.append(item)

    # レコメンド情報リスト
    recommend_info = [recommend_type_list, recommend_type, recommend_item_list]

    return render_template('item_detail.html', item_info=item_info, recommend_info=recommend_info)


# レコメンドタイプ一覧画面
@app.route('/recommend-types')
def recommend_types_func():

    # レコメンドタイプの取得
    recommend_type_info = RecommendType.query.order_by(RecommendType.id).all()

    # レコメンドタイプ一覧の項目ラベル
    recommend_type_info_columns = ['No.', 'コード', '種類', 'レコメンド名', 'コメント', '表示順']

    # レコメンドタイプリストの設定
    recommend_type_list = [recommend_type_info_columns, recommend_type_info]

    return render_template('recommend_types.html', recommend_type_list=recommend_type_list)
