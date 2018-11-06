from datetime import date, datetime
from flask_login import UserMixin
from app import db, login


# ブランドモデル
class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(32), index=True)
    items = db.relationship('Item', backref='item_brand', lazy='dynamic')

    def __repr__(self):
        return '<Brand: id {}, name {}>'.format(self.id, self.brand_name)


# カテゴリー1モデル
class Category1(db.Model):
    __tablename__ = 'categories1'
    id = db.Column(db.Integer, primary_key=True)
    category1_name = db.Column(db.String(32), index=True)
    items = db.relationship('Item', backref='item_category1', lazy='dynamic')

    def __repr__(self):
        return '<Category1: id {}, name {}>'.format(self.id, self.category1_name)


# カテゴリー2モデル
class Category2(db.Model):
    __tablename__ = 'categories2'
    id = db.Column(db.Integer, primary_key=True)
    category2_name = db.Column(db.String(32), index=True)
    items = db.relationship('Item', backref='item_category2', lazy='dynamic')

    def __repr__(self):
        return '<Category2: id {}, name {}>'.format(self.id, self.category2_name)


# カテゴリー3モデル
class Category3(db.Model):
    __tablename__ = 'categories3'
    id = db.Column(db.Integer, primary_key=True)
    category3_name = db.Column(db.String(32), index=True)
    items = db.relationship('Item', backref='item_category3', lazy='dynamic')

    def __repr__(self):
        return '<Category3: id {}, name {}>'.format(self.id, self.category3_name)


# 商品モデル
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.Integer, index=True, unique=True)
    item_name = db.Column(db.String(32), index=True)
    file_name = db.Column(db.String(32), index=True, unique=True)
    brand_code = db.Column(db.Integer, db.ForeignKey('brands.id'), index=True)
    category1_code = db.Column(db.Integer, db.ForeignKey('categories1.id'), index=True)
    category2_code = db.Column(db.Integer, db.ForeignKey('categories2.id'), index=True)
    category3_code = db.Column(db.Integer, db.ForeignKey('categories3.id'), index=True)
    price = db.Column(db.Integer, index=True)
    order_histories = db.relationship('OrderHistory', backref='order_item', lazy='dynamic')

    def __repr__(self):
        return '<Item: item_code {}, name {}>'.format(self.item_code, self.item_name)


# 購入履歴
class OrderHistory(db.Model):
    __tablename__ = 'order_histories'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, default=date.today, index=True)
    user_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    item_code = db.Column(db.Integer, db.ForeignKey('items.item_code'), index=True)
    orders = db.Column(db.Integer, default=0)
    price_no_tax = db.Column(db.Integer, default=0)
    price_on_tax = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<OrderHistoryDetail id {}, user_id {}, item_code {}>'.format(self.id, self.user_id, self.item_code)


# 商品評価
class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    item_code = db.Column(db.Integer, db.ForeignKey('items.item_code'), index=True)
    evaluation_code = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Evaluation user_id {}, item_code {}>'.format(self.user_id, self.item_code)


# お気に入り
class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    item_code = db.Column(db.Integer, db.ForeignKey('items.item_code'), index=True)
    favorite_flag = db.Column(db.Boolean)

    def __repr__(self):
        return '<Favorite user_id {}, item_code {}>'.format(self.user_id, self.item_code)


# ユーザーモデル
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32), index=True)
    sex = db.Column(db.Integer, db.ForeignKey('sexes.id'), index=True)
    age = db.Column(db.Integer, index=True)
    prefecture_code = db.Column(db.Integer, db.ForeignKey('prefectures.id'), index=True)

    def __repr__(self):
        return '<User: id {}, user_name {}>'.format(self.id, self.user_name)


# 性別モデル
class Sex(db.Model):
    __tablename__ = 'sexes'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(2))
    users = db.relationship('User', backref='user_sex', lazy='dynamic')

    def __repr__(self):
        return '<Sex: id {}, sex {}>'.format(self.id, self.sex)


# 地域モデル
class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(8))
    prefectures = db.relationship('Prefecture', backref='prefecture_area', lazy='dynamic')

    def __repr__(self):
        return '<Area: area_code {}, area_name {}>'.format(self.area_code, self.area_name)


# 都道府県モデル
class Prefecture(db.Model):
    __tablename__ = 'prefectures'
    id = db.Column(db.Integer, primary_key=True)
    prefecture_name = db.Column(db.String(5))
    area_code = db.Column(db.Integer, db.ForeignKey('areas.id'), index=True)
    users = db.relationship('User', backref='user_prefecture', lazy='dynamic')

    def __repr__(self):
        return '<Sex: prefecture_code {}, prefecture_name {}>'.format(self.prefecture_code, self.prefecture_name)


# 行動履歴
class UserAction(db.Model):
    __tablename__ = 'user_actions'
    id = db.Column(db.Integer, primary_key=True)
#    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user_id = db.Column(db.Integer, index=True)
    item_code = db.Column(db.Integer, index=True)
    action_code = db.Column(db.String(2), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<UserAction user_id {}, item_code {}, action_code {}>'.format(self.user_id,
                                                                              self.item_code,
                                                                              self.action_code)


# レコメンド選択用
class RecommendType(db.Model):
    __tablename__ = 'recommend_types'
    id = db.Column(db.Integer, primary_key=True)
    type_code = db.Column(db.Integer, index=True, unique=True)
    target = db.Column(db.Integer, index=True)
    recommend_name = db.Column(db.String(30))
    title_message = db.Column(db.String(30))
    type_comment = db.Column(db.String(100))
    order_number = db.Column(db.Integer, index=True)


# LoginManager用ローダー
@login.user_loader
def load_user(id):
    return User.query.get(int(id))