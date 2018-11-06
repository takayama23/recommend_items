import math
import numpy as np
import random
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import func
from app import app, db, routes
from app.models import Evaluation, Favorite, Item, OrderHistory, RecommendType, User, UserAction
from app.recommend import same_type_users, same_type_items, most_watch_items, most_sale_items


# ホーム画面：「ランキング！」ボタン押下
@app.route('/create-recommend-items-to-home/<user_id>', methods=['GET', 'POST'])
@app.route('/create-recommend-items-to-home', methods=['GET', 'POST'])
def create_recommend_items_to_home_func(user_id=None):

    # ユーザーID
    user_id = int(user_id)

    # レコメンドタイプの取得
    recommend_type = request.form['recommend_type']

    # レコメンド関数の呼出
    if recommend_type == '1':

        recommend_items = most_watch_items()

    elif recommend_type == '2':

        recommend_items = most_sale_items()

    elif recommend_type == '3':

        recommend_items = most_watch_items(user_id)

    else:
        recommend_items = None

    return redirect(url_for('index_func', user_id=user_id, recommend_type=recommend_type,
                            recommend_items=recommend_items))


# ユーザー一覧画面: 「ログイン」ボタン押下
@app.route('/login/<user_id>')
def login_func(user_id):

    # 他ユーザーでログインしている場合はログアウトする
    if current_user.is_authenticated:
        logout_user()

    # ユーザー情報を取得してログイン
    user = User.query.filter_by(id=user_id).first()
    login_user(user, remember=True)

    # ログイン後、元の画面に戻る
    request_url = request.headers['REFERER']

    if request_url is None:
        request_url = '/index'

    return redirect(request_url)


# ユーザー一覧画面: 「ユーザー変更」ボタン押下
@app.route('/change-user')
def change_user_func():

    logout_user()

    # ログインしていない場合は、ランダムでログイン
    if current_user.is_anonymous:
        users = db.session.query(User.id).all()
        random.shuffle(users)
        user_id = list(users[0])[0]
        user = User.query.get(user_id)
        login_user(user, remember=True)
    else:
        pass

    # ログアウト後、元の画面に戻る
    request_url = request.headers['REFERER']

    if request_url is None:
        request_url = '/index'

    return redirect(request_url)


# ユーザー詳細画面:「前へ」ボタン押下
@app.route('/previous-user/<user_id>')
def previous_user_func(user_id):

    # 元のユーザーIDを保持
    user_id = int(user_id)
    original_user_id = user_id

    # ユーザーIDの最小を取得
    user_id_min = db.session.query(func.min(User.id)).first()

    # 次のユーザーが見つかるまでユーザーコードを１ずつ減らす。見つからずに最小値まで行った場合はループを抜ける
    user = None
    while user is None:
        if user_id > user_id_min[0]:
            user_id -= 1
        else:
            flash('これ以上ユーザーはいません。')
            break
        user = User.query.get(user_id)
    user_id = user.id if user is not None else original_user_id

    return redirect(url_for('user_detail_func', user_id=user_id))


# ユーザー詳細画面:「次へ」ボタン押下
@app.route('/next-user/<user_id>')
def next_user_func(user_id):

    # 元のユーザーIDを保持
    user_id = int(user_id)
    original_user_id = user_id

    # ユーザーIDの最大値を取得
    user_id_max = db.session.query(func.max(User.id)).first()

    # 次のユーザーが見つかるまでユーザーIDを1ずつ増やす。見つからずに最大値まで行った場合はループを抜ける
    user = None
    while user is None:
        if user_id < user_id_max[0]:
            user_id += 1
        else:
            flash('これ以上ユーザーはいまません。')
            break
        user = User.query.get(user_id)
    user_id = user.id if user is not None else original_user_id

    return redirect(url_for('user_detail_func', user_id=int(user_id)))


# ユーザー詳細画面:「オススメ！」ボタン押下
@app.route('/create-recommend-items-to-user/<user_id>', methods=['GET', 'POST'])
def create_recommend_items_to_user_func(user_id):

    # ユーザーID
    user_id = int(user_id)

    # レコメンドタイプの取得
    recommend_type = request.form['recommend_type']

    # レコメンド関数の呼出
    if recommend_type == '101':

        recommend_items = same_type_users(user_id, 1)

    elif recommend_type == '102':

        recommend_items = same_type_users(user_id, 5)

    else:
        recommend_items = None

    return redirect(url_for('user_detail_func', user_id=user_id, recommend_type=recommend_type,
                            recommend_items=recommend_items))


# 商品詳細画面:「前へ」ボタン押下
@app.route('/previous-item/<item_code>')
def previous_item_func(item_code):

    # 元の商品コードを保持
    item_code = int(item_code)
    original_item_code = int(item_code)

    # 商品コードの最小値を取得
    item_code_min = db.session.query(func.min(Item.item_code)).first()

    # 次の商品が見つかるまで商品コードを1ずつ減らす。見つからずに最小値まで行った場合はループを抜ける
    item = None
    while item is None:
        if item_code > item_code_min[0]:
            item_code -= 1
        else:
            flash('これ以上商品はありません。')
            break

        item = Item.query.filter_by(item_code=item_code).first()
    item_code = item.item_code if item is not None else original_item_code

    return redirect(url_for('item_detail_func', item_code=item_code))


# 商品詳細画面:「次へ」ボタン押下
@app.route('/next-item/<item_code>')
def next_item_func(item_code):

    # 元の商品コードを保持
    item_code = int(item_code)
    original_item_code = int(item_code)

    # 商品コードの最大値を取得
    item_code_max = db.session.query(func.max(Item.item_code)).first()

    # 次の商品が見つかるまで商品コードを1ずつ増やす。見つからずに最大値まで行った場合はループを抜ける
    item = None
    while item is None:
        if item_code < item_code_max[0]:
            item_code += 1
        else:
            flash('これ以上商品はありません。')
            break
        item = Item.query.filter_by(item_code=item_code).first()
    item_code = item.item_code if item is not None else original_item_code

    return redirect(url_for('item_detail_func', item_code=item_code))


# 商品詳細画面:行動履歴関連ボタン押下
@app.route('/user_action/<action_code>/<item_code>', methods=['GET', 'POST'])
def user_action_func(action_code, item_code):

    item_code = int(item_code)
    if current_user.is_authenticated:
        user_id = int(current_user.get_id())
    else:
        user_id = None

    user_action_id = None

    # お気に入りの作成
    if action_code == '2' or action_code == '-2':
        favorite = Favorite.query.filter_by(user_id=user_id, item_code=item_code).first()
        if favorite:
            favorite.favorite_flag = True if favorite.favorite_flag is False else False
        else:
            favorite = Favorite(user_id=user_id,
                                item_code=item_code,
                                favorite_flag=True)
        db.session.add(favorite)
        if action_code == '2':
            message = '「いいね！」しました。'
        else:
            message = '「いいね！」を取り消しました。'

    # 購入履歴の作成
    elif action_code == '4':
        item = Item.query.filter_by(item_code=item_code).first()
        on_tax = app.config['TAX'] + 1.0
        price_on_tax = math.floor(item.price * on_tax)
        orders = int(np.random.choice(a=[1, 2, 3, 4, 5],
                                      size=1,
                                      p=[0.85, 0.07, 0.04, 0.025, 0.015],
                                      replace=True)[0])

        order_history = OrderHistory(user_id=user_id,
                                     item_code=item_code,
                                     orders=orders,
                                     price_no_tax=item.price * orders,
                                     price_on_tax=price_on_tax * orders)
        db.session.add(order_history)
        message = '商品を購入しました。'

    # 商品評価の作成
    elif action_code == '5':
        evaluation_code = int(request.form['evaluation'])
        evaluation = Evaluation.query.filter_by(user_id=user_id, item_code=item_code).first()
        user_action_id = db.session.query(UserAction.id).filter(UserAction.action_code.in_(['-5', '0', '5'])).filter_by(
            user_id=user_id,
            item_code=item_code).first()
        if evaluation:
            evaluation.evaluation_code = evaluation_code
        else:
            evaluation = Evaluation(user_id=user_id,
                                    item_code=item_code,
                                    evaluation_code=evaluation_code)
        db.session.add(evaluation)
        message = '商品を評価しました。'

        # 評価によってアクションコードを振り分ける
        if 1 <= evaluation_code < 3:
            action_code = -5
        elif evaluation_code >= 4:
            action_code = 5
        else:
            action_code = 0
    elif action_code == '1':
        message = '商品を閲覧しました。'
    else:
        message = '商品をカートに追加しました。'

    # 行動履歴の作成
    if user_action_id:
        action_code = str(action_code)
        user_action = UserAction.query.get(user_action_id)
        user_action.action_code = action_code
    else:
        user_action = UserAction(user_id=user_id,
                                 item_code=item_code,
                                 action_code=action_code)

    db.session.add(user_action)
    db.session.commit()

    flash(message)
    return redirect(url_for('item_detail_func', item_code=item_code))


# 商品詳細画面:「オススメ！」ボタン押下
@app.route('/create-recommend-items-to-item/<item_code>', methods=['GET', 'POST'])
def create_recommend_items_to_item_func(item_code):

    # ユーザーID
    item_code = int(item_code)

    # レコメンドタイプの取得
    recommend_type = request.form['recommend_type']

    # レコメンド関数の呼出
    if recommend_type == '201':

        recommend_items = same_type_items(item_code, 1)

    elif recommend_type == '202':

        recommend_items = same_type_items(item_code, 5)

    else:

        recommend_items = None

    return redirect(url_for('item_detail_func', item_code=item_code, recommend_type=recommend_type,
                            recommend_items=recommend_items))
